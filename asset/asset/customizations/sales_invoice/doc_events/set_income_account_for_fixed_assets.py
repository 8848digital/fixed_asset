from asset.asset.doctype.asset.depreciation import get_disposal_account_and_cost_center

def set_income_account_for_fixed_assets(self):
    for item in self.items:
        set_income_account_for_fixed_asset(item, self.company)


def set_income_account_for_fixed_asset(self, company: str):
    """Set income account for fixed asset item based on company's disposal account and cost center."""
    if not self.is_fixed_asset:
        return

    disposal_account, depreciation_cost_center = get_disposal_account_and_cost_center(company)

    self.income_account = disposal_account
    if not self.cost_center:
        self.cost_center = depreciation_cost_center