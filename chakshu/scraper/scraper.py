# import re
# from typing import Optional

# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# # from chakshu.config import ELEMENTS
# ELEMENTS = {
#     "H",
#     "He",
#     "Li",
#     "Be",
#     "B",
#     "C",
#     "N",
#     "O",
#     "F",
#     "Ne",
#     "Na",
#     "Mg",
#     "Al",
#     "Si",
#     "P",
#     "S",
#     "Cl",
#     "Ar",
#     "K",
#     "Ca",
#     "Sc",
#     "Ti",
#     "V",
#     "Cr",
#     "Mn",
#     "Fe",
#     "Co",
#     "Ni",
#     "Cu",
#     "Zn",
#     "Ga",
#     "Ge",
#     "As",
#     "Se",
#     "Br",
#     "Kr",
#     "Rb",
#     "Sr",
#     "Y",
#     "Zr",
#     "Nb",
#     "Mo",
#     "Tc",
#     "Ru",
#     "Rh",
#     "Pd",
#     "Ag",
#     "Cd",
#     "In",
#     "Sn",
#     "Sb",
#     "Te",
#     "I",
#     "Xe",
#     "Cs",
#     "Ba",
#     "La",
#     "Ce",
#     "Pr",
#     "Nd",
#     "Pm",
#     "Sm",
#     "Eu",
#     "Gd",
#     "Tb",
#     "Dy",
#     "Ho",
#     "Er",
#     "Tm",
#     "Yb",
#     "Lu",
#     "Hf",
#     "Ta",
#     "W",
#     "Re",
#     "Os",
#     "Ir",
#     "Pt",
#     "Au",
#     "Hg",
#     "Tl",
#     "Pb",
#     "Bi",
#     "Po",
#     "At",
#     "Rn",
#     "Fr",
#     "Ra",
#     "Ac",
#     "Th",
#     "Pa",
#     "U",
#     "Np",
#     "Pu",
#     "Am",
#     "Cm",
#     "Bk",
#     "Cf",
#     "Es",
#     "Fm",
#     "Md",
#     "No",
#     "Lr",
#     "Rf",
#     "Db",
#     "Sg",
#     "Bh",
#     "Hs",
#     "Mt",
#     "Ds",
#     "Rg",
#     "Cn",
#     "Nh",
#     "Fl",
#     "Mc",
#     "Lv",
#     "Ts",
#     "Og",
# }


# class WikipediaScraper:
#     def __init__(self):
#         self.link = {}
#         self.figure = []
#         self.images = []
#         self.subtables = {}
#         self.listcontent = []
#         self.paragraphs = []
#         self.headings = []
#         self.paralink = []
#         self.content = []

#     def clean_html_tags(self, soup):
#         try:
#             # Remove unwanted tags like script, style, link that do not have any important text.
#             for tag in soup.find_all(["script", "style", "link"]):
#                 try:
#                     tag.decompose()
#                 except Exception as e:
#                     print(f"Error decomposing tag: {e}")

#             for tag in soup.find_all("sup"):
#                 # Remove unwanted reference superscripts
#                 try:
#                     if not tag.get_text() or tag.get_text()[0] == "[":
#                         tag.decompose()
#                 except Exception as e:
#                     print(f"Error decomposing tag: {e}")
#                 else:
#                     try:
#                         # Replace minus character with hyphen
#                         tag.string = tag.string.replace("\u2212", "-")
#                         # To detect charge in chemical formulae
#                         tag.string = "{" + tag.string
#                     except Exception:
#                         # print(f"Error as tag string is empty")
#                         pass

#             # Remove empty paragraph at start of page
#             for tag in soup.find_all("p", class_="mw-empty-elt"):
#                 try:
#                     tag.decompose()
#                 except Exception as e:
#                     print(f"Error decomposing empty element: {e}")

#             return soup

#         except Exception as e:
#             print(f"Error cleaning HTML tags: {e}")

#             return soup

#     def fetch_wikipedia_content(self, url: str) -> Optional[BeautifulSoup]:
#         """Fetch Wikipedia content and parse it thorugh BeautifulSoup."""
#         try:
#             headers = {
#                 'User-Agent': 'AccessibleWikiScraper/1.0 (Accessibility Tool for Blind Users)',
#                 'Accept': 'text/html'
#             }
#             response = requests.get(url, headers=headers, timeout=10)
#             response.raise_for_status()

#             return BeautifulSoup(response.text, "html.parser")

#         except requests.RequestException as e:
#             self._add_error_message(
#                 f"Unable to access Wikipedia page: {str(e)}")
#             return None

