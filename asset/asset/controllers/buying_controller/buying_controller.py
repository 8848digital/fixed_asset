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
)


def validate(self, method=None):
	validate_asset_return(self)
	if self.doctype in ("Purchase Receipt", "Purchase Invoice"):
		update_valuation_rate(self)


def on_submit(self, method=None):
	if self.doctype in ["Purchase Receipt", "Purchase Invoice"]:
		process_fixed_asset(self)


def on_cancel(self, method=None):
	if self.doctype in ["Purchase Receipt", "Purchase Invoice"]:
		field = "purchase_invoice" if self.doctype == "Purchase Invoice" else "purchase_receipt"

		delete_linked_asset(self)
		update_fixed_asset(self, field, delete_asset=True)
