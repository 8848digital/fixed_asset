import frappe
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
from frappe import _
from frappe.query_builder import DocType


def asset_update_rate_in_serial_no_for_non_asset_items(self, receipt_document):
	for item in receipt_document.get("items"):
		if not item.is_fixed_asset and item.serial_no:
			serial_nos = get_serial_nos(item.serial_no)
			if serial_nos:
				SerialNo = DocType("Serial No")
				valuation_rate = item.valuation_rate
				serial_nos_list = serial_nos
				query = (
					frappe.qb.update(SerialNo)
					.set(SerialNo.purchase_rate, valuation_rate)
					.where(SerialNo.name.isin(serial_nos_list))
				)
				query.run()
