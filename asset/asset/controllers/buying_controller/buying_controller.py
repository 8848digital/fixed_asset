import frappe
from erpnext.buying.utils import update_last_purchase_rate, validate_for_items
from erpnext.controllers.buying_controller import BuyingController
from frappe import _

from asset.asset.controllers.buying_controller.override.asset_cancel import (
	delete_linked_asset,
	update_fixed_asset,
)
from asset.asset.controllers.buying_controller.override.process_fixed_asset import (
	process_fixed_asset,
)
from asset.asset.controllers.buying_controller.override.validate_asset import (
	update_valuation_rate,
	validate_asset_return,
	validate_stock_or_nonstock_items,
)


class AssetBuyingController(BuyingController):
	def validate(self):
		self.set_rate_for_standalone_debit_note()

		super(BuyingController, self).validate()
		if getattr(self, "supplier", None) and not self.supplier_name:
			self.supplier_name = frappe.db.get_value("Supplier", self.supplier, "supplier_name")

		self.validate_items()
		self.set_qty_as_per_stock_uom()
		validate_stock_or_nonstock_items(self)
		self.validate_warehouse()
		self.validate_from_warehouse()
		self.set_supplier_address()
		validate_asset_return(self)
		self.validate_auto_repeat_subscription_dates()
		self.create_package_for_transfer()

		if self.doctype == "Purchase Invoice":
			self.validate_purchase_receipt_if_update_stock()

		if self.doctype == "Purchase Receipt" or (
			self.doctype == "Purchase Invoice" and self.update_stock
		):
			# self.validate_purchase_return()
			self.validate_rejected_warehouse()
			self.validate_accepted_rejected_qty()
			validate_for_items(self)

			# sub-contracting
			self.validate_for_subcontracting()
			if self.get("is_old_subcontracting_flow"):
				self.create_raw_materials_supplied()
			self.set_landed_cost_voucher_amount()

		if self.doctype in ("Purchase Receipt", "Purchase Invoice"):
			update_valuation_rate(self)
			self.set_serial_and_batch_bundle()

	def on_submit(self):
		if self.get("is_return"):
			return

		if self.doctype in ["Purchase Receipt", "Purchase Invoice"]:
			process_fixed_asset(self)

		if self.doctype in ["Purchase Order", "Purchase Receipt"] and not frappe.db.get_single_value(
			"Buying Settings", "disable_last_purchase_rate"
		):
			update_last_purchase_rate(self, is_submit=1)

	def on_cancel(self):
		super(BuyingController, self).on_cancel()
		if self.get("is_return"):
			return

		if self.doctype in ["Purchase Order", "Purchase Receipt"] and not frappe.db.get_single_value(
			"Buying Settings", "disable_last_purchase_rate"
		):
			update_last_purchase_rate(self, is_submit=0)

		if self.doctype in ["Purchase Receipt", "Purchase Invoice"]:
			field = "purchase_invoice" if self.doctype == "Purchase Invoice" else "purchase_receipt"

			delete_linked_asset(self)
			update_fixed_asset(self, field, delete_asset=True)
