import difflib

import requests
from bs4 import BeautifulSoup


def extract_paragraph_with_hyperlinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all paragraphs (<p> tags) in the page
    paragraphs = soup.find_all("p")

    extracted_paragraph = ""
    for p in paragraphs:
        extracted_paragraph += str(p)  # This will include the <a> tags as-is

    return extracted_paragraph


def extract_hyperlinks_from_paragraph(paragraph):
    # Extract all <a> tags and their 'href' attributes
    soup = BeautifulSoup(paragraph, "html.parser")
    links = {}
    for a_tag in soup.find_all("a", href=True):
        link_text = a_tag.get_text(strip=True)  # Get the anchor text
        href = a_tag["href"]  # Get the hyperlink URL
        # Include only valid Wikipedia links
        if href.startswith("/wiki/") and ":" not in href:
            full_link = f"https://en.wikipedia.org{href}"
            links[link_text] = full_link  # Map the link text to the full URL
    return links


def get_closest_hyperlinks(user_query, hyperlink_map, n=5):
    """Get the closest 'n' hyperlinks using edit distance"""
    hyperlinks = list(hyperlink_map.keys())
    matches = difflib.get_close_matches(user_query, hyperlinks, n=n)
    return matches


def main():
    # Sample Wikipedia page (you can change this to any Wikipedia URL)
    url = "https://en.wikipedia.org/wiki/James_Bond"  # Example Wikipedia URL
    print(f"Fetching content and hyperlinks from: {url}")

    # Extract the full paragraph, including hyperlinks
    paragraph = extract_paragraph_with_hyperlinks(url)

    print("\nExtracted paragraph with hyperlinks:")
    print(paragraph)  # This prints the paragraph as-is, including hyperlinks

    # Extract individual hyperlinks from the paragraph
    hyperlink_map = extract_hyperlinks_from_paragraph(paragraph)

    if not hyperlink_map:
        print("No valid hyperlinks found in this paragraph.")
        return

    # Display all the hyperlinks found
    print("\nHere are the hyperlinks extracted from the paragraph:")
    for link_text, full_link in hyperlink_map.items():
        print(f"{link_text}: {full_link}")

    # Ask user for input
    user_query = input("\nWhat word or phrase do you have a doubt about? ")

    # Get the closest 'n' hyperlinks (start with top 5)
    closest_links = get_closest_hyperlinks(user_query, hyperlink_map, n=len(hyperlink_map))

    if closest_links:
        for closest_link in closest_links:
            print(f"This is the closest link I found: {
                  closest_link} -> {hyperlink_map[closest_link]}")
            response = input("Do you want to know about this link? (yes/no) ")

            if response.lower() == "yes":
                print(f"Showing details for {closest_link}: {
                      hyperlink_map[closest_link]}")
                break  # Stop once the user confirms they want this link
            else:
                print("Moving to the next closest match...")
    else:
        print("No matching hyperlink found.")


if __name__ == "__main__":
    main()
