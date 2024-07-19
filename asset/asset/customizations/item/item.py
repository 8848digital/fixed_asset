import frappe
from frappe import _, bold

from asset.asset.customizations.item.doc_events.validate_asset_item import (
	validate_fixed_asset,
	validate_item_type,
)


def validate(self, event):
	validate_item_type(self)
	validate_fixed_asset(self)


def onload(self, event):
	self.set_onload("asset_naming_series", get_asset_naming_series())


@frappe.whitelist()
def get_asset_naming_series():
	from asset.asset.doctype.asset.asset import get_asset_naming_series

	return get_asset_naming_series()
