from erpnext.stock.serial_batch_bundle import SerialBatchBundle

class AssetSerialBatchBundle(SerialBatchBundle):
	@property
	def child_doctype(self):
		child_doctype = self.sle.voucher_type + " Item"

		if self.sle.voucher_type == "Subcontracting Receipt" and self.sle.dependant_sle_voucher_detail_no:
			child_doctype = "Subcontracting Receipt Supplied Item"

		if self.sle.voucher_type == "Stock Entry":
			child_doctype = "Stock Entry Detail"

		if self.sle.voucher_type == "Asset Capitalization":
			child_doctype = "Asset Capitalization Stock Item"

		if self.sle.voucher_type == "Asset Repair":
			child_doctype = "Asset Repair Consumed Item"

		return child_doctype