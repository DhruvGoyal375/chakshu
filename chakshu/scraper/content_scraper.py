import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from core.logger import setup_logger
from core.utils import get_env_variable
from joblib import Parallel, delayed

# logger = setup_logger(__name__)
logger = setup_logger(__name__)


class WikipediaScraper:
    def __init__(self):
        self.link = {}
        self.figure = []
        self.images = []
        self.headings = []
        self.content = []
        self.citations = []

    def clean_html_tags(self, soup: BeautifulSoup) -> BeautifulSoup:
        try:
            # Remove tags that generally contain non-essential content, such as scripts, styles, and links.
            for tag in soup.find_all(["script", "style"]):
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
            logger.error(f"Error in mhchem_to_tts: {e}")

    def _render_latex(self, latex: str) -> str:
        """Calls the LaTeX rendering API for a single LaTeX string."""
        url = get_env_variable("LATEX_TO_TEXT_BASE_URL", "http://localhost:8080/api")
        data = {"latexInput": latex}
        try:
            response = requests.post(url, json=data, timeout=15)
            if response.status_code == 200:
                text = response.json()["output"]
                return text.replace("cap ", " ").replace(" normal ", " ")
            logger.error(f"Error from LaTeX API: {response.status_code}, falling back to placeholder.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling LaTeX rendering API: {e}, falling back to placeholder.")
        # Fallback to returning the original LaTeX string in a readable format
        return f"Math Equation: {latex}"

    def replace_math_elements(self, soup):
        """Finds all math elements and replaces them with rendered text in parallel."""
        try:
            math_elements = soup.find_all("span", class_="mwe-math-element")
            if not math_elements:
                return soup

            # 1. Prepare LaTeX inputs
            latex_inputs = []
            for math_element in math_elements:
                latex = math_element.img.get("alt")
                latex = self.chem_in_math_element(latex)
                latex = latex.replace("/", "//")
                latex_inputs.append(latex)

            # 2. Render all LaTeX strings in parallel using a thread pool
            logger.info(f"Rendering {len(latex_inputs)} math elements in parallel.")
            rendered_texts = Parallel(n_jobs=-1, backend="threading")(
                delayed(self._render_latex)(latex) for latex in latex_inputs
            )
            logger.info("Finished rendering math elements.")

            # 3. Replace the original math elements with the rendered text
            for math_element, text in zip(math_elements, rendered_texts):
                # Converting dd tag to p tag since most maths equations are inside dd tag.
                if math_element.parent.name == "dd":
                    par = math_element.parent.parent
                    math_element.parent.replace_with(text)
                    par.name = "p"
                else:
                    math_element.clear()
                    math_element.string = text
            return soup
        except Exception as e:
            logger.error(f"Error replacing math elements: {e}")
            return soup

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
                lis.append([b - 3, a])
                lis1.append(self.mhchem_to_tts(latex[b + 1 : a]))
            i = len(lis) - 1
            while i != -1:
                a = lis[i][0]
                b = lis[i][1]
                latex = latex[:a] + "ce{" + lis1[i] + latex[b:]
                i -= 1
            return latex

        except Exception as e:
            logger.error(f"Error in chem_in_math: {e}")

    def fetch_wikipedia_content(self, url: str) -> Optional[BeautifulSoup]:
        try:
            headers = {"User-Agent": "Chakshu/1.0 (https://github.com/DhruvGoyal375/chakshu; dhruvgoyal375@gmail.com)"}
            # Fetch the page and parse it using Beautiful Soup.
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.critical(f"Error fetching Wikipedia content: {e}")
            return None

    def extract_links_images(self, element):
        try:
            for i in element.find_all("a"):
                try:
                    if isinstance(i.get_text(), str):
                        self.link[i.get_text()] = i.get("href")
                except Exception as e:
                    logger.error(f"Error processing link: {e}")
            for i in element.find_all("img"):
                try:
                    self.images.append([i.get("src"), i.get("alt")])
                except Exception as e:
                    logger.error(f"Error processing image: {e}")
        except Exception as e:
            logger.error(f"Error extracting links and images: {e}")

    def process_paragraph(self, element):
        text = element.get_text()
        self.extract_links_images(element)
        self.content.append(f"Paragraph: {text} \n ")
        for cite in element.find_all("cite"):
            cite.decompose()
        return

    def process_ul(self, element):
        if "mw-gallery-traditional" in element.get("class", []):
            for item in element.find_all("div", ["thumb", "gallerytext"]):
                if "thumb" in item.get("class", []):
                    self.content.append(item.find_all("img")[0].get("alt", ""))
                else:
                    self.content.append(item.get_text())
        else:
            if element.find_parent("table", class_="vevent"):
                return
            for item in element.find_all("li"):
                self.content.append(item.get_text())

            self.content.append("\n ")

    def process_structure(self, soup):
        try:
            self.content = []
            for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "table", "ul", "ol", "figure"]):
                try:
                    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        if element.get("id") in ["Bibliography", "External_links"]:
                            break
                        self.extract_links_images(element)
                        text = element.get_text(strip=True)
                        if text == "Contents":
                            continue
                        self.content.append(f"Heading: {text} \n ")

                    elif element.name == "p":
                        self.extract_links_images(element)
                        self.process_paragraph(element)

                    elif element.name == "table":
                        # TODO: Write function to process table tag
                        pass

                    elif element.name == "ul":
                        self.extract_links_images(element)
                        self.process_ul(element)

                    elif element.name == "ol":
                        # get all the references
                        if "references" in element.get("class", []):
                            for li in element.find_all("li"):
                                self.citations.append(li.get_text(strip=True))

                    elif element.name == "figure":
                        if element.img and element.img.get("src"):
                            figcaption = element.figcaption.get_text() if element.figcaption else ""
                            self.figure.append([element.img.get("src"), figcaption])

                except Exception as inner_e:
                    logger.error(f"Error processing element: {inner_e}")
        except Exception as e:
            logger.error(f"Error in process_structure: {e}")

    def fetch_short_description(self, soup: BeautifulSoup) -> str:
        try:
            short_desc_div = soup.find("div", class_="shortdescription")

            if short_desc_div:
                return short_desc_div.get_text(strip=True)

            return "No short description available."

        except Exception as e:
            logger.error(f"Error fetching short description: {e}")
            return "No short description available."

    def print_structure(self):
        response = ""

        for i in self.content:
            response += i + " "

        return response

    def main(self, url: str) -> Optional[str]:
        try:
            if not isinstance(url, str) or not url.startswith("http"):
                logger.error(f"Invalid URL provided: {url}")
                return None

            soup = self.fetch_wikipedia_content(url)

            if soup is None:
                logger.error("Failed to fetch Wikipedia content.")
                return None

            contentsoup = soup.find("div", class_="mw-body-content")

            if contentsoup is None:
                logger.error("Could not find 'mw-body-content' div in the page.")
                return None

            contentsoup = self.clean_html_tags(contentsoup)
            contentsoup = self.replace_math_elements(contentsoup)
            logger.info("Successfully fetched and cleaned Wikipedia content.")
            self.process_structure(contentsoup)
            response = self.print_structure()
            return response

        except Exception as e:
            logger.critical(f"Error in main: {e}")
            return None


if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/James_Bond"
    scraper = WikipediaScraper()
    result = scraper.main(test_url)
    # print(result)

    if result:
        logger.info("Scraping completed successfully.")
    else:
        logger.error("Scraping failed.")