#     def find_chemical_formulae(self, text):
#         try:
#             # Regular expression to match potential chemical formulae
#             pattern = r"[\[\(\s](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.](?:\{)*[\d]*[+-]*|^(?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.](?:\{)*[\d]*[+-]*|[\[\(\s](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*$"
#             # pattern = '[\[\(\s^](?:(?:[\d]*(?:[\(\[\)\]])?[\d]*[A-Z][a-z]?[\d]*(?:[\(\[\)\]])?[\d]*)+)(?:\{)*[\d]*[+-]*[\]\)\s\.\,$](?:\{)*[\d]*[+-]*'
#             matches = re.finditer(pattern, text)

#             # Filter matches to only include valid chemical formula patterns
#             chemical_formulae = []
#             # print(len(matches))

#             for matche in matches:
#                 match = matche.group()
#                 # print("match:",match)
#                 # Split the match into potential element-symbol/number sequences
#                 elements_in_match = re.findall(
#                     r"[A-Z][a-z]?|\d+|\[|\]|\(|\)|\{", match)
#                 valid = True
#                 i = 0
#                 # Check if the extracted elements are valid symbols and follow the rules
#                 j = 0
#                 while i < len(elements_in_match):
#                     if elements_in_match[i] in ELEMENTS:
#                         i += 1
#                         j += 1
#                         # Optionally followed by a number (quantity of atoms)
#                         if i < len(elements_in_match) and elements_in_match[i].isdigit():
#                             i += 1
#                     elif elements_in_match[i] in {"[", "]", "(", ")", "{"}:
#                         # Skip valid brackets or parentheses
#                         i += 1
#                         if i < len(elements_in_match) and elements_in_match[i].isdigit():
#                             i += 1
#                     elif elements_in_match[i].isdigit():
#                         i += 1
#                     else:
#                         # print(matche,elements_in_match,i)
#                         valid = False
#                         break

#                 if valid:
#                     if j == 1 and (
#                         "I" in match
#                         or ("He" in match and "{" not in match)
#                         or "At" in match
#                         or "As" in match
#                         or "No" in match
#                         or "As" in match
#                     ):
#                         continue
#                     chemical_formulae.append(matche.span())
#             return chemical_formulae
#         except Exception as e:
#             print(f"Error in finding chemical formula: {e}")

#     def replace_math_elements(self, soup):
#         """Replace all math elements in the article with a placeholder or converted LaTeX output."""
#         try:
#             for math_element in soup.find_all("span", class_="mwe-math-element"):
#                 latex_code = math_element.img.get("alt").replace("/", "//")
#                 api_url = "http://localhost:8080/api"
#                 api_payload = {"latexInput": latex_code}

#                 # Send request to convert LaTeX to text output
#                 response = requests.post(api_url, json=api_payload)
#                 math_placeholder = "Math Equation"

#                 if response.status_code == 200:
#                     math_placeholder = response.json().get("output", math_placeholder)
#                 else:
#                     print(f"Error in API response: {response.status_code}")

#                 # Converting dd tag to p tag since most maths equations are inside dd tag
#                 if math_element.parent.name == "dd":
#                     parent_node = math_element.parent.parent
#                     math_element.parent.replace_with(math_placeholder)
#                     parent_node.name = "p"
#                 else:
#                     math_element.replace_with(math_placeholder)

#             return soup

#         except Exception as e:
#             print(f"Error replacing math elements: {e}")
#             return soup

#     def process_chemical_formulae(self, chemical_formulae, text):
#         try:
#             # Covert common roman numerals to numbers
#             text = text.replace("(I)", "1").replace(
#                 "II", "2").replace("III", "3")
#             offset = 0
#             for formu in chemical_formulae:
#                 formula = text[formu[0] + offset: formu[1] + offset]
#                 # print(formula)
#                 off = 0
#                 i = 0
#                 while i + off < len(formula) - 1:
#                     length = len(formula)
#                     c = formula[i + off]
#                     if c == "[":
#                         formula = formula[: i + off] + \
#                             "\nopen bracket\n" + formula[i + off + 1:]
#                     elif c == "]":
#                         formula = formula[: i + off] + \
#                             "\nclosed bracket\n" + formula[i + off + 1:]
#                     elif c.isalnum():
#                         if c == "C" and formula[i + off + 1] == "o":
#                             formula = formula[: i + off] + \
#                                 " Cobalt " + formula[i + off + 2:]
#                         else:
#                             formula = formula[: i + off] + " " + \
#                                 c + " " + formula[i + off + 1:]
#                     elif c == "+":
#                         formula = formula[: i + off] + \
#                             "positive" + formula[i + off + 1:]
#                     elif c == "-":
#                         formula = formula[: i + off] + \
#                             "negative" + formula[i + off + 1:]
#                     elif c == "{":
#                         formula = formula[: i + off] + \
#                             " charge " + formula[i + off + 1:]
#                     elif c == "(":
#                         formula = formula[: i + off] + \
#                             c + formula[i + off + 1:]
#                     elif c == ")":
#                         formula = formula[: i + off] + \
#                             c + formula[i + off + 1:]
#                     off += len(formula) - length
#                     i += 1
#                 # print(formula)
#                 text = text[: formu[0] + offset] + \
#                     formula + text[formu[1] + offset:]
#                 offset += off
#             return text
#         except Exception as e:
#             print(f"Error in processing chemical formula: {e}")

