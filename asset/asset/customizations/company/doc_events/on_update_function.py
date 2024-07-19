import frappe
from frappe import _


def on_update_set_default_accounts(self):
	if not frappe.db.get_value("Cost Center", {"is_group": 0, "company": self.name}):
		self.db_set("depreciation_cost_center", _("Main") + " - " + self.abbr)
	if not frappe.local.flags.ignore_chart_of_accounts:
		set_default_accounts(self)


def set_default_accounts(self):
	default_accounts = {
		"accumulated_depreciation_account": "Accumulated Depreciation",
		"depreciation_expense_account": "Depreciation",
		"capital_work_in_progress_account": "Capital Work in Progress",
		"asset_received_but_not_billed": "Asset Received But Not Billed",
	}

	if self.update_default_account:
		for default_account in default_accounts:
			self._set_default_account(default_account, default_accounts.get(default_account))

	if not self.disposal_account:
		disposal_acct = frappe.db.get_value(
			"Account",
			{"account_name": _("Gain/Loss on Asset Disposal"), "company": self.name, "is_group": 0},
		)

		self.db_set("disposal_account", disposal_acct)
