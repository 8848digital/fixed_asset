import erpnext
import frappe
from erpnext.accounts.utils import get_account_currency
from erpnext.controllers.accounts_controller import merge_taxes
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
	PurchaseReceipt,
	get_invoiced_qty_map,
	get_item_account_wise_additional_cost,
	get_returned_qty_map,
	get_stock_value_difference,
)
from frappe import _, throw
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt

from asset.asset.customizations.purchase_receipt.doc_events.validate_cwip_accounts import (
	validate_cwip_accounts,
)
from asset.asset.customizations.purchase_receipt.override.make_item_gl_entries import (
	asset_make_item_gl_entries,
)
from asset.asset.customizations.purchase_receipt.override.make_purchase_invoice import (
	asset_make_purchase_invoice,
)
from asset.asset.customizations.purchase_receipt.override.update_assets import asset_update_assets


class AssetPurchaseReceipt(PurchaseReceipt):
	def make_item_gl_entries(self, gl_entries, warehouse_account=None):
		asset_make_item_gl_entries(self, gl_entries, warehouse_account=None)

	def update_assets(self, item, valuation_rate):
		asset_update_assets(self, item, valuation_rate)


def validate(self, event):
	validate_cwip_accounts(self)


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None, args=None):
	return asset_make_purchase_invoice(source_name, target_doc=None, args=None)
