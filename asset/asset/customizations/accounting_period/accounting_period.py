from erpnext.accounts.doctype.accounting_period.accounting_period import validate_accounting_period


def validate_accounting_period_on_doc_save(doc, method=None):
	if doc.doctype == "Bank Clearance":
		return
	elif doc.doctype == "Asset":
		if doc.is_existing_asset:
			return
		else:
			date = doc.available_for_use_date
	elif doc.doctype == "Asset Repair":
		date = doc.completion_date
	else:
		date = doc.posting_date

	validate_accounting_period(doc, date)
