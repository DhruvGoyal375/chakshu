import pandas as pd
import requests
from bs4 import BeautifulSoup


class WikipediaScraper:
    def __init__(self):
        self.link = {}
        self.figure = []
        self.images = []
        self.subtables = {}
        self.citations = []

    def clean_html_tags(self, soup):
        """Remove unwanted tags like script, style that do not have any important text."""
        for tag in soup.find_all(["sup", "script", "style"]):
            tag.decompose()
        return soup

    def fetch_wikipedia_content(self, url):
        """Fetch the page and parse it using Beautiful Soup."""
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to retrieve the page.")
            return None
        return BeautifulSoup(response.text, "html.parser")

    def process_table(self, element):
        # Used for processing the table elements.
        for i in element.find_all("a"):
            if type(i.get_text()) is str:
                self.link[i.get_text()] = i.get("href")
        for i in element.find_all("img"):
            self.images.append([i.get("src"), i.get("alt")])

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
        i = 0
        tstr = ""
        while i < len(rows):
            row = rows[i]
            cells = row.find_all(["th", "td"])
            if cells[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
                if len(table_data) != 0:
                    tstr += pd.DataFrame(table_data).to_string(index=False, header=False) + "\n"
                    table_data.clear()
                table = cells[0].get_text()
                i += 1
                td = []
                while i < len(rows):
                    rd = []
                    cels = rows[i].find_all(["th", "td"])
                    if cels[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
                        break
                    for cel in cels:
                        rd.append(cel.get_text(strip=True, separator=" "))
                    i += 1
                    td.append(rd)
                if not td:
                    tstr += "\n"
                    continue
                df = pd.DataFrame(td)  # noqa: PD901
                tablee = df.to_string(index=False, header=False) + "\n"
                tstr += table + "\n" + tablee + "\n"
                self.subtables[table] = td
                continue
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
            i += 1
        if not table_data:
            return tstr
        table_df = pd.DataFrame(table_data)
        drf = table_df.to_string(index=False, header=False)
        tstr += drf
        return tstr

    def print_structure(self, soup):
        """Process and print the content from the soup object."""
        content = []
        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "cite", "figure"]):
            if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                for a in element.find_all("a"):
                    if isinstance(a.get_text(), str):
                        self.link[a.get_text()] = a.get("href")
                for img in element.find_all("img"):
                    self.images.append([img.get("src"), img.get("alt")])
                if element.get_text(strip=True) == "Contents":
                    continue
                content.append(f"\n{element.get_text(strip=True)}\n")

            elif element.name == "p":
                for a in element.find_all("a"):
                    if isinstance(a.get_text(), str):
                        self.link[a.get_text()] = a.get("href")
                for img in element.find_all("img"):
                    self.images.append([img.get("src"), img.get("alt")])
                content.append(element.get_text())
                for cite in element.find_all("cite"):
                    cite.decompose()

            # elif element.name == "table":
            #     table_str = self.process_table(element)
            #     if table_str:
            #         content.append("\n" + table_str + "\n")

            elif element.name == "ul":
                for a in element.find_all("a"):
                    if isinstance(a.get_text(), str):
                        self.link[a.get_text()] = a.get("href")
                for img in element.find_all("img"):
                    self.images.append([img.get("src"), img.get("alt")])
                if "mw-gallery-traditional" in element.get("class", []):
                    for item in element.find_all("div", ["thumb", "gallerytext"]):
                        if "thumb" in item.get("class", []):
                            content.append(item.find_all("img")[0].get("alt", ""))
                        else:
                            content.append(item.get_text())

            elif element.name == "figure":
                self.figure.append([element.img.get("src"), element.figcaption.get_text()])

            elif element.name == "cite":
                for a in element.find_all("a"):
                    if isinstance(a.get_text(), str):
                        self.link[a.get_text()] = a.get("href")
                for img in element.find_all("img"):
                    self.images.append([img.get("src"), img.get("alt")])
                content.append(element.get_text())
                self.citations.append(element.get_text())

        # for block in content:
        #     print(block)
        return content

    def fetch_short_description(self, soup):
        """Fetch text from div with class 'shortdescription'."""
        short_desc_div = soup.find("div", class_="shortdescription")
        if short_desc_div:
            return short_desc_div.get_text(strip=True)
        return "No short description available."

    def main(self, url):
        soup = self.fetch_wikipedia_content(url)
        if soup is None:
            return
        soup = self.clean_html_tags(soup)
        whole_content = self.print_structure(soup)
        print(whole_content)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/James_Bond"
    scraper = WikipediaScraper()
    scraper.main(url)
