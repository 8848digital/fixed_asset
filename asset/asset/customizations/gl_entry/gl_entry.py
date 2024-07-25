from asset.asset.customizations.gl_entry.doc_events.validate_cwip_accounts import validate_cwip_accounts

def validate(doc, method= None):
	if not doc.flags.from_repost:
		validate_cwip_accounts(doc)