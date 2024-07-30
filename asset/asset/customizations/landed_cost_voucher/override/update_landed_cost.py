import frappe
from frappe import _


def asset_update_landed_cost(self):
	for d in self.get("purchase_receipts"):
		doc = frappe.get_doc(d.receipt_document_type, d.receipt_document)
		# check if there are {qty} assets created and linked to this receipt document
		if self.docstatus != 2:
			validate_asset_qty_and_status(self, d.receipt_document_type, doc)

		# set landed cost voucher amount in pr item
		doc.set_landed_cost_voucher_amount()

		# set valuation amount in pr item
		doc.update_valuation_rate(reset_outgoing_rate=False)

		# db_update will update and save landed_cost_voucher_amount and voucher_amount in PR
		for item in doc.get("items"):
			item.db_update()

		# asset rate will be updated while creating asset gl entries from PI or PY

		# update latest valuation rate in serial no
		self.update_rate_in_serial_no_for_non_asset_items(doc)

	for d in self.get("purchase_receipts"):
		doc = frappe.get_doc(d.receipt_document_type, d.receipt_document)
		# update stock & gl entries for cancelled state of PR
		doc.docstatus = 2
		doc.update_stock_ledger(allow_negative_stock=True, via_landed_cost_voucher=True)
		doc.make_gl_entries_on_cancel()

		# update stock & gl entries for submit state of PR
		doc.docstatus = 1
		doc.make_bundle_using_old_serial_batch_fields(via_landed_cost_voucher=True)
		doc.update_stock_ledger(allow_negative_stock=True, via_landed_cost_voucher=True)
		if d.receipt_document_type == "Purchase Receipt":
			doc.make_gl_entries(via_landed_cost_voucher=True)
		else:
			doc.make_gl_entries()
		doc.repost_future_sle_and_gle(via_landed_cost_voucher=True)


def validate_asset_qty_and_status(self, receipt_document_type, receipt_document):
	for item in self.get("items"):
		if item.is_fixed_asset:
			receipt_document_type = (
				"purchase_invoice" if item.receipt_document_type == "Purchase Invoice" else "purchase_receipt"
			)
			docs = frappe.db.get_all(
				"Asset",
				filters={
					receipt_document_type: item.receipt_document,
					"item_code": item.item_code,
					"docstatus": ["!=", 2],
				},
				fields=["name", "docstatus"],
			)
			if not docs or len(docs) < item.qty:
				frappe.throw(
					_(
						"There are only {0} asset created or linked to {1}. Please create or link {2} Assets with respective document."
					).format(len(docs), item.receipt_document, item.qty)
				)
			if docs:
				for d in docs:
					if d.docstatus == 1:
						frappe.throw(
							_(
								"{0} <b>{1}</b> has submitted Assets. Remove Item <b>{2}</b> from table to continue."
							).format(
								item.receipt_document_type, item.receipt_document, item.item_code
							)
						)
