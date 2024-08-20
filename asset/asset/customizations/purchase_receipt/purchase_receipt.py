import frappe
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import PurchaseReceipt
from frappe import _

from asset.asset.controllers.buying_controller.override.validate_asset import (
	update_valuation_rate,
	validate_stock_or_nonstock_items,
)
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
		asset_make_item_gl_entries(self, gl_entries, warehouse_account)

	def update_assets(self, item, valuation_rate):
		asset_update_assets(self, item, valuation_rate)

	def validate_stock_or_nonstock_items(self):
		validate_stock_or_nonstock_items(self)

	def update_valuation_rate(self, reset_outgoing_rate=True):
		update_valuation_rate(self, reset_outgoing_rate)


def validate(self, method=None):
	validate_cwip_accounts(self)


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None, args=None):
	return asset_make_purchase_invoice(source_name, target_doc, args)
