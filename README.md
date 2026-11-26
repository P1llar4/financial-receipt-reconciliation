# Financial and Receipt Reconciliation

This portfolio demo answers a bookkeeping question: which payments have a matching receipt, and which need a closer look?

## Run the example

From the repository root, run `python3 reconcile.py`. Python 3 and its standard library are the only requirements. To save a spreadsheet-ready report, run `python3 reconcile.py > report.csv`.

## What the report shows

| Order | Payment (USD) | Receipt (USD) | Result |
|---|---:|---:|---|
| DEMO-01 | 14.50 | 14.50 | Matched |
| DEMO-02 | 25.00 | 23.00 | Amount mismatch |
| DEMO-03 | 9.99 | — | Missing receipt |
| DEMO-04 | — | 11.00 | Missing payment |
| DEMO-05 | Two entries of 8.00 | 8.00 | Duplicate review |

The script groups records by order ID and compares exact decimal amounts. Repeated entries go to review before matching. The example covers USD purchases and assumes one expected payment and receipt per order.

## Sample data

Both files in `samples/` are fictional. The payment CSV contains normalized records. The MBOX uses two demo-specific email headers for order ID and total. Real merchant email and payment exports require source-specific extraction before reconciliation.
