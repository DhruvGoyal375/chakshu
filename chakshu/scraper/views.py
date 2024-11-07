from django.http import HttpResponse
from django.views import View

from .scraper import WikipediaScraper


def get_short_description(url):
    scraper = WikipediaScraper()
    soup = scraper.fetch_wikipedia_content(url)

    return scraper.fetch_short_description(soup)


class WikiSummaryScraper(View):
    def get(self, request):
        url = request.GET.get("url")
        if url:
            scraper = WikipediaScraper()
            soup = scraper.fetch_wikipedia_content(url)
            if soup is None:
                return HttpResponse("Failed to retrieve the page.", status=500)
            soup = scraper.clean_html_tags(soup)
            summary = self.get_summary(soup)
            return HttpResponse(f"Summary of the page:\n\n{summary}")
        else:
            return HttpResponse("Please provide the 'url' parameter.")

    def get_summary(self, soup):
        paragraphs = soup.find_all("p")
        summary = "\n".join([p.get_text(strip=True) for p in paragraphs[:2]])
        return summary


def get_citations(url):
    scraper = WikipediaScraper()
    soup = scraper.fetch_wikipedia_content(url)

    scraper.print_structure(soup)

    return scraper.citations


def get_full_content(url):
    scraper = WikipediaScraper()
    soup = scraper.fetch_wikipedia_content(url)

    whole_content = scraper.print_structure(soup)

    return whole_content
