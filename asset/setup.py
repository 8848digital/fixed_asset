import json
import os

import frappe
from frappe import _
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_migrate():
	create_custom_fields()
	create_property_setter()


def after_install():
	create_custom_fields()
	create_property_setter()
	run_post_install_patches()


def before_uninstall():
	delete_custom_fields()


def create_custom_fields():
	CUSTOM_FIELDS = {}
	print("Creating/Updating Custom Fields....")
	path = os.path.join(os.path.dirname(__file__), "asset/custom_fields")
	for file in os.listdir(path):
		with open(os.path.join(path, file), "r") as f:
			CUSTOM_FIELDS.update(json.load(f))
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(CUSTOM_FIELDS)


def create_property_setter():
	print("Creating/Updating Property Setter....")
	path = os.path.join(os.path.dirname(__file__), "asset/property_setter")
	for file in os.listdir(path):
		with open(os.path.join(path, file), "r") as f:
			property_setters = json.load(f)
			for doctype, properties in property_setters.items():
				for args in properties:
					if not args.get("doctype"):
						args["doctype"] = doctype
					make_property_setter(**args)


def delete_custom_fields():
	print("Removing Custom Fields....")
	module_list = frappe.get_module_list("asset")
	cfs = frappe.db.get_values("Custom Field", filters={"module": ["in", module_list]})
	for cf in cfs:
		frappe.delete_doc("Custom Field", cf[0])


def get_post_install_patches():
	return (
		"erpnext.patches.v11_0.make_asset_finance_book_against_old_entries",
		"erpnext.patches.v11_0.make_location_from_warehouse",
		"erpnext.patches.v11_0.rename_asset_adjustment_doctype",
		"erpnext.patches.v11_0.merge_land_unit_with_location",
		"erpnext.patches.v12_0.set_cwip_and_delete_asset_settings",
		"erpnext.patches.v13_0.create_accounting_dimensions_for_asset_repair",
		"erpnext.patches.v13_0.update_asset_quantity_field",
		"erpnext.patches.v14_0.create_accounting_dimensions_for_asset_capitalization",
		"erpnext.patches.v14_0.update_total_asset_cost_field",
		"erpnext.patches.v14_0.update_zero_asset_quantity_field",
	)


def run_post_install_patches():
	print("\nPatching Existing Data...")

	POST_INSTALL_PATCHES = get_post_install_patches()
	frappe.flags.in_patch = True

	try:
		for patch in POST_INSTALL_PATCHES:
			patch_name = patch.split(".")[-1]
			if not patch_name:
				continue

			frappe.get_attr(f"asset.patches.post_install.{patch_name}.execute")()
	finally:
		frappe.flags.in_patch = False


from erpnext.controllers.accounts_controller import AccountsController
from erpnext.controllers.stock_controller import StockController
from erpnext.stock.serial_batch_bundle import SerialBatchBundle

from asset.asset.controllers.accounts_controller.accounts_controller import AssetAccountsController
from asset.asset.controllers.stock_controller.stock_controller import AssetStockController
from asset.asset.customizations.serial_and_batch_bundle.serial_batch_bundle import (
	AssetSerialBatchBundle,
)


def apply_patches():
	StockController.make_gl_entries = AssetStockController.make_gl_entries
	StockController.make_bundle_using_old_serial_batch_fields = (
		AssetStockController.make_bundle_using_old_serial_batch_fields
	)
	SerialBatchBundle.child_doctype = AssetSerialBatchBundle.child_doctype
	AccountsController.set_missing_item_details = AssetAccountsController.set_missing_item_details
