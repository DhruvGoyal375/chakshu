import datetime
import re
from collections import OrderedDict

from captioner.views import fetch_and_process_images
from django.http import JsonResponse
from django.views import View
from googlesearch import search
from joblib import Parallel, delayed
from scraper.views import get_citations, get_full_content, get_short_description

from .wiki_api import WikiAPI

mediawiki_api = WikiAPI(user_agent="Chakshu (chakshu@pec.edu.in)")


class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        query.replace("%20", " ")
        query_for_wiki = query + " site:en.wikipedia.org"
        if query:
            search_results_list = list(search(query_for_wiki, num_results=5))
            print(search_results_list)
            print("SEARCH RESULTS FETCHED at, ", datetime.datetime.now())

            # Remove duplicates by converting the list to an OrderedDict, which maintains order
            search_results_list = list(OrderedDict.fromkeys(search_results_list))

            # Fetch descriptions in parallel for the filtered results
            short_descriptions = Parallel(n_jobs=-1)(delayed(get_short_description)(url) for url in search_results_list)
            print("SHORT DESCRIPTIONS FETCHED at, ", datetime.datetime.now())
            # Format the results into a response-friendly structure
            results = [
                {
                    "index": index + 1,
                    "url": url,
                    "title": " ".join(url.split("/")[-1].split("_")),
                    "short_description": short_description,
                }
                for index, (url, short_description) in enumerate(zip(search_results_list, short_descriptions))
            ]
            response_data = {"message": "Select the article you want to read", "results": results}

            return JsonResponse(response_data)

        return JsonResponse({"error": "Please provide a search query using the 'q' parameter."}, status=400)


class SelectLinkView(View):
    def get(self, request):
        selected_link = request.GET.get("link")

        if selected_link:
            options = [
                "Read short description of the page.",
                "Read summary of the page.",
                "Read the whole page.",
                "Read only captions of the images present on the page.",
                "Read all the References present on the page.",
            ]

            return JsonResponse({"message": "Select an option", "options": options})

        return JsonResponse({"error": "Please provide the 'link' parameter."}, status=400)


class ProcessOptionView(View):
    def get(self, request):
        selected_link = request.GET.get("link")
        option = request.GET.get("option")

        if selected_link and option:
            try:
                option = int(option)
                page_title = selected_link.split("/")[-1]

                # get short description of page
                if option == 1:
                    short_description = get_short_description(selected_link)
                    return JsonResponse({"short_description": short_description})

                # get summary of page
                elif option == 2:
                    summary = mediawiki_api.get_page_summary(page_title)

                    # Remove escape characters like \n, \t, etc.
                    clean_summary = re.sub(r"[\n\t\r]+", " ", summary).strip()

                    return JsonResponse({"summary": clean_summary})

                # get full page content
                if option == 3:
                    full_content = get_full_content(selected_link)
                    return JsonResponse({"text": full_content})
                    # full_page_content = soup.get_text()
                    # return JsonResponse({"full_page_content": full_page_content})

                # get captions of all images
                elif option == 4:
                    ls_captions = fetch_and_process_images(selected_link)
                    return JsonResponse({"text": ls_captions})

                # get the references
                elif option == 5:
                    citations = get_citations(selected_link)
                    return JsonResponse({"text": citations})

                return JsonResponse({"error": "Invalid option. Please select a valid option (1-5)."}, status=400)

            except ValueError:
                return JsonResponse(
                    {"error": "Invalid option. Please provide a valid number for the option."}, status=400
                )

        return JsonResponse({"error": "Please provide both 'link' and 'option' parameters."}, status=400)
