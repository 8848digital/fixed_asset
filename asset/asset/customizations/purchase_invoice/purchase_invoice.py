import frappe
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice

from asset.asset.customizations.purchase_invoice.override.make_item_gl_entries import (
	asset_make_item_gl_entries,
	asset_update_gross_purchase_amount_for_linked_assets,
)
from asset.asset.customizations.purchase_invoice.override.make_purchase_receipt import (
	asset_make_purchase_receipt,
)
from asset.asset.customizations.purchase_invoice.override.set_expense_account import (
	asset_set_expense_account,
)
from asset.asset.doctype.asset.asset import is_cwip_accounting_enabled


class AssetPurchaseInvoice(PurchaseInvoice):
	def set_expense_account(self, for_validate=False):
		asset_set_expense_account(self, for_validate=False)

	def make_item_gl_entries(self, gl_entries):
		asset_make_item_gl_entries(self, gl_entries)

	def update_gross_purchase_amount_for_linked_assets(self, item):
		asset_update_gross_purchase_amount_for_linked_assets(self, item)

	def check_asset_cwip_enabled(self):
		# Check if there exists any item with cwip accounting enabled in it's asset category
		for item in self.get("items"):
			if item.item_code and item.is_fixed_asset:
				asset_category = frappe.get_cached_value("Item", item.item_code, "asset_category")
				if is_cwip_accounting_enabled(asset_category):
					return 1
		return 0


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	asset_make_purchase_receipt(source_name, target_doc=None)
