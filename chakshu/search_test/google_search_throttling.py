import random
import time
from googlesearch import search

def perform_search(queries, max_requests_per_minute):
    results = []
    processed_count = 0  # Counter for processed queries
    time_window = 60  # One minute time window
    last_request_time = 0  # Timestamp of the last request

    for query in queries:
        try:
            # Throttle requests dynamically
            time_since_last_request = time.time() - last_request_time
            if time_since_last_request < time_window / max_requests_per_minute:
                time.sleep((time_window / max_requests_per_minute) - time_since_last_request)

            print(f"Searching for: {query}")
            # Perform search and limit results to 10 per query
            for result in search(query, num_results=10):
                results.append(result)
                print(result)  # Output the result URL
            
            processed_count += 1  # Increment the counter after a successful search
            last_request_time = time.time()  # Update the timestamp
        except Exception as e:
            print(f"Error occurred while searching for '{query}': {e}")
            continue  # Skip to the next query without stopping the entire script

    print(f"Total queries processed: {processed_count}")
    return results, processed_count

# Base topics for generating queries
base_topics = [
    "best programming languages",
    "top machine learning algorithms",
    "what is artificial intelligence",
    "history of the Internet",
    "quantum computing explained",
    "cloud computing technologies",
    "how to build a website",
    "understanding blockchain",
    "data science applications",
    "cybersecurity best practices",
    "mobile app development",
    "software engineering principles",
    "agile methodology overview",
    "internet of things applications",
    "history of computer science",
]

# Generate 1000 random queries
num_queries = 1000
queries = [f"{random.choice(base_topics)} {random.choice(['2024', 'trends', 'guide', 'introduction', 'overview'])}" for _ in range(num_queries)]

# Set the maximum number of requests per minute (throttling limit)
max_requests_per_minute = 25  # 10 requests per minute

# Execute the search with throttling
search_results, total_processed = perform_search(queries, max_requests_per_minute)

# Optionally, save the results to a file
with open("search_results.txt", "w") as f:
    for result in search_results:
        f.write(result + "\n")

print(f"Search completed. Results saved to 'search_results.txt'.")
print(f"Total requests successfully processed: {total_processed}")
