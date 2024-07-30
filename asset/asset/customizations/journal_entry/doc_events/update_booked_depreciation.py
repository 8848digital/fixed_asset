import frappe


def update_booked_depreciation(self, cancel=0):
	for d in self.get("accounts"):
		if (
			self.voucher_type == "Depreciation Entry"
			and d.reference_type == "Asset"
			and d.reference_name
			and frappe.get_cached_value("Account", d.account, "root_type") == "Expense"
			and d.debit
		):
			asset = frappe.get_doc("Asset", d.reference_name)
			for fb_row in asset.get("finance_books"):
				if fb_row.finance_book == self.finance_book:
					if cancel:
						fb_row.total_number_of_booked_depreciations -= 1
					else:
						fb_row.total_number_of_booked_depreciations += 1
					fb_row.db_update()
					break
