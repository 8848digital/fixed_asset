app_name = "asset"
app_title = "Asset"
app_publisher = "8848 Digital"
app_description = "Asset"
app_email = "sibi@8848digital.com"
app_license = "mit"
required_apps = ["frappe", "erpnext"]

app_include_js = "asset.bundle.js"

doctype_js = {
	"Company": "asset/customizations/company/company.js",
	"Item": "asset/customizations/item/item.js",
	"Purchase Receipt": "asset/customizations/purchase_receipt/purchase_receipt.js",
	"Purchase Invoice": "asset/customizations/purchase_invoice/purchase_invoice.js",
	"Serial and Batch Bundle": "asset/customizations/serial_and_batch_bundle/serial_and_batch_bundle.js",
	"Sales Invoice": "asset/customizations/sales_invoice/sales_invoice.js",
	"Journal Entry": "asset/customizations/journal_entry/journal_entry.js",
	"Product Bundle": "asset/customizations/product_bundle/product_bundle.js",
	"BOM": "asset/customizations/bom/bom.js",
}

after_install = "asset.install.after_install"
after_migrate = "asset.setup.after_migrate"

before_uninstall = "asset.uninstall.before_uninstall"

override_doctype_class = {
	"Purchase Receipt": "asset.asset.customizations.purchase_receipt.purchase_receipt.AssetPurchaseReceipt",
	"Purchase Invoice": "asset.asset.customizations.purchase_invoice.purchase_invoice.AssetPurchaseInvoice",
	"Landed Cost Voucher": "asset.asset.customizations.landed_cost_voucher.landed_cost_voucher.AssetLandedCostVoucher",
	"Serial and Batch Bundle": "asset.asset.customizations.serial_and_batch_bundle.serial_and_batch_bundle.AssetSerialandBatchBundle",
	"Sales Invoice": "asset.asset.customizations.sales_invoice.sales_invoice.overrideSalesInvoice",
}

period_closing_doctypes = ["Asset", "Asset Capitalization", "Asset Repair"]
buying_controller_list = ["Purchase Receipt", "Purchase Invoice"]

doc_events = {
	tuple(period_closing_doctypes): {
		"validate": "asset.asset.customizations.accounting_period.accounting_period.validate_accounting_period_on_doc_save",
	},
	tuple(buying_controller_list): {
		"validate": "asset.asset.controllers.buying_controller.buying_controller.validate",
		"on_submit": "asset.asset.controllers.buying_controller.buying_controller.on_submit",
		"on_cancel": "asset.asset.controllers.buying_controller.buying_controller.on_cancel",
	},
	"Company": {
		"on_update": "asset.asset.customizations.company.company.on_update",
	},
	"Item": {
		"validate": "asset.asset.customizations.item.item.validate",
		"onload": "asset.asset.customizations.item.item.onload",
	},
	"Purchase Receipt": {
		"validate": "asset.asset.customizations.purchase_receipt.purchase_receipt.validate"
	},
	"Journal Entry": {
		"on_submit": "asset.asset.customizations.journal_entry.journal_entry.on_submit",
		"on_cancel": "asset.asset.customizations.journal_entry.journal_entry.on_cancel",
	},
	"Sales Invoice": {"validate": "asset.asset.customizations.sales_invoice.sales_invoice.validate"},
	"Product Bundle": {
		"validate": "asset.asset.customizations.product_bundle.product_bundle.validate"
	},
	"GL Entry": {"validate": "asset.asset.customizations.gl_entry.gl_entry.validate"},
}

scheduler_events = {
	"daily": [
		"asset.asset.doctype.asset.asset.update_maintenance_status",
		"asset.asset.doctype.asset.asset.make_post_gl_entry",
		"asset.asset.doctype.asset_maintenance_log.asset_maintenance_log.update_asset_maintenance_log_status",
	],
	"daily_long": [
		"asset.asset.doctype.asset.depreciation.post_depreciation_entries",
	],
}

override_whitelisted_methods = {
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_receipt",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_invoice",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice_from_portal": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_invoice_from_portal",
	"erpnext.accounts.doctype.purchase_invoice.purchase_invoice.make_purchase_receipt": "asset.asset.customizations.purchase_invoice.purchase_invoice.make_purchase_receipt",
	"erpnext.selling.page.point_of_sale.point_of_sale.get_items": "asset.asset.customizations.point_of_sale.point_of_sale.get_items",
	"erpnext.stock.doctype.material_request.material_request.make_purchase_order": "asset.asset.customizations.material_request.material_request.make_purchase_order",
	"erpnext.stock.get_item_details.get_item_details": "asset.asset.customizations.get_item_details.get_item_details.get_item_details",
}

override_doctype_dashboards = {
	"Purchase Receipt": "asset.asset.customizations.purchase_receipt.purchase_receipt_dashboard.get_dashboard_for_purchase_receipt",
	"Purchase Invoice": "asset.asset.customizations.purchase_invoice.purchase_invoice_dashboard.get_dashboard_for_purchase_invoice",
	"Finance Book": "asset.asset.customizations.finance_book.finance_book_dashboard.get_dashboard_for_finance_book",
}

accounting_dimension_doctypes = [
	"Asset",
	"Asset Value Adjustment",
	"Asset Repair",
	"Asset Capitalization",
]

global_search_doctypes = {
	"Default": [
		{"doctype": "Asset", "index": 28},
	],
}
