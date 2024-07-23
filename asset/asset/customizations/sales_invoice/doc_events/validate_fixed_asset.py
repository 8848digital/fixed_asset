import frappe
from frappe import _, throw


def validate_fixed_asset(self):
	for d in self.get("items"):
		if d.is_fixed_asset and d.meta.get_field("asset") and d.asset:
			asset = frappe.get_doc("Asset", d.asset)
			if self.doctype == "Sales Invoice" and self.docstatus == 1:
				if self.update_stock:
					frappe.throw(_("'Update Stock' cannot be checked for fixed asset sale"))

				elif asset.status in ("Scrapped", "Cancelled", "Capitalized", "Decapitalized") or (
					asset.status == "Sold" and not self.is_return
				):
					frappe.throw(
						_("Row #{0}: Asset {1} cannot be submitted, it is already {2}").format(
							d.idx, d.asset, asset.status
						)
					)
