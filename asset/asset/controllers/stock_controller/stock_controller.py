from erpnext.controllers.stock_controller import StockController

from asset.asset.controllers.stock_controller.override.bundle_using_old_serial_batch import (
	asset_make_bundle_using_old_serial_batch_fields,
)
from asset.asset.controllers.stock_controller.override.make_gl_entries import asset_make_gl_entries


class AssetStockController(StockController):
	def make_gl_entries(self, gl_entries=None, from_repost=False, via_landed_cost_voucher=False):
		asset_make_gl_entries(self, gl_entries=None, from_repost=False, via_landed_cost_voucher=False)

	def make_bundle_using_old_serial_batch_fields(
		self, table_name=None, via_landed_cost_voucher=False
	):
		asset_make_bundle_using_old_serial_batch_fields(
			self, table_name=None, via_landed_cost_voucher=False
		)
