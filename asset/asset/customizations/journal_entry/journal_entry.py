import frappe

from asset.asset.customizations.journal_entry.doc_events.unlink_asset_reference import (
	unlink_asset_reference,
)
from asset.asset.customizations.journal_entry.doc_events.update_asset_value import (
	update_asset_value,
)
from asset.asset.customizations.journal_entry.doc_events.update_booked_depreciation import (
	update_booked_depreciation,
)


def on_submit(self, method=None):
	update_asset_value(self)
	update_booked_depreciation(self)


def on_cancel(self, method=None):
	unlink_asset_reference(self)
	unlink_asset_adjustment_entry(self)
	update_booked_depreciation(self, 1)


def unlink_asset_adjustment_entry(self):
	frappe.db.sql(
		""" update `tabAsset Value Adjustment`
        set journal_entry = null where journal_entry = %s""",
		self.name,
	)
