import json

import frappe
from frappe import _, msgprint, scrub
from frappe.utils import comma_and, cstr, flt, fmt_money, formatdate, get_link_to_form, nowdate

import erpnext
from erpnext.accounts.deferred_revenue import get_deferred_booking_accounts
from erpnext.accounts.doctype.invoice_discounting.invoice_discounting import (
	get_party_account_based_on_invoice_discounting,
)
from erpnext.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	validate_docs_for_deferred_accounting,
	validate_docs_for_voucher_types,
)
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
	get_party_tax_withholding_details,
)
from erpnext.accounts.party import get_party_account
from erpnext.accounts.utils import (
	cancel_exchange_gain_loss_journal,
	get_account_currency,
	get_balance_on,
	get_stock_accounts,
	get_stock_and_account_balance,
)
from asset.asset.doctype.asset_depreciation_schedule.asset_depreciation_schedule import (
	get_depr_schedule,
)
from erpnext.controllers.accounts_controller import AccountsController


from asset.asset.customizations.journal_entry.doc_events.update_asset_value import update_asset_value
from asset.asset.customizations.journal_entry.doc_events.unlink_asset_reference import unlink_asset_reference
from asset.asset.customizations.journal_entry.doc_events.update_booked_depreciation import update_booked_depreciation


def on_submit(self, event):
    update_asset_value(self)
    update_booked_depreciation(self)


def on_cancel(self, event):
    unlink_asset_reference(self)
    unlink_asset_adjustment_entry(self)
    update_booked_depreciation(self, 1)


def unlink_asset_adjustment_entry(self):
    frappe.db.sql(
        """ update `tabAsset Value Adjustment`
        set journal_entry = null where journal_entry = %s""",
        self.name,
    )