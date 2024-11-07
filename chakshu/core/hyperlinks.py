from bs4 import BeautifulSoup
import requests
from rapidfuzz import process

# Extract hyperlinks and their text from the entire Wikipedia page
def extract_hyperlinks(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    # Find all <a> tags with 'href' attribute
    links = soup.find_all('a', href=True)
    # Create a dictionary {hyperlink: text}
    return {link.get('href'): link.text for link in links if link.text.strip()}

# Get closest matches based on the user's query
def get_closest_hyperlinks(user_query, hyperlink_map, limit=5):
    hyperlinks = list(hyperlink_map.values())
    # Using rapidfuzz to get the closest 'limit' matches
    matches = process.extract(user_query, hyperlinks, limit=limit)
    return matches

def main():
    # Example Wikipedia page (can be any valid URL)
    url = "https://en.wikipedia.org/wiki/Black_hole"
    response = requests.get(url)

    # Extract hyperlinks from the page content
    hyperlink_map = extract_hyperlinks(response.text)

    if not hyperlink_map:
        print("No hyperlinks found on the page.")
        return

    # Ask user for input
    user_query = input("What word do you have a doubt about? ")

    # Get the closest hyperlinks
    closest_links = get_closest_hyperlinks(user_query, hyperlink_map)

    if closest_links:
        for match in closest_links:
            closest_text = match[0]
            # Find the corresponding hyperlink
            for href, text in hyperlink_map.items():
                if text == closest_text:
                    print(f"This is the closest link I found: {text}")
                    response = input("Do you want to know about this link? (yes/no) ")
                    if response.lower() == 'yes':
                        print(f"Here is the description: {text}")
                        print(f"Click here: https://en.wikipedia.org{href}")  # Full clickable link
                        return  # Exit after showing the link
                    else:
                        print("Moving to the next option...")
    else:
        print("No matching hyperlink found.")

        
if __name__ == "__main__":
    main()
