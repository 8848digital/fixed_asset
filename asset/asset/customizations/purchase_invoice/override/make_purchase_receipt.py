import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


def asset_make_purchase_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.received_qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.conversion_factor)
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (
			(flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate) * flt(source_parent.conversion_rate)
		)

	doc = get_mapped_doc(
		"Purchase Invoice",
		source_name,
		{
			"Purchase Invoice": {
				"doctype": "Purchase Receipt",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Purchase Invoice Item": {
				"doctype": "Purchase Receipt Item",
				"field_map": {
					"name": "purchase_invoice_item",
					"parent": "purchase_invoice",
					"bom": "bom",
					"purchase_order": "purchase_order",
					"po_detail": "purchase_order_item",
					"material_request": "material_request",
					"material_request_item": "material_request_item",
					"wip_composite_asset": "wip_composite_asset",
				},
				"postprocess": update_item,
				"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty),
			},
			"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges"},
		},
		target_doc,
	)

	return doc
