# VLOOKUP with Gemini in Google Sheets

**Estimated Time to Complete:** 20 minutes

## Overview

VLOOKUP is a powerful function in Google Sheets that allows you to search for a specific value in a column and return a corresponding value from another column. However, constructing VLOOKUP formulas can be tricky and error-prone. Gemini can help you generate these formulas quickly and accurately, directly within your spreadsheet.

>Note: This use case assumes you have an understanding of VLOOKUP functions, including when you might want to use one. 

<details>
<summary>Click here for a refresher on VLOOKUP functions</summary>

**When Would You Need a VLOOKUP?** 

* *You're looking up information:* If you have a 'key' (like a product ID, customer number, or name) and you want to find corresponding information (like a price, address, or other details) in another table or sheet, VLOOKUP is often a good choice.

* *Data is organized vertically:* VLOOKUP searches for a value in the first column of a range and returns a value from the same row in a specified column.1 This means your data needs to be arranged with the lookup value in the leftmost column of your lookup table.   
* *You need to pull data from another sheet or range:* If the information you need is in a separate sheet or a different part of the same sheet, VLOOKUP can bridge that gap.

* *You want to automate data retrieval:* Instead of manually searching for information, VLOOKUP lets you automatically pull it in based on a lookup value.

**LOOKUP Basics**

* What it does: VLOOKUP searches for a value in the first column of a range and returns a value in the same row from a column you specify.

* The Syntax:

```markdown
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

* lookup_value: The value you want to find (e.g., a product ID).
* table_array: The range of cells where you're searching (e.g., 'Products'!A:C).
* col_index_num: The column number within the table_array that contains the value you want to return. (The first column of the table_array is 1)
* [range_lookup]: (Optional) TRUE (or omitted) for an approximate match, or FALSE for an exact match. It's almost always best practice to use FALSE for exact matches to avoid unexpected results.

</details>


## Steps

**1. Access Gemini in Google Sheets**

* Open a Google Sheet that contains data you want to write a VLOOKUP function for.
* Look for the Gemini icon in the right-hand side panel of your Google Sheet window.
* Click on the icon to open the Gemini interface.

**2. Provide a Prompt to Gemini**

* In the Gemini chat, type a prompt describing the VLOOKUP formula you want to create.
    * Be clear about the lookup value, the range containing the data, and the column index number of the return value.
    * You can reference cells or ranges in your sheet directly within your prompt.

* **Prompt Templates:**
```markdown 
"Create a VLOOKUP formula that [clearly state the lookup value, the range containing the data, and the column index number of the return value]."

"I need to find a formula that looks up the value in [cell containing lookup value] in the table [range containing data]. When it finds a match, I want it to return the value from the [column number] column of the table."
```

<details>
<summary>Click here for an example</summary>

Imagine you have two sheets in your Google Sheet workbook: "Products" and "Sales".
* The "Products" sheet contains product information, including product ID (column A), product name (column B), and price (column C).
* The "Sales" sheet contains sales records, including product ID (column B), quantity sold (column C), and revenue (column D).
* You want to use VLOOKUP to bring the product name and price from the "Products" sheet into the "Sales" sheet based on the product ID.

   
    **Sample Data:**

    Products Sheet

    | Product ID | Product Name | Price |
    |---|---|---|
    | A123 | Apple iPhone 15 | $999 |
    | B456 | Samsung Galaxy S23 | $899 |
    | C789 | Google Pixel 8 | $799 |
    | D101 | OnePlus 12 | $699 |

    **Sales Sheet**

    | Sale ID | Product ID | Quantity | Revenue | Product Name | Price |
    |---|---|---|---|---|---|
    | S1 | B456 | 2 | $1798 |  |  |
    | S2 | A123 | 1 | $999 |  |  |
    | S3 | C789 | 3 | $2397 |  |  |
    | S4 | D101 | 2 | $1398 |  |  |

    **Sample Prompts:**

    ```markdown 
    "I have two sheets in my Google Sheet workbook: 'Products' and 'Sales'. In the 'Sales' sheet, cell D2, I want to use VLOOKUP to find the product name from the 'Products' sheet, where the product ID in 'Sales' sheet B2 matches the product ID in the 'Products' sheet column A. The product name is in the second column of the 'Products' sheet. Provide the exact formula."

    "Create a Google Sheets VLOOKUP formula to retrieve the price from the 'Products' sheet, column C, based on the product ID in cell B2 of the 'Sales' sheet. The product ID is in column A of the 'Products' sheet. Return an exact match."
    ```

**Key things to include in your prompt:**
* The sheets involved (e.g., "Products" and "Sales")
* The lookup value (e.g., "cell B2")
* The table array (e.g., "Products!A:C" or "the 'Products' sheet")
* The column index number (e.g., "the second column")
* The range lookup (e.g., "exact match" or "FALSE")
* The column you want the results in.

</details>


**3. Review the Generated Formula**

* Gemini will analyze your prompt and create a formula that matches your instructions.
* The formula will appear in the Gemini chat window.

```MARKDOWN
Example VLOOKUP Formula:`=VLOOKUP(B2,Products!A:B,2,FALSE)`
```

**4. Refine the Formula with Gemini**

* If you need to make any changes, ask Gemini to revise the formula.
* You can ask Gemini to adjust the formula to use a different lookup value, search range, or column index number.

Examples of prompts to ask for changes:
```markdown
"Can you modify this formula to search for the value in cell B3 instead?"`

"Can you change this formula to search in the range A:C?"`

"Can you adjust this formula to return the value from the 3rd column instead?"
```

**5. Copy and Paste the Formula**

* When you're satisfied with the formula, copy it from the Gemini chat window.
* Paste the formula into the desired cell in your Google Sheet.

## Additional Resources

* [VLOOKUP in Google Sheets](https://support.google.com/docs/answer/3093318?hl=en)
* [Collaborate with Gemini in Google Sheets](https://support.google.com/docs/answer/14605956)