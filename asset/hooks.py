app_name = "asset"
app_title = "Asset"
app_publisher = "8848 Digital"
app_description = "Asset"
app_email = "sibi@8848digital.com"
app_license = "mit"
required_apps = ["frappe", "erpnext"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/asset/css/asset.css"
# app_include_js = "/assets/asset/js/asset.js"

# include js, css files in header of web template
# web_include_css = "/assets/asset/css/asset.css"
# web_include_js = "/assets/asset/js/asset.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "asset/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Company": "asset/customizations/company/company.js",
	"Item": "asset/customizations/item/item.js",
	"Purchase Receipt": "asset/customizations/purchase_receipt/purchase_receipt.js",
	"Purchase Invoice": "asset/customizations/purchase_invoice/purchase_invoice.js",
	"Serial and Batch Bundle": "asset/customizations/serial_and_batch_bundle/serial_and_batch_bundle.js",
	"Sales Invoice": "asset/customizations/sales_invoice/sales_invoice.js",
    "Journal Entry": "asset/customizations/journal_entry/journal_entry.js",
    "Product Bundle": "asset/customizations/product_bundle/product_bundle.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "asset/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "asset.utils.jinja_methods",
# 	"filters": "asset.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "asset.install.before_install"
after_install = "asset.install.after_install"
after_migrate = "asset.setup.after_migrate"

# Uninstallation
# ------------

before_uninstall = "asset.uninstall.before_uninstall"
# after_uninstall = "asset.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "asset.utils.before_app_install"
# after_app_install = "asset.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "asset.utils.before_app_uninstall"
# after_app_uninstall = "asset.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "asset.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Purchase Receipt": "asset.asset.customizations.purchase_receipt.purchase_receipt.AssetPurchaseReceipt",
	"Purchase Invoice": "asset.asset.customizations.purchase_invoice.purchase_invoice.AssetPurchaseInvoice",
	"Landed Cost Voucher": "asset.asset.customizations.landed_cost_voucher.landed_cost_voucher.AssetLandedCostVoucher",
	"Serial and Batch Bundle": "asset.asset.customizations.serial_and_batch_bundle.serial_and_batch_bundle.AssetSerialandBatchBundle",
}

# Document Events
# ---------------
# Hook on document methods and events
period_closing_doctypes = [
	"Asset",
	"Asset Capitalization",
	"Asset Repair"
]

doc_events = {
    tuple(period_closing_doctypes): {
		"validate": "erpnext.accounts.doctype.accounting_period.accounting_period.validate_accounting_period_on_doc_save",
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
    "GL Entry": {"validate":"asset.asset.customizations.gl_entry.gl_entry.validate"}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"asset.tasks.all"
	# ],
	"daily": [
		"asset.asset.doctype.asset.asset.update_maintenance_status",
		"asset.asset.doctype.asset.asset.make_post_gl_entry",
		"asset.asset.doctype.asset_maintenance_log.asset_maintenance_log.update_asset_maintenance_log_status",
	],
	# "hourly": [
	# 	"asset.tasks.hourly"
	# ],
	# "weekly": [
	# 	"asset.tasks.weekly"
	# ],
	"daily_long": [
		"asset.asset.doctype.asset.depreciation.post_depreciation_entries",
	],
	# "monthly": [
	# 	"asset.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "asset.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_receipt",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_invoice",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice_from_portal": "asset.asset.customizations.purchase_order.purchase_order.make_purchase_invoice_from_portal",
	"erpnext.accounts.doctype.purchase_invoice.purchase_invoice.make_purchase_receipt": "asset.asset.customizations.purchase_invoice.purchase_invoice.make_purchase_receipt",
    "erpnext.selling.page.point_of_sale.point_of_sale.get_items": "asset.asset.customizations.point_of_sale.point_of_sale.get_items",
    "erpnext.stock.doctype.material_request.material_request.make_purchase_order": "asset.asset.customizations.material_request.material_request.make_purchase_order",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
override_doctype_dashboards = {
	"Purchase Receipt": "asset.asset.customizations.purchase_receipt.purchase_receipt_dashboard.get_dashboard_for_purchase_receipt",
	"Purchase Invoice": "asset.asset.customizations.purchase_invoice.purchase_invoice_dashboard.get_dashboard_for_purchase_invoice",
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["asset.utils.before_request"]
# after_request = ["asset.utils.after_request"]

# Job Events
# ----------
# before_job = ["asset.utils.before_job"]
# after_job = ["asset.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"asset.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

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
