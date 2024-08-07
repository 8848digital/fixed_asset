from frappe import _


def get_dashboard_for_finance_book(data):
	data["non_standard_fieldnames"].update({"Asset": "default_finance_book"})

	data["transactions"].append({"label": _("Assets"), "items": ["Asset", "Asset Value Adjustment"]})

	return data
