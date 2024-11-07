import wikipediaapi


class WikiAPI:
    def __init__(self, user_agent, language="en"):
        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language)

    def get_page(self, title):
        return self.wiki.page(title)

    def page_exists(self, title):
        page = self.get_page(title)
        return page.exists()

    def get_page_summary(self, title):
        page = self.get_page(title)
        return page.summary

    def get_page_url(self, title):
        page = self.get_page(title)
        return page.fullurl

    def get_full_text(self, title):
        page = self.get_page(title)
        return page.text

    def get_page_sections(self, title):
        page = self.get_page(title)
        return page.sections

    def get_section_by_title(self, title, section_title):
        page = self.get_page(title)
        return page.section_by_title(section_title)

    def get_sections_by_title(self, title, section_title):
        page = self.get_page(title)
        return page.sections_by_title(section_title)

    def get_page_in_other_languages(self, title):
        page = self.get_page(title)
        return page.langlinks

    def get_page_links(self, title):
        page = self.get_page(title)
        return page.links

    def get_page_categories(self, title):
        page = self.get_page(title)
        return page.categories

    def get_pages_in_category(self, category_name, max_level=1):
        category_page = self.get_page(category_name)
        return self._get_category_members(category_page.categorymembers, max_level)

    def _get_category_members(self, categorymembers, level, max_level):
        members = []
        for c in categorymembers.values():
            members.append((c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                members.extend(self._get_category_members(c.categorymembers, level + 1, max_level))
        return members


if __name__ == "__main__":
    wiki_api = WikiAPI(user_agent="MyProjectName (merlin@example.com)")

    summary = wiki_api.get_page_summary("Python (programming language)")
    print(summary)
