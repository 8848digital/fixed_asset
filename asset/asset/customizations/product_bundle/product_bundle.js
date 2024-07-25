frappe.ui.form.on("Product Bundle", {
	refresh: function (frm) {
		frm.toggle_enable("new_item_code", frm.is_new());
		frm.set_query("new_item_code", () => {
			return {
				query: "asset.asset.customizations.product_bundle.product_bundle.get_new_item_code",
			};
		});
	},
});
