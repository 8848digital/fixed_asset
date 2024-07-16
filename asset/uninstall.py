import click

from asset.setup import before_uninstall as remove_custom_fields


def before_uninstall():
	try:
		print("Removing customizations created by the Frappe Asset app...")
		remove_custom_fields()

	except Exception as e:
		click.secho(
			"Removing Customizations for Frappe Asset failed due to an error."
			" Please try again.",
			fg="bright_red",
		)
		raise e

	click.secho("Frappe Asset app customizations have been removed successfully...", fg="green")
