from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

from asset.asset.customizations.sales_invoice.doc_events.set_income_account_for_fixed_assets import (
	set_income_account_for_fixed_assets,
)
from asset.asset.customizations.sales_invoice.doc_events.validate_fixed_asset import (
	validate_fixed_asset,
)
from asset.asset.customizations.sales_invoice.override.make_item_gl_entries import (
	asset_make_item_gl_entries,
)


class overrideSalesInvoice(SalesInvoice):
	def make_item_gl_entries(self, gl_entries):
		asset_make_item_gl_entries(self, gl_entries)


def validate(self, event):
	validate_fixed_asset(self)
	set_income_account_for_fixed_assets(self)
