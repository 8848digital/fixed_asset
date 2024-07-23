__version__ = "0.0.1"

from erpnext.controllers.buying_controller import BuyingController

from asset.asset.controllers.buying_controller.buying_controller import AssetBuyingController

BuyingController.validate = AssetBuyingController.validate
BuyingController.on_submit = AssetBuyingController.on_submit
BuyingController.on_cancel = AssetBuyingController.on_cancel