#     def tableToString(self, tableList):
#         try:
#             tableString = ""
#             cols = len(tableList[1])
#             for rowCount in range(1, len(tableList)):
#                 tableString += f"Row {rowCount}: "
#                 for colCount in range(0, cols):
#                     tableString += tableList[0][colCount] + \
#                         ": " + tableList[rowCount][colCount] + ",  "
#                 tableString += "\n"
#             return tableString
#         except Exception as e:
#             print(f"Error converting table to string: {e}")
#             return ""

#     def extract_links_images(self, element):
#         try:
#             for i in element.find_all("a"):
#                 try:
#                     if isinstance(i.get_text(), str):
#                         self.link[i.get_text()] = i.get("href")
#                 except Exception as e:
#                     print(f"Error processing link: {e}")
#             for i in element.find_all("img"):
#                 try:
#                     self.images.append([i.get("src"), i.get("alt")])
#                 except Exception as e:
#                     print(f"Error processing image: {e}")
#         except Exception as e:
#             print(f"Error extracting links and images: {e}")

#     def process_table(self, element):
#         try:
#             # Used for processing the table elements.
#             for i in element.find_all("a"):
#                 if type(i.get_text()) is str:
#                     self.link[i.get_text()] = i.get("href")
#             for i in element.find_all("img"):
#                 self.images.append([i.get("src"), i.get("alt")])

#             rows = element.find_all("tr")
#             cols = len(rows[0].find_all("th"))
#             flg = False
#             if cols == 1:
#                 if "vevent" in element["class"]:
#                     cols = int(rows[0].find_all("th")[0]["colspan"])
#                     flg = True
#                 else:
#                     return ""

#             if cols == 0:
#                 return ""

#             table_data = []
#             counts = [0] * cols
#             textdata = [None] * cols
#             rowCounter = 0
#             allTableString = ""
#             while rowCounter < len(rows):
#                 row = rows[rowCounter]
#                 cells = row.find_all(["th", "td"])
#                 if cells[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
#                     if len(table_data) > 1:
#                         self.listcontent.append(
#                             ["table", pd.DataFrame(table_data)])
#                         allTableString += pd.DataFrame(table_data).to_string(
#                             index=False, header=False) + "\n"
#                     table_data.clear()
#                     tableHeading = cells[0].get_text()
#                     rowCounter += 1
#                     tableList = []
#                     while rowCounter < len(rows):
#                         rowList = []
#                         cells = rows[rowCounter].find_all(["th", "td"])
#                         if cells[0].name == "th" and int(cells[0].get("colspan", 1)) == cols:
#                             if flg:
#                                 if not tableList:
#                                     allTableString += "\n"
#                                     break
#                                 tableDf = pd.DataFrame(tableList)
#                                 tableString = tableDf.to_string(
#                                     index=False, header=False) + "\n"
#                                 allTableString += tableHeading + "\n" + tableString + "\n"
#                                 self.subtables[tableHeading] = tableList
#                                 self.listcontent.append(
#                                     ["subtable " + tableHeading, tableDf])
#                                 table_data.clear()
#                                 tableList.clear()
#                                 tableHeading = cells[0].get_text()
#                                 rowCounter += 1
#                                 cells = rows[rowCounter].find_all(["th", "td"])
#                             else:
#                                 break
#                         for cel in cells:
#                             rowList.append(cel.get_text(
#                                 strip=True, separator=" "))
#                         rowCounter += 1
#                         tableList.append(rowList)
#                     if not tableList:
#                         allTableString += "\n"
#                         continue
#                     if not flg:
#                         hdng = rows[0].find_all("th")
#                         for cnt in range(0, len(hdng)):
#                             hdng[cnt] = hdng[cnt].get_text(strip=True)
#                         tableList = [hdng] + tableList
#                     table_df = pd.DataFrame(tableList)
#                     tableString = table_df.to_string(
#                         index=False, header=False) + "\n"
#                     allTableString += tableHeading + "\n" + tableString + "\n"
#                     self.subtables[tableHeading] = tableList
#                     self.listcontent.append(
#                         ["subtable " + tableHeading, table_df])
#                     continue
#                 row_data = []
#                 cell_counter = 0
#                 current_column = 0
#                 while current_column < cols:
#                     if counts[current_column] > 0:
#                         row_data.append(textdata[current_column])
#                         counts[current_column] -= 1
#                         current_column += 1
#                         continue
#                     cell_text = cells[cell_counter].get_text(
#                         strip=True, separator=" ")
#                     colspan = int(cells[cell_counter].get("colspan", 1))
#                     rowspan = int(cells[cell_counter].get("rowspan", 1))
#                     if rowspan > 1:
#                         counts[current_column] = rowspan - 1
#                         textdata[current_column] = cell_text
#                     cell_counter += 1
#                     current_column += colspan
#                     row_data.append(cell_text)
#                 table_data.append(row_data)
#                 rowCounter += 1
#             if not table_data:
#                 return allTableString
#             table_df = pd.DataFrame(table_data)
#             if flg:
#                 self.listcontent.append(["subtable", table_df])
#             else:
#                 self.listcontent.append(["table", table_df])
#             tableString = table_df.to_string(index=False, header=False)
#             allTableString += tableString
#             return allTableString
#         except Exception as e:
#             print(f"Error processing table: {e}")
#             return ""

