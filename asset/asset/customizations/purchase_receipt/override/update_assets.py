import frappe
from frappe.utils import flt


def asset_update_assets(self, item, valuation_rate):
    assets = frappe.db.get_all(
        "Asset",
        filters={"purchase_receipt": self.name, "item_code": item.item_code},
        fields=["name", "asset_quantity"],
    )

    for asset in assets:
        purchase_amount = flt(valuation_rate) * asset.asset_quantity
        frappe.db.set_value(
            "Asset",
            asset.name,
            {
                "gross_purchase_amount": purchase_amount,
                "purchase_amount": purchase_amount,
            },
        )