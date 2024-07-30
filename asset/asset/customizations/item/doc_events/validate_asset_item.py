import frappe
from frappe import _, bold


def validate_item_type(self):
	if self.has_serial_no == 1 and self.is_stock_item == 0 and not self.is_fixed_asset:
		frappe.throw(_("'Has Serial No' can not be 'Yes' for non-stock item"))


def validate_fixed_asset(self):
	if self.is_fixed_asset:
		if self.is_stock_item:
			frappe.throw(_("Fixed Asset Item must be a non-stock item."))

		if not self.asset_category:
			frappe.throw(_("Asset Category is mandatory for Fixed Asset item"))

		if self.stock_ledger_created():
			frappe.throw(_("Cannot be a fixed asset item as Stock Ledger is created."))

	if not self.is_fixed_asset:
		asset = frappe.db.get_all("Asset", filters={"item_code": self.name, "docstatus": 1}, limit=1)
		if asset:
			frappe.throw(_('"Is Fixed Asset" cannot be unchecked, as Asset record exists against the item'))
