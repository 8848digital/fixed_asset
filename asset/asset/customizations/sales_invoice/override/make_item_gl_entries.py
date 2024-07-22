import frappe
from frappe import _
from frappe.utils import cint, flt, get_link_to_form

import erpnext
from erpnext.accounts.utils import get_account_currency
from asset.asset.doctype.asset.depreciation import (
	depreciate_asset,
	get_gl_entries_on_asset_disposal,
	get_gl_entries_on_asset_regain,
	reset_depreciation_schedule,
	reverse_depreciation_entry_made_after_disposal,
)
from asset.asset.doctype.asset_activity.asset_activity import add_asset_activity
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_gl_entries


def asset_make_item_gl_entries(self, gl_entries):
    # income account gl entries
    enable_discount_accounting = cint(
        frappe.db.get_single_value("Selling Settings", "enable_discount_accounting")
    )

    for item in self.get("items"):
        if flt(item.base_net_amount, item.precision("base_net_amount")):
            if item.is_fixed_asset:
                asset = get_asset(self, item)

                if self.is_return:
                    fixed_asset_gl_entries = get_gl_entries_on_asset_regain(
                        asset,
                        item.base_net_amount,
                        item.finance_book,
                        self.get("doctype"),
                        self.get("name"),
                        self.get("posting_date"),
                    )
                    asset.db_set("disposal_date", None)
                    add_asset_activity(asset.name, _("Asset returned"))

                    if asset.calculate_depreciation:
                        posting_date = frappe.db.get_value(
                            "Sales Invoice", self.return_against, "posting_date"
                        )
                        reverse_depreciation_entry_made_after_disposal(asset, posting_date)
                        notes = _(
                            "This schedule was created when Asset {0} was returned through Sales Invoice {1}."
                        ).format(
                            get_link_to_form(asset.doctype, asset.name),
                            get_link_to_form(self.doctype, self.get("name")),
                        )
                        reset_depreciation_schedule(asset, self.posting_date, notes)
                        asset.reload()

                else:
                    if asset.calculate_depreciation:
                        notes = _(
                            "This schedule was created when Asset {0} was sold through Sales Invoice {1}."
                        ).format(
                            get_link_to_form(asset.doctype, asset.name),
                            get_link_to_form(self.doctype, self.get("name")),
                        )
                        depreciate_asset(asset, self.posting_date, notes)
                        asset.reload()

                    fixed_asset_gl_entries = get_gl_entries_on_asset_disposal(
                        asset,
                        item.base_net_amount,
                        item.finance_book,
                        self.get("doctype"),
                        self.get("name"),
                        self.get("posting_date"),
                    )
                    asset.db_set("disposal_date", self.posting_date)
                    add_asset_activity(asset.name, _("Asset sold"))

                for gle in fixed_asset_gl_entries:
                    gle["against"] = self.customer
                    gl_entries.append(self.get_gl_dict(gle, item=item))

                set_asset_status(self, asset)

            else:
                # Do not book income for transfer within same company
                if not self.is_internal_transfer():
                    income_account = (
                        item.income_account
                        if (not item.enable_deferred_revenue or self.is_return)
                        else item.deferred_revenue_account
                    )

                    amount, base_amount = self.get_amount_and_base_amount(
                        item, enable_discount_accounting
                    )

                    account_currency = get_account_currency(income_account)
                    gl_entries.append(
                        self.get_gl_dict(
                            {
                                "account": income_account,
                                "against": self.customer,
                                "credit": flt(base_amount, item.precision("base_net_amount")),
                                "credit_in_account_currency": (
                                    flt(base_amount, item.precision("base_net_amount"))
                                    if account_currency == self.company_currency
                                    else flt(amount, item.precision("net_amount"))
                                ),
                                "cost_center": item.cost_center,
                                "project": item.project or self.project,
                            },
                            account_currency,
                            item=item,
                        )
                    )

    # expense account gl entries
    if cint(self.update_stock) and erpnext.is_perpetual_inventory_enabled(self.company):
        gl_entries += get_gl_entries(self)


def get_asset(self, item):
    if item.get("asset"):
        asset = frappe.get_doc("Asset", item.asset)
    else:
        frappe.throw(
            _("Row #{0}: You must select an Asset for Item {1}.").format(item.idx, item.item_name),
            title=_("Missing Asset"),
        )

    self.check_finance_books(item, asset)
    return asset

	
def set_asset_status(self, asset):
    if self.is_return:
        asset.set_status()
    else:
        asset.set_status("Sold" if self.docstatus == 1 else None)