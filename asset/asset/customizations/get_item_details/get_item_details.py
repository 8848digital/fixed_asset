import frappe
from erpnext.setup.doctype.brand.brand import get_brand_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.get_item_details import (
	_get_item_details,
	get_basic_details,
	get_default_expense_account,
	process_args,
)


@frappe.whitelist()
def get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
	args = process_args(args)
	item = frappe.get_cached_doc("Item", args.item_code)
	out = get_basic_details(args, item, overwrite_warehouse)

	if item.is_fixed_asset:
		expense_account = None
		from asset.asset.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled

		if is_cwip_accounting_enabled(item.asset_category):
			expense_account = get_asset_account(
				"capital_work_in_progress_account",
				asset_category=item.asset_category,
				company=args.company,
			)
		elif args.get("doctype") in (
			"Purchase Invoice",
			"Purchase Receipt",
			"Purchase Order",
			"Material Request",
		):
			from asset.asset.doctype.asset_category.asset_category import get_asset_category_account

			expense_account = get_asset_category_account(
				fieldname="fixed_asset_account", item=args.item_code, company=args.company
			)

		item_defaults = get_item_defaults(item.name, args.company)
		item_group_defaults = get_item_group_defaults(item.name, args.company)
		brand_defaults = get_brand_defaults(item.name, args.company)

		out.update(
			{
				"expense_account": expense_account
				or get_default_expense_account(args, item_defaults, item_group_defaults, brand_defaults),
				"is_fixed_asset": item.is_fixed_asset,
			}
		)
	return _get_item_details(args, out, doc, for_validate, overwrite_warehouse)
