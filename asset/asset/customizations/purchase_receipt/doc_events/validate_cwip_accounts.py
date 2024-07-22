from asset.asset.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from asset.asset.doctype.asset_category.asset_category import get_asset_category_account


def validate_cwip_accounts(self):
	for item in self.get("items"):
		if item.is_fixed_asset and is_cwip_accounting_enabled(item.asset_category):
			# check cwip accounts before making auto assets
			# Improves UX by not giving messages of "Assets Created" before throwing error of not finding arbnb account
			self.get_company_default("asset_received_but_not_billed")
			get_asset_account(
				"capital_work_in_progress_account",
				asset_category=item.asset_category,
				company=self.company,
			)
			break