#     def process_structure(self, soup):
#         try:
#             self.content = []

#             for element in soup.find_all(
#                 ["h1", "h2", "h3", "h4", "h5", "h6", "p",
#                     "table", "ul", "cite", "figure", "dd"]
#             ):
#                 try:
#                     element_name = element.name

#                     if element_name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
#                         element_id = element.get("id")

#                         if element_id in ["Bibliography", "External_links", "References"]:
#                             break

#                         self.extract_links_images(element)
#                         text = element.get_text(strip=True)

#                         if text == "Contents":
#                             continue

#                         formulae = self.find_chemical_formulae(text)
#                         text = self.process_chemical_formulae(formulae, text)
#                         self.content.append(f"\n{text}\n")
#                         self.headings.append(text)
#                         self.listcontent.append([element_name, text])

#                     elif element_name == "p":
#                         self.extract_links_images(element)
#                         self.process_paragraph(element)

#                     elif element_name == "table":
#                         table_str = self.process_table(element)
#                         if table_str:
#                             self.content.append("\n" + table_str + "\n")

#                     elif element_name == "ul":
#                         self.extract_links_images(element)
#                         self.process_ul(element)

#                     elif element_name == "figure":
#                         if element.img.get("src"):
#                             self.figure.append(
#                                 [element.img.get("src"), element.figcaption.get_text()])

#                     elif element_name == "dd":
#                         chemspan = element.find_all("span", class_="chemf")

#                         for span in chemspan:
#                             text = span.get_text()
#                             text = (
#                                 text.replace("(s)", " solid ").replace(
#                                     "(aq)", " aqueous ").replace("(g)", " gaseous ")
#                             )
#                             formula = self.find_chemical_formulae(text)
#                             text = self.process_chemical_formulae(
#                                 formula, text)
#                             text = (
#                                 text.replace("\u2192", "yields")
#                                 .replace("\u2191", "released as gas")
#                                 .replace("\u2193", "as precitipate")
#                                 .replace("\u21cc", "is in equilibrium with")
#                                 .replace("\u21c4", "is in equilibrium with")
#                             )
#                             # print(text)
#                             self.content.append(text)

#                 except Exception as inner_e:
#                     print(f"Error processing element: {inner_e}")
#         except Exception as e:
#             print(f"Error in print_structure: {e}")

#     def process_ul(self, element):
#         if "mw-gallery-traditional" in element.get("class", []):
#             flag = False
#             for item in element.find_all("div", ["thumb", "gallerytext"]):
#                 if "thumb" in item.get("class", []):
#                     self.content.append(item.find_all("img")[0].get("alt", ""))
#                 else:
#                     self.content.append(item.get_text())
#                     if flag:
#                         self.listcontent[-1][1] += "\n" + item.get_text()
#                     else:
#                         self.listcontent.append(
#                             [element.name, item.get_text()])
#                         flag = True
#         else:
#             if element.find_parent("table", class_="vevent"):
#                 return
#             flag = False
#             for item in element.find_all("li"):
#                 self.content.append(item.get_text())
#                 if flag:
#                     self.listcontent[-1][1] += "\n" + item.get_text()
#                 else:
#                     self.listcontent.append([element.name, item.get_text()])
#                     flag = True
#             self.content.append("\n")

