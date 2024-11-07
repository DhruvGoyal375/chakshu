import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


class WikipediaScraper:
    def __init__(self):
        self.link = {}
        self.figure = []
        self.images = []
        self.subtables = {}
        self.listcontent = []
        self.paragraphs = []
        self.headings = []
        self.paralink = []
        self.content = []

    def clean_html_tags(self, soup):
        try:
            # Remove unwanted tags like script, style, link that do not have any important text.
            for tag in soup.find_all(["script", "style", "link"]):
                try:
                    tag.decompose()
                except Exception as e:
                    print(f"Error decomposing tag: {e}")

            for tag in soup.find_all("sup"):
                # Remove unwanted reference superscripts
                try:
                    if not tag.get_text() or tag.get_text()[0] == "[":
                        tag.decompose()
                except Exception as e:
                    print(f"Error decomposing tag: {e}")
                else:
                    try:
                        # Replace minus character with hyphen
                        tag.string = tag.string.replace("\u2212", "-")
                        # To detect charge in chemical formulae
                        tag.string = "{" + tag.string
                    except Exception:
                        # print(f"Error as tag string is empty")
                        pass
            # Remove empty paragraph at start of page
            for tag in soup.find_all("p", class_="mw-empty-elt"):
                try:
                    tag.decompose()
                except Exception as e:
                    print(f"Error decomposing empty element: {e}")
            return soup
        except Exception as e:
            print(f"Error cleaning HTML tags: {e}")
            return soup

    def fetch_wikipedia_content(self, url):
        try:
            # Fetch the page and parse it using Beautiful Soup.
            response = requests.get(url)
            if response.status_code != 200:
                print("Failed to retrieve the page.")
                return None
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error fetching Wikipedia content: {e}")
            return None

    def find_chemical_formulae(self, text):
        try:
            # List of valid element symbols from the periodic table
            ELEMENTS = {
                "H",
                "He",
                "Li",
                "Be",
                "B",
                "C",
                "N",
                "O",
                "F",
                "Ne",
                "Na",
                "Mg",
                "Al",
                "Si",
                "P",
                "S",
                "Cl",
                "Ar",
                "K",
                "Ca",
                "Sc",
                "Ti",
                "V",
                "Cr",
                "Mn",
                "Fe",
                "Co",
                "Ni",
                "Cu",
                "Zn",
                "Ga",
                "Ge",
                "As",
                "Se",
                "Br",
                "Kr",
                "Rb",
                "Sr",
                "Y",
                "Zr",
                "Nb",
                "Mo",
                "Tc",
                "Ru",
                "Rh",
                "Pd",
                "Ag",
                "Cd",
                "In",
                "Sn",
                "Sb",
                "Te",
                "I",
                "Xe",
                "Cs",
                "Ba",
                "La",
                "Ce",
                "Pr",
                "Nd",
                "Pm",
                "Sm",
                "Eu",
                "Gd",
                "Tb",
                "Dy",
                "Ho",
                "Er",
                "Tm",
                "Yb",
                "Lu",
                "Hf",
                "Ta",
                "W",
                "Re",
                "Os",
                "Ir",
                "Pt",
                "Au",
                "Hg",
                "Tl",
                "Pb",
                "Bi",
                "Po",
                "At",
                "Rn",
                "Fr",
                "Ra",
                "Ac",
                "Th",
                "Pa",
                "U",
                "Np",
                "Pu",
                "Am",
                "Cm",
                "Bk",
                "Cf",
                "Es",
                "Fm",
                "Md",
                "No",
                "Lr",
                "Rf",
                "Db",
                "Sg",
                "Bh",
                "Hs",
                "Mt",
                "Ds",
                "Rg",
                "Cn",
                "Nh",
                "Fl",
                "Mc",
                "Lv",
                "Ts",
                "Og",
            }
            # Regular expression to match potential chemical formulae
            pattern = r"[\[\(\s](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.](?:\{)*[\d]*[+-]*|^(?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.](?:\{)*[\d]*[+-]*|[\[\(\s](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*$"
            # pattern = '[\[\(\s^](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.\,$](?:\{)*[\d]*[+-]*'
            matches = re.finditer(pattern, text)

            # Filter matches to only include valid chemical formula patterns
            chemical_formulae = []
            # print(len(matches))

            for matche in matches:
                match = matche.group()
                # print("match:",match)
                # Split the match into potential element-symbol/number sequences
                elements_in_match = re.findall(r"[A-Z][a-z]?|\d+|\[|\]|\(|\)|\{", match)
                valid = True
                i = 0
                # Check if the extracted elements are valid symbols and follow the rules
                j = 0
                while i < len(elements_in_match):
                    if elements_in_match[i] in ELEMENTS:
                        i += 1
                        j += 1
                        # Optionally followed by a number (quantity of atoms)
                        if i < len(elements_in_match) and elements_in_match[i].isdigit():
                            i += 1
                    elif elements_in_match[i] in {"[", "]", "(", ")", "{"}:
                        # Skip valid brackets or parentheses
                        i += 1
                        if i < len(elements_in_match) and elements_in_match[i].isdigit():
                            i += 1
                    elif elements_in_match[i].isdigit():
                        i += 1
                    else:
                        # print(matche,elements_in_match,i)
                        valid = False
                        break

                if valid:
                    if j == 1 and (
                        "I" in match
                        or ("He" in match and "{" not in match)
                        or "At" in match
                        or "As" in match
                        or "No" in match
                        or "As" in match
                    ):
                        continue
                    chemical_formulae.append(matche.span())
            return chemical_formulae
        except Exception as e:
            print(f"Error in finding chemical formula: {e}")

    def replace_math_elements(self, soup):
        """Replace all math elements with a placeholder."""
        try:
            math_counter = 1
            for math_element in soup.find_all("span", class_="mwe-math-element"):
                latex = math_element.img.get("alt")
                latex = latex.replace("/", "//")
                url = "http://localhost:8080/api"
                data = {"latexInput": latex}
                response = requests.post(url, json=data)
                text = "Math Equation"
                if response.status_code == 200:  # 201 Created
                    text = response.json()["output"]
                    # print(text)
                else:
                    print(f"Error: {response.status_code}")
                # Converting dd tag to p tag since most maths equations are inside dd tag.
                if math_element.parent.name == "dd":
                    par = math_element.parent.parent
                    math_element.parent.replace_with(text)
                    par.name = "p"
                    # print(par)
                else:
                    math_element.replace_with(text)
                math_counter += 1
            return soup
        except Exception as e:
            print(f"Error replacing math elements: {e}")
            return soup

    def process_chemical_formulae(self, chemical_formulae, text):
        try:
            # Covert common roman numerals to numbers
            text = text.replace("(I)", "1").replace("II", "2").replace("III", "3")
            offset = 0
            for formu in chemical_formulae:
                formula = text[formu[0] + offset : formu[1] + offset]
                # print(formula)
                off = 0
                i = 0
                while i + off < len(formula) - 1:
                    length = len(formula)
                    c = formula[i + off]
                    if c == "[":
                        formula = formula[: i + off] + "\nopen bracket\n" + formula[i + off + 1 :]
                    elif c == "]":
                        formula = formula[: i + off] + "\nclosed bracket\n" + formula[i + off + 1 :]
                    elif c.isalnum():
                        if c == "C" and formula[i + off + 1] == "o":
                            formula = formula[: i + off] + " Cobalt " + formula[i + off + 2 :]
                        else:
                            formula = formula[: i + off] + " " + c + " " + formula[i + off + 1 :]
                    elif c == "+":
                        formula = formula[: i + off] + "positive" + formula[i + off + 1 :]
                    elif c == "-":
                        formula = formula[: i + off] + "negative" + formula[i + off + 1 :]
                    elif c == "{":
                        formula = formula[: i + off] + " charge " + formula[i + off + 1 :]
                    elif c == "(":
                        formula = formula[: i + off] + c + formula[i + off + 1 :]
                    elif c == ")":
                        formula = formula[: i + off] + c + formula[i + off + 1 :]
                    off += len(formula) - length
                    i += 1
                # print(formula)
                text = text[: formu[0] + offset] + formula + text[formu[1] + offset :]
                offset += off
            return text
        except Exception as e:
            print(f"Error in processing chemical formula: {e}")

    def tableToString(self, tableList):
        try:
            tableString = ""
            cols = len(tableList[1])
            for rowCount in range(1, len(tableList)):
                tableString += f"Row {rowCount}: "
                for colCount in range(0, cols):
                    tableString += tableList[0][colCount] + ": " + tableList[rowCount][colCount] + ",  "
                tableString += "\n"
            return tableString
        except Exception as e:
            print(f"Error converting table to string: {e}")
            return ""

    def extract_links_images(self, element):
        try:
            for i in element.find_all("a"):
                try:
                    if isinstance(i.get_text(), str):
                        self.link[i.get_text()] = i.get("href")
                except Exception as e:
                    print(f"Error processing link: {e}")
            for i in element.find_all("img"):
                try:
                    self.images.append([i.get("src"), i.get("alt")])
                except Exception as e:
                    print(f"Error processing image: {e}")
        except Exception as e:
            print(f"Error extracting links and images: {e}")

    def process_table(self, element):
        try:
            # Used for processing the table elements.
            for i in element.find_all("a"):
                if type(i.get_text()) is str:
                    self.link[i.get_text()] = i.get("href")
            for i in element.find_all("img"):
                self.images.append([i.get("src"), i.get("alt")])

            rows = element.find_all("tr")
            cols = len(rows[0].find_all("th"))
            flg = False
            if cols == 1:
                if "vevent" in element["class"]:
                    cols = int(rows[0].find_all("th")[0]["colspan"])
                    flg = True
                else:
                    return ""

            if cols == 0:
                return ""

            table_data = []
            counts = [0] * cols
            textdata = [None] * cols
            rowCounter = 0
            allTableString = ""
            while rowCounter < len(rows):
                row = rows[rowCounter]
                cells = row.find_all(["th", "td"])
                if cells[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
                    if len(table_data) > 1:
                        self.listcontent.append(["table", pd.DataFrame(table_data)])
                        allTableString += pd.DataFrame(table_data).to_string(index=False, header=False) + "\n"
                    table_data.clear()
                    tableHeading = cells[0].get_text()
                    rowCounter += 1
                    tableList = []
                    while rowCounter < len(rows):
                        rowList = []
                        cells = rows[rowCounter].find_all(["th", "td"])
                        if cells[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
                            if flg:
                                if not tableList:
                                    allTableString += "\n"
                                    break
                                tableDf = pd.DataFrame(tableList)
                                tableString = tableDf.to_string(index=False, header=False) + "\n"
                                allTableString += tableHeading + "\n" + tableString + "\n"
                                self.subtables[tableHeading] = tableList
                                self.listcontent.append(["subtable " + tableHeading, tableDf])
                                table_data.clear()
                                tableList.clear()
                                tableHeading = cells[0].get_text()
                                rowCounter += 1
                                cells = rows[rowCounter].find_all(["th", "td"])
                            else:
                                break
                        for cel in cells:
                            rowList.append(cel.get_text(strip=True, separator=" "))
                        rowCounter += 1
                        tableList.append(rowList)
                    if not tableList:
                        allTableString += "\n"
                        continue
                    if not flg:
                        hdng = rows[0].find_all("th")
                        for cnt in range(0, len(hdng)):
                            hdng[cnt] = hdng[cnt].get_text(strip=True)
                        tableList = [hdng] + tableList
                    table_df = pd.DataFrame(tableList)
                    tableString = table_df.to_string(index=False, header=False) + "\n"
                    allTableString += tableHeading + "\n" + tableString + "\n"
                    self.subtables[tableHeading] = tableList
                    self.listcontent.append(["subtable " + tableHeading, table_df])
                    continue
                row_data = []
                cell_counter = 0
                current_column = 0
                while current_column < cols:
                    if counts[current_column] > 0:
                        row_data.append(textdata[current_column])
                        counts[current_column] -= 1
                        current_column += 1
                        continue
                    cell_text = cells[cell_counter].get_text(strip=True, separator=" ")
                    colspan = int(cells[cell_counter].get("colspan", 1))
                    rowspan = int(cells[cell_counter].get("rowspan", 1))
                    if rowspan > 1:
                        counts[current_column] = rowspan - 1
                        textdata[current_column] = cell_text
                    cell_counter += 1
                    current_column += colspan
                    row_data.append(cell_text)
                table_data.append(row_data)
                rowCounter += 1
            if not table_data:
                return allTableString
            table_df = pd.DataFrame(table_data)
            if flg:
                self.listcontent.append(["subtable", table_df])
            else:
                self.listcontent.append(["table", table_df])
            tableString = table_df.to_string(index=False, header=False)
            allTableString += tableString
            return allTableString
        except Exception as e:
            print(f"Error processing table: {e}")
            return ""

    def process_structure(self, soup):
        try:
            self.content = []
            for element in soup.find_all(
                ["h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "cite", "figure", "dd"]
            ):
                try:
                    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        if element.get("id") in ["Bibliography", "External_links", "References"]:
                            break
                        self.extract_links_images(element)
                        text = element.get_text(strip=True)
                        if text == "Contents":
                            continue
                        formulae = self.find_chemical_formulae(text)
                        text = self.process_chemical_formulae(formulae, text)
                        self.content.append(f"\n{text}\n")
                        self.headings.append(text)
                        self.listcontent.append([element.name, text])

                    elif element.name == "p":
                        self.extract_links_images(element)
                        self.process_paragraph(element)

                    elif element.name == "table":
                        table_str = self.process_table(element)
                        if table_str:
                            self.content.append("\n" + table_str + "\n")

                    elif element.name == "ul":
                        self.extract_links_images(element)
                        self.process_ul(element)

                    elif element.name == "figure":
                        if element.img.get("src"):
                            self.figure.append([element.img.get("src"), element.figcaption.get_text()])

                    elif element.name == "dd":
                        chemspan = element.find_all("span", class_="chemf")
                        for span in chemspan:
                            text = span.get_text()
                            text = (
                                text.replace("(s)", " solid ").replace("(aq)", " aqueous ").replace("(g)", " gaseous ")
                            )
                            formula = self.find_chemical_formulae(text)
                            text = self.process_chemical_formulae(formula, text)
                            text = (
                                text.replace("\u2192", "yields")
                                .replace("\u2191", "released as gas")
                                .replace("\u2193", "as precitipate")
                                .replace("\u21cc", "is in equilibrium with")
                                .replace("\u21c4", "is in equilibrium with")
                            )
                            # print(text)
                            self.content.append(text)

                except Exception as inner_e:
                    print(f"Error processing element: {inner_e}")
        except Exception as e:
            print(f"Error in print_structure: {e}")

    def process_ul(self, element):
        if "mw-gallery-traditional" in element.get("class", []):
            flag = False
            for item in element.find_all("div", ["thumb", "gallerytext"]):
                if "thumb" in item.get("class", []):
                    self.content.append(item.find_all("img")[0].get("alt", ""))
                else:
                    self.content.append(item.get_text())
                    if flag:
                        self.listcontent[-1][1] += "\n" + item.get_text()
                    else:
                        self.listcontent.append([element.name, item.get_text()])
                        flag = True
        else:
            if element.find_parent("table", class_="vevent"):
                return
            flag = False
            for item in element.find_all("li"):
                self.content.append(item.get_text())
                if flag:
                    self.listcontent[-1][1] += "\n" + item.get_text()
                else:
                    self.listcontent.append([element.name, item.get_text()])
                    flag = True
            self.content.append("\n")

    def process_paragraph(self, element):
        temp = {}
        text = element.get_text()
        formulae = self.find_chemical_formulae(text)
        text = self.process_chemical_formulae(formulae, text)
        for a in element.find_all("a"):
            if isinstance(a.get_text(), str):
                temp[a.get_text()] = a.get("href")
        self.paralink.append(temp)
        self.extract_links_images(element)
        self.content.append(text)
        self.paragraphs.append(text)
        self.listcontent.append([element.name, text])
        for cite in element.find_all("cite"):
            cite.decompose()
        return

    def fetch_short_description(self, soup):
        try:
            short_desc_div = soup.find("div", class_="shortdescription")
            if short_desc_div:
                return short_desc_div.get_text(strip=True)
            return "No short description available."
        except Exception as e:
            print(f"Error fetching short description: {e}")
            return "No short description available."

    def print_structure(self):
        for i in self.content:
            print(i)

    def main(self, url):
        try:
            soup = self.fetch_wikipedia_content(url)
            if soup is None:
                return
            contentsoup = soup.find("div", id="mw-content-text")
            soup = self.clean_html_tags(contentsoup)
            soup = self.replace_math_elements(soup)
            self.process_structure(contentsoup)
            self.print_structure()
        except Exception as e:
            print(f"Error in main: {e}")


if __name__ == "__main__":
    # url = "https://en.wikipedia.org/wiki/James_Bond"
    url = "https://en.wikipedia.org/wiki/Chemical_equation"
    scraper = WikipediaScraper()
    scraper.main(url)
