import frappe
from frappe import _


def validate(self, method=None):
	validate_main_item(self)


def validate_main_item(self):
	if frappe.db.get_value("Item", self.new_item_code, "is_fixed_asset"):
		frappe.throw(_("Parent Item {0} must not be a Fixed Asset").format(self.new_item_code))


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_new_item_code(doctype, txt, searchfield, start, page_len, filters):
	product_bundles = frappe.db.get_list("Product Bundle", {"disabled": 0}, pluck="name")

	item = frappe.qb.DocType("Item")
	query = (
		frappe.qb.from_(item)
		.select(item.item_code, item.item_name)
		.where(
			(item.is_stock_item == 0) & (item.is_fixed_asset == 0) & (item[searchfield].like(f"%{txt}%"))
		)
		.limit(page_len)
		.offset(start)
	)

	if product_bundles:
		query = query.where(item.name.notin(product_bundles))

	return query.run()
