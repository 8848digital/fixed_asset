import frappe
from erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher import LandedCostVoucher

from asset.asset.customizations.landed_cost_voucher.override.get_items_from_pr import (
	asset_get_items_from_purchase_receipts,
)
from asset.asset.customizations.landed_cost_voucher.override.update_landed_cost import (
	asset_update_landed_cost,
)
from asset.asset.customizations.landed_cost_voucher.override.update_rate_non_asset_items import (
	asset_update_rate_in_serial_no_for_non_asset_items,
)


class AssetLandedCostVoucher(LandedCostVoucher):
	def update_landed_cost(self):
		asset_update_landed_cost(self)

	def update_rate_in_serial_no_for_non_asset_items(self, receipt_document):
		asset_update_rate_in_serial_no_for_non_asset_items(self, receipt_document)

	@frappe.whitelist()
	def get_items_from_purchase_receipts(self):
		asset_get_items_from_purchase_receipts(self)
