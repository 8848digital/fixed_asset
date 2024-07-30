frappe.ui.form.on("Journal Entry", {
	setup: function (frm) {
		frm.ignore_doctypes_on_cancel_all.push(
			"Asset",
			"Asset Movement",
			"Asset Depreciation Schedule"
		);
	},
});
