from frappe import _


def get_dashboard_for_purchase_invoice(data):
	data["transactions"].append({"label": _("Asset"), "items": ["Asset"]})

	return data
