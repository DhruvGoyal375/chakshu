import csv
import logging

import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

url_input = input("Enter the URL of the Wikipedia page: ")
table_number = int(input("Enter the table number you want to scrape: "))

# URL of the Wikipedia page
url = url_input
logging.debug(f"URL set to: {url}")

# Send a request to fetch the page content
response = requests.get(url)
logging.debug(f"HTTP GET request sent to {url}, status code: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")
logging.debug("Page content parsed with BeautifulSoup")

# Find all tables with class 'wikitable'
tables = soup.find_all("table", class_="wikitable")
logging.debug(f"Found {len(tables)} tables on the page")

# Select the 7th table (as indicated by table index 6)
if len(tables) > table_number - 1:
    table = tables[table_number - 1]
    logging.debug("table selected")
else:
    logging.error("enter valid table number")
    table = None


# Function to safely extract text from an element
def get_text_safe(element):
    return element.get_text(strip=True) if element else "N/A"


# Dictionary to manage rowspan and colspan values: {col_index: (value, remaining_rows)}
rowspan_memory = {}
colspan_memory = None


# Function to handle the creation of headers with colspan and rowspan
def parse_headers(table):
    header_rows = []
    headers = []
    rows = table.find_all("tr")

    for row in rows:
        ths = row.find_all("th")
        if ths:
            header_row = [{"text": th.get_text(strip=True), "colspan": int(th.get("colspan", 1))} for th in ths]
            header_rows.append(header_row)

    # Initialize prev_idx to -1 and parse headers
    final_headers = []
    prev_idx = -1

    # Only process the first row to find the main headings
    for idx, header in enumerate(header_rows[0]):
        main_heading = header["text"]
        colspan = header["colspan"]

        if colspan > 1 and len(header_rows) > 1:
            # Go to the next row and get subheadings
            subheadings = header_rows[1][prev_idx + 1 : prev_idx + 1 + colspan]
            # Build new headers in the format main-heading subheading
            final_headers.extend([f"{main_heading}-{subheading['text']}" for subheading in subheadings])
            prev_idx += colspan
        else:
            # If colspan == 1, it's a standalone column
            final_headers.append(main_heading)

    return final_headers


if table:
    # Extract headers to use as keys for dictionary entries
    headers = parse_headers(table)
    logging.debug(f"Table headers extracted: {headers}")

    data = []  # List to store all row data

    # Loop over rows (skipping the header row)
    for row in table.find_all("tr")[1:]:
        entry = {}  # Store the current row's data
        cells = row.find_all(["td", "th"])  # Get all cells for the current row
        cell_idx = 0  # Track the cell index as we parse through

        # Process each column (adjusting for skipped columns from rowspan memory)
        for col_idx, header in enumerate(headers):
            # Handle rowspan memory
            if col_idx in rowspan_memory:
                value, remaining = rowspan_memory[col_idx]
                entry[header] = value  # Use the memory value

                # Decrease the remaining count, and remove if done
                if remaining > 1:
                    rowspan_memory[col_idx] = (value, remaining - 1)
                else:
                    del rowspan_memory[col_idx]

            # Handle colspan memory
            elif colspan_memory is not None:
                entry[header] = colspan_memory["value"]
                colspan_memory["remaining"] -= 1

                # If no more columns to fill, reset the colspan memory
                if colspan_memory["remaining"] == 0:
                    colspan_memory = None

            else:
                # Handle the next available cell for this column
                if cell_idx < len(cells):
                    cell = cells[cell_idx]
                    value = get_text_safe(cell)

                    # Check for rowspan and store in memory if needed
                    rowspan = int(cell.get("rowspan", 1))
                    if rowspan > 1:
                        rowspan_memory[col_idx] = (value, rowspan - 1)

                    # Check for colspan and store in memory if needed
                    colspan = int(cell.get("colspan", 1))
                    if colspan > 1:
                        colspan_memory = {"value": value, "remaining": colspan - 1}

                    entry[header] = value  # Store the current cell's value
                    cell_idx += 1  # Move to the next cell
                else:
                    entry[header] = "N/A"  # If no cell is available, default to 'N/A'

        # Add the row entry to the data list
        data.append(entry)
        logging.debug(f"Row added: {entry}")

    # Save the data to a TSV file
    tsv_file_path = "scraped_table.tsv"
    logging.debug(f"Saving data to {tsv_file_path}")
    with open(tsv_file_path, "w", newline="") as tsv_file:
        writer = csv.DictWriter(tsv_file, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        writer.writerows(data)
    logging.debug("Data saved to TSV file successfully")

    print(f"Data saved to {tsv_file_path}")
else:
    logging.error("No table found to process.")
