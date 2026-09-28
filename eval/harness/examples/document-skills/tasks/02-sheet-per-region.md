# Task 02: one sheet per region

- **Type:** write-from-spec   **Touches:** splitting tabular data across sheets

## Prompt (give verbatim to the model)

> The CSV below lists orders as `region,product,qty`. Turn it into `orders.xlsx` with one sheet
> per region, named after the region, in order of first appearance. Each sheet has the header
> row `product`, `qty` followed by that region's rows in input order, with qty stored as a
> number. Save the file, reopen it, and print one line per sheet: the sheet name, a colon, and
> the sum of its qty column.
> ```
> region,product,qty
> East,widget,4
> West,gadget,7
> East,gizmo,2
> North,widget,5
> West,widget,1
> ```

## Reference (for scoring, do not show the model)

- Solution: `02-sheet-per-region.ref.py` · golden: `02-sheet-per-region.expected`