#     def process_paragraph(self, element):
#         temp = {}
#         text = element.get_text()
#         formulae = self.find_chemical_formulae(text)
#         text = self.process_chemical_formulae(formulae, text)
#         for a in element.find_all("a"):
#             if isinstance(a.get_text(), str):
#                 temp[a.get_text()] = a.get("href")
#         self.paralink.append(temp)
#         self.extract_links_images(element)
#         self.content.append(text)
#         self.paragraphs.append(text)
#         self.listcontent.append([element.name, text])
#         for cite in element.find_all("cite"):
#             cite.decompose()
#         return

#     def fetch_short_description(self, soup):
#         try:
#             short_desc_div = soup.find("div", class_="shortdescription")

#             if short_desc_div:
#                 return short_desc_div.get_text(strip=True)

#             return "No short description available."

#         except Exception as e:
#             print(f"Error fetching short description: {e}")

#             return "No short description available."

#     def print_structure(self):
#         for i in self.content:
#             print(i)

#     def save_content(self, filename: str = "output.txt") -> None:
#         """Save content in an accessible format."""
#         print(self.images)
#         try:
#             with open(filename, "w", encoding="utf-8") as file:
#                 for content in self.content:
#                     file.write(f"{content}\n")

#         except Exception as e:
#             print(f"Error saving content: {str(e)}")

#     def main(self, url):
#         try:
#             soup = self.fetch_wikipedia_content(url)

#             if soup is None:
#                 return

#             contentsoup = soup.find("div", id="mw-content-text")
#             soup = self.clean_html_tags(contentsoup)
#             soup = self.replace_math_elements(soup)
#             self.process_structure(contentsoup)
#             self.print_structure()
#             self.save_content()

#         except Exception as e:
#             print(f"Error in main: {e}")


# if __name__ == "__main__":
#     # url = "https://en.m.wikipedia.org/wiki/James_Bond"
#     # url = "https://en.wikipedia.org/wiki/Chemical_equation"
#     url = "https://en.wikipedia.org/wiki/Chemical_equilibrium"
#     scraper = WikipediaScraper()
#     scraper.main(url)


