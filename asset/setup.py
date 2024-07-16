import os

import json

import frappe
from frappe import _
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_migrate():
	create_custom_fields()
	create_property_setter()


def after_install():
	create_custom_fields()
	create_property_setter()


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
			args = json.load(f)
			if isinstance(args.get("value"), list):
				args["value"] = json.dumps(args["value"])
			make_property_setter(args, is_system_generated=False)


def delete_custom_fields():
	print("Removing Custom Fields....")
	module_list = frappe.get_module_list("asset")
	cfs = frappe.db.get_values("Custom Field", filters={"module": ["in", module_list]})
	for cf in cfs:
		frappe.delete_doc("Custom Field", cf[0])
