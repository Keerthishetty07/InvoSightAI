# InvoSightAI — TallyPrime Export

## What was added

The invoice detail page now provides three TallyPrime-oriented export options:

- Excel (`.xlsx`) — field-oriented workbook for TallyPrime user-defined transaction mapping.
- XML (`.xml`) — Tally voucher import envelope using the current invoice-level fields.
- JSON (`.json`) — TallyPrime Release 7 integration-style request payload.

TallyPrime supports importing data from Excel and XML in Release 4.0+, and JSON in Release 7.0+. Excel imports can use Mapping Templates, while native XML/JSON imports depend on the fields and masters configured in the target company.

## Current limitation

The current `Invoice` model stores invoice-level totals but does not store:

- individual item/stock-item rows
- quantity and rate per item
- HSN/SAC per item
- separate CGST, SGST and IGST amounts
- place of supply
- Tally ledger mappings

Therefore the first Tally export implementation is intentionally invoice-level. It should not be presented as a complete GST/stock-item accounting voucher until line-item extraction and tax-component mapping are added.

## Recommended next implementation

1. Add an `InvoiceItem` model.
2. Extract item name, HSN/SAC, quantity, unit, rate and amount.
3. Extract CGST/SGST/IGST separately.
4. Add editable Tally ledger mapping fields.
5. Generate native item-wise Tally vouchers.
6. Add a Tally company name/configuration setting.
7. Test imports against the target TallyPrime release and company backup.

## Import note

For Excel, TallyPrime supports both predefined Sample Excel Files and user-defined Excel files mapped through Mapping Templates. Users should verify that party and dependent ledgers/masters exist before importing transactions.
