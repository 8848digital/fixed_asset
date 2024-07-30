__version__ = "0.0.1"

from erpnext.controllers.buying_controller import BuyingController
from erpnext.controllers.stock_controller import StockController
from erpnext.stock.serial_batch_bundle import SerialBatchBundle

from asset.asset.controllers.buying_controller.buying_controller import AssetBuyingController
from asset.asset.controllers.stock_controller.stock_controller import AssetStockController
from asset.asset.customizations.serial_and_batch_bundle.serial_batch_bundle import (
	AssetSerialBatchBundle,
)

BuyingController.validate = AssetBuyingController.validate
BuyingController.on_submit = AssetBuyingController.on_submit
BuyingController.on_cancel = AssetBuyingController.on_cancel
StockController.make_gl_entries = AssetStockController.make_gl_entries
StockController.make_bundle_using_old_serial_batch_fields = (
	AssetStockController.make_bundle_using_old_serial_batch_fields
)
SerialBatchBundle.child_doctype = AssetSerialBatchBundle.child_doctype
