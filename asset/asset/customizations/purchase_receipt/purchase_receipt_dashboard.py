from frappe import _


def get_dashboard_for_purchase_receipt(data):
	data["non_standard_fieldnames"].update({"Asset": "purchase_receipt"})

	data["transactions"].append({"label": _("Asset"), "items": ["Asset"]})

	return data