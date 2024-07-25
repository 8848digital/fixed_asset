import frappe

def asset_make_bundle_using_old_serial_batch_fields(self, table_name=None, via_landed_cost_voucher=False):
    if self.get("_action") == "update_after_submit":
        return

    # To handle test cases
    if frappe.flags.in_test and frappe.flags.use_serial_and_batch_fields:
        return

    if not table_name:
        table_name = "items"

    if self.doctype == "Asset Capitalization":
        table_name = "stock_items"

    for row in self.get(table_name):
        if row.serial_and_batch_bundle and (row.serial_no or row.batch_no):
            self.validate_serial_nos_and_batches_with_bundle(row)

        if not row.serial_no and not row.batch_no and not row.get("rejected_serial_no"):
            continue

        if not row.use_serial_batch_fields and (
            row.serial_no or row.batch_no or row.get("rejected_serial_no")
        ):
            row.use_serial_batch_fields = 1

        if row.use_serial_batch_fields and (
            not row.serial_and_batch_bundle and not row.get("rejected_serial_and_batch_bundle")
        ):
            bundle_details = {
                "item_code": row.get("rm_item_code") or row.item_code,
                "posting_date": self.posting_date,
                "posting_time": self.posting_time,
                "voucher_type": self.doctype,
                "voucher_no": self.name,
                "voucher_detail_no": row.name,
                "company": self.company,
                "is_rejected": 1 if row.get("rejected_warehouse") else 0,
                "use_serial_batch_fields": row.use_serial_batch_fields,
                "via_landed_cost_voucher": via_landed_cost_voucher,
                "do_not_submit": True if not via_landed_cost_voucher else False,
            }

            if row.get("qty") or row.get("consumed_qty") or row.get("stock_qty"):
                self.update_bundle_details(bundle_details, table_name, row)
                self.create_serial_batch_bundle(bundle_details, row)

            if row.get("rejected_qty"):
                self.update_bundle_details(bundle_details, table_name, row, is_rejected=True)
                self.create_serial_batch_bundle(bundle_details, row)