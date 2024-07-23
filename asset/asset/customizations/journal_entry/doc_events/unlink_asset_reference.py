import frappe
from frappe import _

from asset.asset.doctype.asset_depreciation_schedule.asset_depreciation_schedule import (
	get_depr_schedule,
)


def unlink_asset_reference(self):
	for d in self.get("accounts"):
		if (
			self.voucher_type == "Depreciation Entry"
			and d.reference_type == "Asset"
			and d.reference_name
			and frappe.get_cached_value("Account", d.account, "root_type") == "Expense"
			and d.debit
		):
			asset = frappe.get_doc("Asset", d.reference_name)

			if asset.calculate_depreciation:
				je_found = False

				for fb_row in asset.get("finance_books"):
					if je_found:
						break

					depr_schedule = get_depr_schedule(asset.name, "Active", fb_row.finance_book)

					for s in depr_schedule or []:
						if s.journal_entry == self.name:
							s.db_set("journal_entry", None)

							fb_row.value_after_depreciation += d.debit
							fb_row.db_update()

							je_found = True
							break
				if not je_found:
					fb_idx = 1
					if self.finance_book:
						for fb_row in asset.get("finance_books"):
							if fb_row.finance_book == self.finance_book:
								fb_idx = fb_row.idx
								break

					fb_row = asset.get("finance_books")[fb_idx - 1]
					fb_row.value_after_depreciation += d.debit
					fb_row.db_update()
			else:
				asset.db_set("value_after_depreciation", asset.value_after_depreciation + d.debit)
			asset.set_status()
		elif self.voucher_type == "Journal Entry" and d.reference_type == "Asset" and d.reference_name:
			journal_entry_for_scrap = frappe.db.get_value(
				"Asset", d.reference_name, "journal_entry_for_scrap"
			)

			if journal_entry_for_scrap == self.name:
				frappe.throw(
					_("Journal Entry for Asset scrapping cannot be cancelled. Please restore the Asset.")
				)
