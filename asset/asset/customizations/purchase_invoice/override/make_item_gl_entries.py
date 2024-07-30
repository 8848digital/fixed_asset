import frappe
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import (
	get_purchase_document_details,
)
from erpnext.accounts.utils import get_account_currency
from erpnext.stock import get_warehouse_account_map
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
	get_item_account_wise_additional_cost,
)
from frappe import _
from frappe.utils import cint, flt


def asset_make_item_gl_entries(self, gl_entries):
	# item gl entries
	stock_items = self.get_stock_items()
	if self.update_stock and self.auto_accounting_for_stock:
		warehouse_account = get_warehouse_account_map(self.company)

	landed_cost_entries = get_item_account_wise_additional_cost(self.name)

	voucher_wise_stock_value = {}
	if self.update_stock:
		stock_ledger_entries = frappe.get_all(
			"Stock Ledger Entry",
			fields=["voucher_detail_no", "stock_value_difference", "warehouse"],
			filters={"voucher_no": self.name, "voucher_type": self.doctype, "is_cancelled": 0},
		)
		for d in stock_ledger_entries:
			voucher_wise_stock_value.setdefault(
				(d.voucher_detail_no, d.warehouse), d.stock_value_difference
			)

	valuation_tax_accounts = [
		d.account_head
		for d in self.get("taxes")
		if d.category in ("Valuation", "Total and Valuation")
		and flt(d.base_tax_amount_after_discount_amount)
	]

	exchange_rate_map, net_rate_map = get_purchase_document_details(self)

	provisional_accounting_for_non_stock_items = cint(
		frappe.get_cached_value(
			"Company", self.company, "enable_provisional_accounting_for_non_stock_items"
		)
	)
	if provisional_accounting_for_non_stock_items:
		self.get_provisional_accounts()

	for item in self.get("items"):
		if flt(item.base_net_amount):
			account_currency = get_account_currency(item.expense_account)
			if item.item_code:
				frappe.get_cached_value("Item", item.item_code, "asset_category")

			if (
				self.update_stock
				and self.auto_accounting_for_stock
				and (item.item_code in stock_items or item.is_fixed_asset)
			):
				# warehouse account
				warehouse_debit_amount = self.make_stock_adjustment_entry(
					gl_entries, item, voucher_wise_stock_value, account_currency
				)

				if item.from_warehouse:
					gl_entries.append(
						self.get_gl_dict(
							{
								"account": warehouse_account[item.warehouse]["account"],
								"against": warehouse_account[item.from_warehouse]["account"],
								"cost_center": item.cost_center,
								"project": item.project or self.project,
								"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
								"debit": warehouse_debit_amount,
							},
							warehouse_account[item.warehouse]["account_currency"],
							item=item,
						)
					)

					credit_amount = item.base_net_amount
					if self.is_internal_supplier and item.valuation_rate:
						credit_amount = flt(item.valuation_rate * item.stock_qty)

					# Intentionally passed negative debit amount to avoid incorrect GL Entry validation
					gl_entries.append(
						self.get_gl_dict(
							{
								"account": warehouse_account[item.from_warehouse]["account"],
								"against": warehouse_account[item.warehouse]["account"],
								"cost_center": item.cost_center,
								"project": item.project or self.project,
								"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
								"debit": -1 * flt(credit_amount, item.precision("base_net_amount")),
							},
							warehouse_account[item.from_warehouse]["account_currency"],
							item=item,
						)
					)

					# Do not book expense for transfer within same company transfer
					if not self.is_internal_transfer():
						gl_entries.append(
							self.get_gl_dict(
								{
									"account": item.expense_account,
									"against": self.supplier,
									"debit": flt(item.base_net_amount, item.precision("base_net_amount")),
									"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
									"cost_center": item.cost_center,
									"project": item.project,
								},
								account_currency,
								item=item,
							)
						)

				else:
					if not self.is_internal_transfer():
						gl_entries.append(
							self.get_gl_dict(
								{
									"account": item.expense_account,
									"against": self.supplier,
									"debit": warehouse_debit_amount,
									"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
									"cost_center": item.cost_center,
									"project": item.project or self.project,
								},
								account_currency,
								item=item,
							)
						)

				# Amount added through landed-cost-voucher
				if landed_cost_entries:
					if (item.item_code, item.name) in landed_cost_entries:
						for account, amount in landed_cost_entries[(item.item_code, item.name)].items():
							gl_entries.append(
								self.get_gl_dict(
									{
										"account": account,
										"against": item.expense_account,
										"cost_center": item.cost_center,
										"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
										"credit": flt(amount["base_amount"]),
										"credit_in_account_currency": flt(amount["amount"]),
										"project": item.project or self.project,
									},
									item=item,
								)
							)

				# sub-contracting warehouse
				if flt(item.rm_supp_cost):
					supplier_warehouse_account = warehouse_account[self.supplier_warehouse]["account"]
					if not supplier_warehouse_account:
						frappe.throw(_("Please set account in Warehouse {0}").format(self.supplier_warehouse))
					gl_entries.append(
						self.get_gl_dict(
							{
								"account": supplier_warehouse_account,
								"against": item.expense_account,
								"cost_center": item.cost_center,
								"project": item.project or self.project,
								"remarks": self.get("remarks") or _("Accounting Entry for Stock"),
								"credit": flt(item.rm_supp_cost),
							},
							warehouse_account[self.supplier_warehouse]["account_currency"],
							item=item,
						)
					)

			else:
				expense_account = (
					item.expense_account
					if (not item.enable_deferred_expense or self.is_return)
					else item.deferred_expense_account
				)

				dummy, amount = self.get_amount_and_base_amount(item, None)

				if provisional_accounting_for_non_stock_items:
					self.make_provisional_gl_entry(gl_entries, item)

				if not self.is_internal_transfer():
					gl_entries.append(
						self.get_gl_dict(
							{
								"account": expense_account,
								"against": self.supplier,
								"debit": amount,
								"cost_center": item.cost_center,
								"project": item.project or self.project,
							},
							account_currency,
							item=item,
						)
					)

					# check if the exchange rate has changed
					if item.get("purchase_receipt") and self.auto_accounting_for_stock:
						if (
							exchange_rate_map[item.purchase_receipt]
							and self.conversion_rate != exchange_rate_map[item.purchase_receipt]
							and item.net_rate == net_rate_map[item.pr_detail]
						):
							discrepancy_caused_by_exchange_rate_difference = (item.qty * item.net_rate) * (
								exchange_rate_map[item.purchase_receipt] - self.conversion_rate
							)

							gl_entries.append(
								self.get_gl_dict(
									{
										"account": expense_account,
										"against": self.supplier,
										"debit": discrepancy_caused_by_exchange_rate_difference,
										"cost_center": item.cost_center,
										"project": item.project or self.project,
									},
									account_currency,
									item=item,
								)
							)
							gl_entries.append(
								self.get_gl_dict(
									{
										"account": self.get_company_default("exchange_gain_loss_account"),
										"against": self.supplier,
										"credit": discrepancy_caused_by_exchange_rate_difference,
										"cost_center": item.cost_center,
										"project": item.project or self.project,
									},
									account_currency,
									item=item,
								)
							)
		if (
			self.auto_accounting_for_stock
			and self.is_opening == "No"
			and item.item_code in stock_items
			and item.item_tax_amount
		):
			# Post reverse entry for Stock-Received-But-Not-Billed if it is booked in Purchase Receipt
			if item.purchase_receipt and valuation_tax_accounts:
				negative_expense_booked_in_pr = frappe.db.sql(
					"""select name from `tabGL Entry`
                        where voucher_type='Purchase Receipt' and voucher_no=%s and account in %s""",
					(item.purchase_receipt, valuation_tax_accounts),
				)

				stock_rbnb = (
					self.get_company_default("asset_received_but_not_billed")
					if item.is_fixed_asset
					else self.stock_received_but_not_billed
				)

				if not negative_expense_booked_in_pr:
					gl_entries.append(
						self.get_gl_dict(
							{
								"account": stock_rbnb,
								"against": self.supplier,
								"debit": flt(item.item_tax_amount, item.precision("item_tax_amount")),
								"remarks": self.remarks or _("Accounting Entry for Stock"),
								"cost_center": self.cost_center,
								"project": item.project or self.project,
							},
							item=item,
						)
					)

					self.negative_expense_to_be_booked += flt(
						item.item_tax_amount, item.precision("item_tax_amount")
					)

		if item.is_fixed_asset and item.landed_cost_voucher_amount:
			self.update_gross_purchase_amount_for_linked_assets(item)


def asset_update_gross_purchase_amount_for_linked_assets(self, item):
	assets = frappe.db.get_all(
		"Asset",
		filters={"purchase_invoice": self.name, "item_code": item.item_code},
		fields=["name", "asset_quantity"],
	)
	for asset in assets:
		purchase_amount = flt(item.valuation_rate) * asset.asset_quantity
		frappe.db.set_value(
			"Asset",
			asset.name,
			{
				"gross_purchase_amount": purchase_amount,
				"purchase_amount": purchase_amount,
			},
		)
