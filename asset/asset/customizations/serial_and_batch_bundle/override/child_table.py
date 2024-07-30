def asset_child_table(self):
	if self.voucher_type == "Job Card":
		return

	parent_child_map = {
		"Asset Capitalization": "Asset Capitalization Stock Item",
		"Asset Repair": "Asset Repair Consumed Item",
		"Quotation": "Packed Item",
		"Stock Entry": "Stock Entry Detail",
	}

	return (
		parent_child_map[self.voucher_type]
		if self.voucher_type in parent_child_map
		else f"{self.voucher_type} Item"
	)
