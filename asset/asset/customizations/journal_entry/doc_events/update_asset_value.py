import frappe


def update_asset_value(self):
    if self.flags.planned_depr_entry or self.voucher_type != "Depreciation Entry":
        return

    for d in self.get("accounts"):
        if (
            d.reference_type == "Asset"
            and d.reference_name
            and d.account_type == "Depreciation"
            and d.debit
        ):
            asset = frappe.get_doc("Asset", d.reference_name)

            if asset.calculate_depreciation:
                fb_idx = 1
                if self.finance_book:
                    for fb_row in asset.get("finance_books"):
                        if fb_row.finance_book == self.finance_book:
                            fb_idx = fb_row.idx
                            break
                fb_row = asset.get("finance_books")[fb_idx - 1]
                fb_row.value_after_depreciation -= d.debit
                fb_row.db_update()
            else:
                asset.db_set("value_after_depreciation", asset.value_after_depreciation - d.debit)

            asset.set_status()