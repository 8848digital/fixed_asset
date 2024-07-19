import frappe
from frappe import _

from asset.asset.customizations.purchase_order.override.get_mapped_purchase_invoice import (
	get_mapped_purchase_invoice,
)
from asset.asset.customizations.purchase_order.override.make_purchase_receipt import (
	asset_make_purchase_receipt,
)


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	asset_make_purchase_receipt(source_name, target_doc=None)


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	return get_mapped_purchase_invoice(source_name, target_doc)


@frappe.whitelist()
def make_purchase_invoice_from_portal(purchase_order_name):
	doc = get_mapped_purchase_invoice(purchase_order_name, ignore_permissions=True)
	if doc.contact_email != frappe.session.user:
		frappe.throw(_("Not Permitted"), frappe.PermissionError)
	doc.save()
	frappe.db.commit()
	frappe.response["type"] = "redirect"
	frappe.response.location = "/purchase-invoices/" + doc.name
