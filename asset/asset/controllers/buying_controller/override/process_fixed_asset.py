import frappe
from frappe import _
from frappe.utils import cint, flt

from asset.asset.controllers.buying_controller.override.validate_asset import get_asset_items


def process_fixed_asset(self):
    if self.doctype == "Purchase Invoice" and not self.update_stock:
        return

    asset_items = get_asset_items(self)
    if asset_items:
        auto_make_assets(self, asset_items)

def auto_make_assets(self, asset_items):
    items_data = get_asset_item_details(asset_items)
    messages = []
    alert = False

    for d in self.items:
        if d.is_fixed_asset:
            item_data = items_data.get(d.item_code)

            if item_data.get("auto_create_assets"):
                # If asset has to be auto created
                # Check for asset naming series
                if item_data.get("asset_naming_series"):
                    created_assets = []
                    if item_data.get("is_grouped_asset"):
                        asset = make_asset(self, d, is_grouped_asset=True)
                        created_assets.append(asset)
                    else:
                        for _qty in range(cint(d.qty)):
                            asset = make_asset(self, d)
                            created_assets.append(asset)

                    if len(created_assets) > 5:
                        # dont show asset form links if more than 5 assets are created
                        messages.append(
                            _("{} Assets created for {}").format(
                                len(created_assets), frappe.bold(d.item_code)
                            )
                        )
                    else:
                        assets_link = list(
                            map(lambda d: frappe.utils.get_link_to_form("Asset", d), created_assets)
                        )
                        assets_link = frappe.bold(",".join(assets_link))

                        is_plural = "s" if len(created_assets) != 1 else ""
                        messages.append(
                            _("Asset{} {assets_link} created for {}").format(
                                is_plural, frappe.bold(d.item_code), assets_link=assets_link
                            )
                        )
                else:
                    frappe.throw(
                        _(
                            "Row {}: Asset Naming Series is mandatory for the auto creation for item {}"
                        ).format(d.idx, frappe.bold(d.item_code))
                    )
            else:
                messages.append(
                    _("Assets not created for {0}. You will have to create asset manually.").format(
                        frappe.bold(d.item_code)
                    )
                )
                alert = True

    for message in messages:
        frappe.msgprint(message, title="Success", indicator="green", alert=alert)

def make_asset(self, row, is_grouped_asset=False):
    if not row.asset_location:
        frappe.throw(_("Row {0}: Enter location for the asset item {1}").format(row.idx, row.item_code))

    item_data = frappe.get_cached_value(
        "Item", row.item_code, ["asset_naming_series", "asset_category"], as_dict=1
    )
    asset_quantity = row.qty if is_grouped_asset else 1
    purchase_amount = flt(row.valuation_rate) * asset_quantity

    asset = frappe.get_doc(
        {
            "doctype": "Asset",
            "item_code": row.item_code,
            "asset_name": row.item_name,
            "naming_series": item_data.get("asset_naming_series") or "AST",
            "asset_category": item_data.get("asset_category"),
            "location": row.asset_location,
            "company": self.company,
            "supplier": self.supplier,
            "purchase_date": self.posting_date,
            "calculate_depreciation": 0,
            "purchase_amount": purchase_amount,
            "gross_purchase_amount": purchase_amount,
            "asset_quantity": asset_quantity,
            "purchase_receipt": self.name if self.doctype == "Purchase Receipt" else None,
            "purchase_invoice": self.name if self.doctype == "Purchase Invoice" else None,
        }
    )

    asset.flags.ignore_validate = True
    asset.flags.ignore_mandatory = True
    asset.set_missing_values()
    asset.db_insert()

    return asset.name


def get_asset_item_details(asset_items):
	asset_items_data = {}
	for d in frappe.get_all(
		"Item",
		fields=["name", "auto_create_assets", "asset_naming_series", "is_grouped_asset"],
		filters={"name": ("in", asset_items)},
	):
		asset_items_data.setdefault(d.name, d)

	return asset_items_data