import logging
import re
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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
        self.citations = []

    # *DONE
    def clean_html_tags(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Cleans the given BeautifulSoup object by removing unnecessary HTML elements and formatting content for further processing.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

        Returns:
            BeautifulSoup: The cleaned BeautifulSoup object.
        """
        try:
            # Remove tags that generally contain non-essential content, such as scripts, styles, and links.
            for tag in soup.find_all(["script", "style", "link"]):
                try:
                    tag.decompose()
                except Exception as e:
                    logger.error(f"Error decomposing tag: {e}")

            # Handle <sup> tags, typically used for references or chemical notations.
            for tag in soup.find_all("sup"):
                try:
                    # Remove reference superscripts that start with "[" or are empty. (e.g., [1] is a reference tag)
                    if not tag.get_text() or tag.get_text().startswith("["):
                        tag.decompose()
                    else:
                        # Retain useful superscripts, e.g., chemical charge notation.
                        try:
                            tag.string = "`" + tag.string
                        except Exception:
                            logger.warning("Superscript tag string is empty or invalid.")
                except Exception as e:
                    logger.error(f"Error processing <sup> tag: {e}")

            # Remove empty paragraphs marked with a specific class (e.g., placeholder elements in Wikipedia).
            for tag in soup.find_all("p", class_="mw-empty-elt"):
                try:
                    tag.decompose()
                except Exception as e:
                    logger.error(f"Error decomposing empty paragraph: {e}")

            return soup

        except Exception as e:
            logger.critical(f"Critical error cleaning HTML tags: {e}")
            return soup

    # *DONE
    def fetch_wikipedia_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetches and parses the content of a Wikipedia page into a BeautifulSoup object.

        Args:
            url (str): The URL of the Wikipedia page to be fetched.

        Returns:
            Optional[BeautifulSoup]:
                - A BeautifulSoup object containing the parsed HTML content if the request is successful.
                - `None` if an error occurs during the fetch or parsing process.
        """
        try:
            # Fetch the page and parse it using Beautiful Soup.
            response = requests.get(url)

            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            logger.critical(f"Error fetching Wikipedia content: {e}")
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
            pattern = r"[\[\(\{\s](?:{com}*[A-Z][a-z]?{com}*)+[\]\)\s\.,]|^(?:{com}*[A-Z][a-z]?{com}*)+[\]\)\s\.,]|[\[\(\{\s](?:{com}*[A-Z][a-z]?{com}*)+$|^(?:{com}*[A-Z][a-z]?{com}*)+$".replace(
                "{com}", r"[\d\(\)\{\}\[\]+\u2212`]"
            )
            matches = re.finditer(pattern, text)

            # Filter matches to only include valid chemical formula patterns
            chemical_formulae = []

            for matche in matches:
                match = matche.group()
                # print("match:",match)
                # Split the match into potential element-symbol/number sequences
                elements_in_match = re.findall(r"[A-Z][a-z]?|\d+|\[|\]|\(|\)|\{|\}", match)
                valid = True
                i = 0
                j = 0
                # Check if the extracted elements are valid symbols and follow the rules
                while i < len(elements_in_match):
                    if elements_in_match[i] in ELEMENTS:
                        j += len(elements_in_match[i])
                        i += 1
                    elif elements_in_match[i] in {"[", "]", "(", ")", "{", "}"}:
                        # Skip brackets
                        i += 1
                    elif elements_in_match[i].isdigit():
                        i += 1
                        j += 1
                    else:
                        valid = False
                        break
                if valid:
                    if "`" not in match and (
                        j == 1
                        or (
                            j == 2
                            and (
                                "He" in match
                                or "At" in match
                                or "As" in match
                                or "No" in match
                                or "As" in match
                                or "In" in match
                                or "II" in match
                            )
                        )
                    ):
                        continue
                    chemical_formulae.append(matche.span())
            return chemical_formulae
        except Exception as e:
            print(f"Error in finding chemical formula: {e}")

    def mhchem_to_tts(self, mhchem_notation):
        try:
            mhchem_notation = (
                mhchem_notation.replace("(s)", " solid ")
                .replace("(aq)", " aqueous ")
                .replace("(g)", " gaseous ")
                .replace("(l)", " liquid ")
                .replace(" v ", " precipitate ")
                .replace("(v)", " precipitate ")
                .replace("(^)", " released as gas ")
                .replace(" ^ ", " released as gas ")
            )
            # Define regex patterns for elements, isotopes, bonds, arrows, and charges
            element_pattern = r"(\d*[A-Z][A-Za-z\d]+)"  # Matches consecutive elements and digits
            isotope_pattern = r"([^a-zA-z])\^(\{\d+\})"  # Matches isotopes, e.g., ^{14}C
            bond_pattern = r"bond\{-\}|bond\{=\}|bond\{#\}|bond\{~\}"  # Matches bonds (single, double, triple, etc.)
            arrow_pattern = r"->|=>|<-|<=>"  # Matches reaction arrows
            charge_pattern = r"\^(\d*[+\-]|\{\d*[+\-]\}|\{\d*\}[+\-])"  # Matches charges, e.g., ^{+1}
            charge_pattern2 = r"([A-Z]|[a-z]|\d)([+\-])"
            power_pattern = r"\^(\d+)"
            # Step 1: Convert elements, e.g., "Cl" to "C l"
            readable = re.sub(element_pattern, lambda m: " ".join(m.group(1)), mhchem_notation)

            # Step 2: Handle isotopes, converting them to "14 C" etc.
            readable = re.sub(
                isotope_pattern,
                lambda m: f"{m.group(1)} isotope {m.group(2).replace('{', '').replace('}', '')} ",
                readable,
            )

            # Step 3: Handle bonds, converting them to words like "single bond", "double bond"
            bond_conversion = {
                "bond{-}": " single bond ",
                "bond{=}": " double bond ",
                "bond{#}": " triple bond ",
                "bomd{~}": " resonance bond ",
            }
            readable = re.sub(bond_pattern, lambda m: bond_conversion[m.group(0)], readable)

            # Step 4: Handle arrows, converting them to phrases like "yields", "reversible reaction"
            arrow_conversion = {
                "->": " yields ",
                "=>": " yields with condition ",
                "<-": " reversible ",
                "<=>": " is in equilibrium with ",
            }
            readable = re.sub(arrow_pattern, lambda m: arrow_conversion[m.group(0)], readable)

            # Step 5: Handle charges
            readable = re.sub(
                charge_pattern,
                lambda m: f" charge {m.group(1).replace('{', '').replace('}', '').replace('+', '').replace('-', '')} {'positive' if '+' in m.group(1) else 'negative'}",
                readable,
            )

            readable = re.sub(
                charge_pattern2,
                lambda m: f" {m.group(1)} charge {m.group(2).replace('+', '').replace('-', '')} {'positive' if '+' in m.group(2) else 'negative'}",
                readable,
            )

            readable = re.sub(power_pattern, lambda m: f" raised to the power {m.group(1)} ", readable)

            return readable
        except Exception as e:
            print(f"Error in mhchem_to_tts: {e}")

    # !REASON
    def chem_in_math_element(self, latex):
        try:
            ce = re.finditer(r"\\ce", latex)
            lis = []
            lis1 = []
            for c in ce:
                a = c.end() + 1
                if len(lis) >= 1 and lis[-1][1] > a:
                    continue
                b = a
                i = 1
                while i != 0:
                    a += 1
                    if latex[a] == "{":
                        i += 1
                    elif latex[a] == "}":
                        i -= 1
                # print(latex[b+1:a])
                lis.append([b - 3, a])
                lis1.append(self.mhchem_to_tts(latex[b + 1 : a]))
            i = len(lis) - 1
            # print(latex)
            while i != -1:
                a = lis[i][0]
                b = lis[i][1]
                latex = latex[:a] + "ce{" + lis1[i] + latex[b:]
                i -= 1
            # print(latex)

            return latex

        except Exception as e:
            print(f"Error in chem_in_math: {e}")

    # !REASON
    def replace_math_elements(self, soup):
        """Replace all math elements with a placeholder."""
        try:
            for math_element in soup.find_all("span", class_="mwe-math-element"):
                latex = math_element.img.get("alt")

                # Processing chemistry stuff in \ce latex
                # ! WHY, Example??
                latex = self.chem_in_math_element(latex)

                latex = latex.replace("/", "//")
                url = "http://localhost:8080/api"
                data = {"latexInput": latex}
                response = requests.post(url, json=data)
                text = "Math Equation"
                if response.status_code == 200:  # 201 Created
                    text = response.json()["output"]
                    # ! WHY
                    text = text.replace("cap ", " ").replace(" normal ", " ")
                    # print(text)
                else:
                    print(f"Error: {response.status_code}")
                # Converting dd tag to p tag since most maths equations are inside dd tag.
                if math_element.parent.name == "dd":
                    par = math_element.parent.parent
                    math_element.parent.replace_with(text)
                    par.name = "p"
                else:
                    math_element.clear()
                    math_element.string = text
                    # print(math_element)
            return soup
        except Exception as e:
            print(f"Error replacing math elements: {e}")
            return soup

    def process_chemical_formulae(self, chemical_formulae, text):
        try:
            # Covert common roman numeral to number
            text = text.replace("III", " 3 ").replace("II", " 2")
            offset = 0
            for formu in chemical_formulae:
                formula = text[formu[0] + offset : formu[1] + offset]
                # print('Original:',formula)
                off = 0
                i = 0
                while i + off < len(formula):
                    length = len(formula)
                    c = formula[i + off]
                    if c == "[" or c == "{":
                        formula = formula[: i + off] + "\nopen bracket\n" + formula[i + off + 1 :]
                    elif c == "]" or c == "}":
                        formula = formula[: i + off] + "\nclosed bracket\n" + formula[i + off + 1 :]
                    elif c.isalpha():
                        if c == "C" and formula[i + off + 1] == "o":
                            formula = formula[: i + off] + " Cobalt " + formula[i + off + 2 :]
                        else:
                            formula = formula[: i + off] + " " + c + " " + formula[i + off + 1 :]
                    elif c.isdigit():
                        j = i + 1
                        while j + off < len(formula) and formula[j + off].isdigit():
                            j += 1
                        formula = formula[: i + off] + " " + formula[i + off : j + off] + " " + formula[j + off :]
                        i += j - i - 1
                    elif c == "+":
                        formula = formula[: i + off] + "positive" + formula[i + off + 1 :]
                    elif c == "\u2212":
                        formula = formula[: i + off] + "negative" + formula[i + off + 1 :]
                    elif c == "`":
                        formula = formula[: i + off] + " charge " + formula[i + off + 1 :]
                    # elif c == "(":
                    #     formula = formula[: i + off] + c + formula[i + off + 1 :]
                    # elif c == ")":
                    #     formula = formula[: i + off] + c + formula[i + off + 1 :]
                    off += len(formula) - length
                    i += 1
                # print('Processed:',formula)
                text = text[: formu[0] + offset] + formula + text[formu[1] + offset :]
                offset += off
            text = (
                text.replace("(I)", "1")
                .replace("(aq)", " aqueous ")
                .replace("(s)", " solid ")
                .replace("(g)", " gaseous ")
                .replace("(v)", " vapour ")
            )
            return text
        except Exception as e:
            print(f"Error in processing chemical formula: {e}")

    # *DONE
    def process_chem2_su(self, soup: BeautifulSoup) -> None:
        """
        Processes chemical equations with both superscript and subscript tags
        by swapping the text content of two nested <span> elements.

        Args:
            soup (BeautifulSoup): A BeautifulSoup object representing the HTML document.
        """
        spans = soup.find_all("span", class_="template-chem2-su")

        for span in spans:
            try:
                nested_spans = span.find_all("span")

                if len(nested_spans) == 2:
                    original_text = nested_spans[0].get_text()
                    nested_spans[0].string = nested_spans[1].get_text()
                    nested_spans[1].string = "`" + original_text

            except Exception as error:
                print(f"Error in processing chemical superscript/subscript: {error}")

    def process_dd_for_chem(self, soup):
        try:
            dds = soup.find_all("dd")
            for dd in dds:
                chemspan = dd.find_all("span", class_="chemf")
                for span in chemspan:
                    text = span.get_text()
                    text = (
                        text.replace("(s)", " solid ")
                        .replace("(aq)", " aqueous ")
                        .replace("(g)", " gaseous ")
                        .replace("(v)", " vapour ")
                        .replace("(l)", " liquid ")
                    )
                    formula = self.find_chemical_formulae(text)
                    text = self.process_chemical_formulae(formula, text)
                    text = (
                        text.replace("\u2192", "yields")
                        .replace("\u2191", "released as gas")
                        .replace("\u2193", "as precipitate")
                        .replace("\u21cc", "is in equilibrium with")
                        .replace("\u21c4", "is in equilibrium with")
                    )
                    # print('dd:',text)
                    span.string = text
                    dd.name = "p"
                if not chemspan and not dd.find("span"):
                    text = dd.get_text()
                    formula = self.find_chemical_formulae(text)
                    text = self.process_chemical_formulae(formula, text)
                    text = (
                        text.replace("\u2192", "yields")
                        .replace("\u2191", "released as gas")
                        .replace("\u2193", "as precipitate")
                        .replace("\u21cc", "is in equilibrium with")
                        .replace("\u21c4", "is in equilibrium with")
                    )
                    dd.string = text
                    dd.name = "p"
        except Exception as e:
            print(f"Error in dd_for_chem: {e}")

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
            for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "cite", "figure"]):
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
                    elif element.name == "cite":
                        for a in element.find_all("a"):
                            if isinstance(a.get_text(), str):
                                self.link[a.get_text()] = a.get("href")
                        for img in element.find_all("img"):
                            self.images.append([img.get("src"), img.get("alt")])
                        self.citations.append(element.get_text())

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

    # *DONE
    def fetch_short_description(self, soup: BeautifulSoup) -> str:
        try:
            short_desc_div = soup.find("div", class_="shortdescription")

            if short_desc_div:
                return short_desc_div.get_text(strip=True)

            return "No short description available."

        except Exception as e:
            print(f"Error fetching short description: {e}")
            return "No short description available."

    # *DONE
    def save_content(self, filename: str = "output.txt") -> None:
        """Save content in an accessible format."""
        print(self.images)
        try:
            with open(filename, "w", encoding="utf-8") as file:
                for content in self.content:
                    file.write(f"{content}\n")

        except Exception as e:
            print(f"Error saving content: {str(e)}")

    def print_structure(self):
        response = ""
        for i in self.content:
            # print(i)
            response += i + " "

        return response

    def main(self, url: str) -> str:
        try:
            soup = self.fetch_wikipedia_content(url)
            if soup is None:
                return
            # div with id mw-content-text contains main content of the article
            contentsoup = soup.find("div", id="mw-content-text")

            # clean unneccesary tags
            soup = self.clean_html_tags(contentsoup)

            # replace math elements present in form of latex to blind friendly format using MathJax library
            soup = self.replace_math_elements(soup)

            # process chemical elements containing both superscript and subscript
            self.process_chem2_su(soup)

            self.process_dd_for_chem(soup)
            self.process_structure(contentsoup)
            response = self.print_structure()
            self.save_content()
            return response
            # for i in self.images:
            # print(i)
        except Exception as e:
            print(f"Error in main: {e}")


if __name__ == "__main__":
    # url = "https://en.wikipedia.org/wiki/James_Bond"
    # url = "https://en.wikipedia.org/wiki/Equation"
    # url = "https://en.wikipedia.org/wiki/Cube_(algebra)"
    # url = "https://en.wikipedia.org/wiki/Chemical_equation"
    url = "https://en.wikipedia.org/wiki/Chemical_equilibrium"
    # url = "https://en.wikipedia.org/wiki/Ion"
    scraper = WikipediaScraper()
    scraper.main(url)
