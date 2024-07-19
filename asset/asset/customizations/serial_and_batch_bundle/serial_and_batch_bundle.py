import frappe
from erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle import (
	SerialandBatchBundle,
)

from asset.asset.customizations.serial_and_batch_bundle.override.child_table import (
	asset_child_table,
)


class AssetSerialandBatchBundle(SerialandBatchBundle):
	@property
	def child_table(self):
		asset_child_table(self)
