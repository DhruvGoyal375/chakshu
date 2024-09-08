import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views import View
from googlesearch import search
from joblib import Parallel, delayed
from scraper.views import get_short_description
from text_to_speech.views import convert_text_to_speech

from .wiki_api import WikiAPI


def convert_to_audio_response(text):
    audio_bytes = convert_text_to_speech(text)

    response = HttpResponse(audio_bytes, content_type="audio/wav")
    response["Content-Disposition"] = 'attachment; filename="short_description.wav"'
    return response


class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        query_for_wiki = query + " site:en.wikipedia.org"

        if query:
            search_results_list = list(search(query_for_wiki, num_results=10))

            descriptions = Parallel(n_jobs=-1)(delayed(get_short_description)(url) for url in search_results_list)

            results = [
                f"{index + 1}. {url.split('/')[-1]}: {description}."
                for index, (url, description) in enumerate(zip(search_results_list, descriptions))
            ]
            response_text = "Select the article you want to read: " + " ".join(results)

            response_audio = convert_to_audio_response(response_text[:300])
            return response_audio

        return HttpResponse("Please provide a search query using the 'q' parameter.")


class SelectLinkView(View):
    def get(self, request):
        selected_link = request.GET.get("link")

        if selected_link:
            options = (
                "1. Read short description of the page.\n"
                "2. Read summary of the page.\n"
                "3. Read the whole page.\n"
                "4. Read only captions of the images present on the page.\n"
                "5. Read all the References present on the page.\n"
            )
            response = convert_to_audio_response(options)
            return response
        else:
            return HttpResponse("Please provide the 'link' parameter.")


class ProcessOptionView(View):
    def get(self, request):
        selected_link = request.GET.get("link")
        option = request.GET.get("option")

        if selected_link and option:
            try:
                option = int(option)
                page_title = selected_link.split("/")[-1]

                if option == 1:
                    """get short description of page"""
                    short_description = get_short_description(selected_link)
                    response = convert_to_audio_response(short_description)
                    return response

                elif option == 2:
                    """get summary of page"""
                    mediawiki_api = WikiAPI(user_agent="Chakshu (chakshu@pec.edu.in)")
                    summary = mediawiki_api.get_page_summary(page_title)
                    response = convert_to_audio_response(summary[:300])
                    return response

                page = requests.get(selected_link)
                soup = BeautifulSoup(page.content, "html.parser")

                if option == 3:
                    """get full page content"""
                    full_text = soup.get_text()
                    return HttpResponse(f"Full page content:\n\n{full_text}")

                elif option == 4:
                    """get captions of all images"""
                    captions = "\n".join([img.get("alt", "No caption") for img in soup.find_all("img")])
                    return HttpResponse(f"Image captions:\n\n{captions}")

                elif option == 5:
                    """"get the references"""
                    references = "\n".join(
                        [
                            ref.get_text()
                            for ref in soup.find_all("li", {"id": lambda x: x and x.startswith("cite_note")})
                        ]
                    )
                    return HttpResponse(f"References on the page:\n\n{references}")

                else:
                    return HttpResponse("Invalid option. Please select a valid option (1-4).")

            except ValueError:
                return HttpResponse("Invalid option. Please provide a valid number for the option.")

        else:
            return HttpResponse("Please provide both 'link' and 'option' parameters.")
