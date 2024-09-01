import pandas as pd
import requests
from bs4 import BeautifulSoup

link = {}
figure = []
images = []


def clean_html_tags(soup):
    # Remove unwanted tags like script, style that doesnot have any important text.
    for sup in soup.find_all("sup"):
        sup.decompose()
    for script in soup.find_all("script"):
        script.decompose()
    for style in soup.find_all("style"):
        style.decompose()
    return soup


def fetch_wikipedia_content(url):
    # Fetching the page parsing it using Beautiful Soup.
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page.")
        return None
    return BeautifulSoup(response.text, "html.parser")


def process_table(element):
    # Used for processing the table elements.
    for i in element.find_all("a"):
        if type(i.get_text()) is str:
            link[i.get_text()] = i.get("href")
            # print(i.get_text(), ":", i.get('href'))
    for i in element.find_all("img"):
        images.append([i.get("src"), i.get("alt")])

    rows = element.find_all("tr")
    cols = len(rows[0].find_all("th"))

    if cols == 1:
        # For summary table on top right, use heading's colspan as cols
        if "vevent" in element["class"]:
            cols = int(rows[0].find_all("th")[0]["colspan"])
        else:
            return ""
    # For tables containing only list items
    if cols == 0:
        tabledata = ""
        lists = rows[0].find_all("li")
        for listt in lists:
            tabledata += listt.get_text()
            tabledata += "\n"
        return tabledata

    table_data = []
    # Count array for remaining rowspans of each column
    counts = [0] * cols
    # Corresponding text data for the columns with remaining rowspan
    textdata = [None] * cols

    for row in rows:
        cells = row.find_all(["th", "td"])
        row_data = []
        # For cells list
        cell_counter = 0
        # For total columns
        current_column = 0
        while current_column < cols:
            # Adjust for any pending rowspans
            if counts[current_column] > 0:
                row_data.append(textdata[current_column])
                counts[current_column] -= 1
                current_column += 1
                continue

            cell_text = cells[cell_counter].get_text(strip=True, separator=" ")
            colspan = int(cells[cell_counter].get("colspan", 1))
            rowspan = int(cells[cell_counter].get("rowspan", 1))
            # New column having rowspan, update using current_column
            if rowspan > 1:
                counts[current_column] = rowspan - 1
                textdata[current_column] = cell_text
            cell_counter += 1
            current_column += colspan
            row_data.append(cell_text)

        table_data.append(row_data)
        # print(row_data)

    table_df = pd.DataFrame(table_data)
    return table_df.to_string(index=False, header=False)


def print_structure(soup):
    # Used for all data processing and printing it.
    content = []
    for element in soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "cite", "figure"]
    ):
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            # If we are under heading.
            for i in element.find_all("a"):
                # Used for processing anchor tags.
                if type(i.get_text()) is str:
                    link[i.get_text()] = i.get("href")
                    # print(i.get_text(), ":", i.get('href'))
            for i in element.find_all("img"):
                # Used for processing image tags.
                images.append([i.get("src"), i.get("alt")])
            if element.get_text(strip=True) == "Contents":
                continue
            content.append(f"\n{element.get_text(strip=True)}\n")

        elif element.name == "p":
            # For paragraph tag. Below code for anchor and images same for each element name.
            for i in element.find_all("a"):
                if type(i.get_text()) is str:
                    link[i.get_text()] = i.get("href")
                    # print(i.get_text(), ":", i.get('href'))
            for i in element.find_all("img"):
                images.append([i.get("src"), i.get("alt")])
            paragraph = element.get_text()
            content.append(paragraph)
            # To make citations appear only once. Else it was being taken twice. Both under para tag as well as cite elif branching.
            for i in element.find_all("cite"):
                i.decompose()

        elif element.name == "table":
            # Calling the function for table processing.
            table_str = process_table(element)
            if table_str != "":
                content.append("\n" + table_str + "\n")

        elif element.name == "ul":
            # To process ul tag.
            for i in element.find_all("a"):
                if type(i.get_text()) is str:
                    link[i.get_text()] = i.get("href")
                    # print(i.get_text(), ":", i.get('href'))
            for i in element.find_all("img"):
                images.append([i.get("src"), i.get("alt")])
            # For list of images
            if "mw-gallery-traditional" in element.attrs.get("class", ""):
                item_list = element.find_all("div", ["thumb", "gallerytext"])
                for item in item_list:
                    if "thumb" in item["class"]:
                        content.append(item.find_all("img")[0].attrs.get("alt", ""))
                    else:
                        content.append(item.get_text())

        elif element.name == "figure":
            # Used to get the figure tag.
            figure.append([element.img.get("src"), element.figcaption.get_text()])

        elif element.name == "cite":
            # Used to get the ctie tag.
            for i in element.find_all("a"):
                if type(i.get_text()) is str:
                    link[i.get_text()] = i.get("href")
                    # print(i.get_text(), ":", i.get('href'))
            for i in element.find_all("img"):
                images.append([i.get("src"), i.get("alt")])
            cite = element.get_text()
            content.append(cite)

        # To use figcaption description in text content where images occur
        # elif element.name == 'img':
        #     for sibling in element.parent.find_next_siblings():
        #         if sibling.name=='figcaption':
        #             content.append("Image: "+sibling.get_text()+"\n")

    # Print the structured content
    for block in content:
        print(block)


def main(url):
    soup = fetch_wikipedia_content(url)
    if soup is None:
        return
    soup = clean_html_tags(soup)
    print_structure(soup)


# Example usage
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/James_Bond"
    main(url)
    # For printing links, figure, images to check the output.
    # for i in link:
    #     print(i, ":", link[i])
    # for i in figure:
    #     print(i[0],":", i[1])
    # for i in images:
    #     print(i[0],":", i[1])
