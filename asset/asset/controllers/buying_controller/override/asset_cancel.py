import frappe
from frappe import _


def update_fixed_asset(self, field, delete_asset=False):
	for d in self.get("items"):
		if d.is_fixed_asset:
			is_auto_create_enabled = frappe.db.get_value("Item", d.item_code, "auto_create_assets")
			assets = frappe.db.get_all("Asset", filters={field: self.name, "item_code": d.item_code})

			for asset in assets:
				asset = frappe.get_doc("Asset", asset.name)
				if delete_asset and is_auto_create_enabled:
					# need to delete movements to delete assets otherwise throws link exists error
					movements = frappe.db.sql(
						"""SELECT asm.name
                        FROM `tabAsset Movement` asm, `tabAsset Movement Item` asm_item
                        WHERE asm_item.parent=asm.name and asm_item.asset=%s""",
						asset.name,
						as_dict=1,
					)
					for movement in movements:
						frappe.delete_doc("Asset Movement", movement.name, force=1)
					frappe.delete_doc("Asset", asset.name, force=1)
					continue

				if self.docstatus == 2:
					if asset.docstatus == 2:
						continue
					if asset.docstatus == 0:
						asset.set(field, None)
						asset.supplier = None
					if asset.docstatus == 1 and delete_asset:
						frappe.throw(
							_(
								"Cannot cancel this document as it is linked with submitted asset {0}. Please cancel it to continue."
							).format(frappe.utils.get_link_to_form("Asset", asset.name))
						)

				asset.flags.ignore_validate_update_after_submit = True
				asset.flags.ignore_mandatory = True
				if asset.docstatus == 0:
					asset.flags.ignore_validate = True

				asset.save()


def delete_linked_asset(self):
	if self.doctype == "Purchase Invoice" and not self.get("update_stock"):
		return

	asset_movement = frappe.db.get_value("Asset Movement", {"reference_name": self.name}, "name")
	frappe.delete_doc("Asset Movement", asset_movement, force=1)
