import frappe
from frappe import _

from asset.asset.customizations.company.doc_events.on_update_function import (
	on_update_set_default_accounts,
)


def on_update(self, event):
	on_update_set_default_accounts(self)
