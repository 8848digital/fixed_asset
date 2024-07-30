import frappe


def execute():
	frappe.reload_doc("asset", "doctype", "Location")
	for dt in (
		"Location"
	):
		frappe.reload_doctype(dt)
		frappe.get_doc("DocType", dt).run_module_method("on_doctype_update")