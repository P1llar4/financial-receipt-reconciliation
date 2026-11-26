"""Reconcile the synthetic payment and email fixtures; write CSV to stdout."""
import csv
import mailbox
import sys
from collections import defaultdict
from contextlib import closing
from decimal import Decimal
from pathlib import Path

SAMPLES = Path(__file__).resolve().parent / "samples"


def main():
    records = defaultdict(lambda: {"payment": [], "receipt": []})
    with (SAMPLES / "payments.csv").open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            records[row["order_id"]]["payment"].append(Decimal(row["amount_usd"]))

    with closing(mailbox.mbox(SAMPLES / "receipts.mbox", create=False)) as inbox:
        for message in inbox:
            order = message["X-Demo-Order"]
            records[order]["receipt"].append(Decimal(message["X-Demo-Total-USD"]))

    report = csv.writer(sys.stdout)
    report.writerow(["order_id", "payment_usd", "receipt_usd", "status"])
    for order, entries in sorted(records.items()):
        payments, receipts = entries["payment"], entries["receipt"]
        if len(payments) > 1 or len(receipts) > 1:
            status = "duplicate_review"
        elif not receipts:
            status = "missing_receipt"
        elif not payments:
            status = "missing_payment"
        elif payments == receipts:
            status = "matched"
        else:
            status = "amount_mismatch"
        report.writerow([order, "|".join(map(str, payments)), "|".join(map(str, receipts)), status])


if __name__ == "__main__":
    main()
