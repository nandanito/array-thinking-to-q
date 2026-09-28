# Task 01: a total row with a live formula

- **Type:** write-from-spec   **Touches:** formulas, reopening a saved workbook

## Prompt (give verbatim to the model)

> Create a spreadsheet `sales.xlsx` with one sheet named `Sales`. Row 1 is the header `Region`,
> `Units`. Rows 2 to 5 hold North 120, South 95, East 143, West 88. Cell A6 holds the label
> `Total` and cell B6 the formula `=SUM(B2:B5)`. Save the file, then open it again and print two
> lines: the formula stored in B6, and the total of B2:B5 computed from the stored values.

## Reference (for scoring, do not show the model)

- Solution: `01-sum-formula.ref.py` · golden: `01-sum-formula.expected`
