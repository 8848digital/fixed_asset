import frappe
from frappe.utils import cint

import erpnext
from erpnext.accounts.general_ledger import (
	make_gl_entries,
	make_reverse_gl_entries,
)
from erpnext.stock import get_warehouse_account_map


def asset_make_gl_entries(self, gl_entries=None, from_repost=False, via_landed_cost_voucher=False):
    if self.docstatus == 2:
        make_reverse_gl_entries(voucher_type=self.doctype, voucher_no=self.name)

    provisional_accounting_for_non_stock_items = cint(
        frappe.get_cached_value(
            "Company", self.company, "enable_provisional_accounting_for_non_stock_items"
        )
    )

    is_asset_pr = any(d.get("is_fixed_asset") for d in self.get("items"))

    if (
        cint(erpnext.is_perpetual_inventory_enabled(self.company))
        or provisional_accounting_for_non_stock_items
        or is_asset_pr
    ):
        warehouse_account = get_warehouse_account_map(self.company)

        if self.docstatus == 1:
            if not gl_entries:
                gl_entries = (
                    self.get_gl_entries(warehouse_account, via_landed_cost_voucher)
                    if self.doctype == "Purchase Receipt"
                    else self.get_gl_entries(warehouse_account)
                )
            make_gl_entries(gl_entries, from_repost=from_repost)