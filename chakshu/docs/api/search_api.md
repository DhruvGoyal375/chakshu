# Search API

The Search API is the entry point for discovering Wikipedia articles. It uses Google Search scoped to Wikipedia to find relevant articles based on user queries.

## Endpoint

```
GET /api/search/
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query (max 255 characters) |

### Parameter Details

**Query (`q`)**
- **Format**: URL-encoded string
- **Max Length**: 255 characters
- **Examples**: `Python`, `Machine Learning`, `Climate Change`
- **Special Characters**: Automatically URL-encoded by most HTTP clients

## Request Examples

### Basic Search
```bash
curl "http://localhost:8000/api/search/?q=Python"
```

### Search with Spaces
```bash
curl "http://localhost:8000/api/search/?q=Machine%20Learning"
# Or let curl handle encoding:
curl "http://localhost:8000/api/search/?q=Machine Learning"
```

### Search with Special Characters
```bash
curl "http://localhost:8000/api/search/?q=C%2B%2B%20programming"
# Searches for "C++ programming"
```

## Response Format

### Success Response

```json
{
  "status": "success",
  "message": "Select the article you want to read",
  "results": [
    {
      "id": 1,
      "url": "https://en.wikipedia.org/wiki/Article_Title",
      "title": "Article Title",
      "short_description": "Brief description of the article"
    }
  ],
  "query": "original search query",
  "result_count": 5
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Always "success" for valid requests |
| `message` | string | Human-readable status message |
| `results` | array | Array of search result objects (max 9 results) |
| `query` | string | Original search query (URL-decoded) |
| `result_count` | integer | Number of results returned |

### Result Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Sequential identifier (1-9) |
| `url` | string | Full Wikipedia article URL |
| `title` | string | Article title (extracted from URL, spaces restored) |
| `short_description` | string | Brief article description or "No short description available." |

## Search Behavior

### Search Process
1. **Query Processing**: Input is URL-decoded and validated
2. **Google Search**: Query is scoped to `site:en.wikipedia.org`
3. **Result Filtering**: Duplicate URLs are removed while preserving order
4. **Description Fetching**: Short descriptions are fetched in parallel for performance
5. **Response Assembly**: Results are formatted and returned

### Search Scope
- **Language**: English Wikipedia only (`en.wikipedia.org`)
- **Result Limit**: Maximum 9 results per query
- **Deduplication**: Duplicate URLs are automatically removed
- **Ordering**: Results maintain Google Search ranking order

### Performance Optimizations
- **Parallel Processing**: Short descriptions are fetched using parallel workers
- **Caching**: Search results are cached for 1 hour
- **Timeout Handling**: Individual description fetches have timeouts to prevent blocking

## Error Handling

### Missing Query Parameter

**Request:**
```bash
curl "http://localhost:8000/api/search/"
```

**Response:**
```json
{
  "status": "error",
  "message": "Missing required parameter: q"
}
```

### Query Too Long

**Request:**
```bash
curl "http://localhost:8000/api/search/?q=very_long_query_that_exceeds_255_characters..."
```

**Response:**
```json
{
  "status": "error",
  "message": "q is too long (max 255 characters)"
}
```

### No Results Found

**Request:**
```bash
curl "http://localhost:8000/api/search/?q=xyznonexistentquery123"
```

**Response:**
```json
{
  "status": "success",
  "message": "No results found.",
  "results": [],
  "query": "xyznonexistentquery123",
  "result_count": 0
}
```

### Service Error

**Response:**
```json
{
  "status": "error",
  "message": "An error occurred while processing your search request."
}
```

## Usage Examples

### JavaScript/Fetch
```javascript
async function searchWikipedia(query) {
  const url = `/api/search/?q=${encodeURIComponent(query)}`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.status === 'success') {
      console.log(`Found ${data.result_count} results for "${data.query}"`);
      return data.results;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Search failed:', error);
    throw error;
  }
}

// Usage
searchWikipedia('Artificial Intelligence')
  .then(results => {
    results.forEach(result => {
      console.log(`${result.id}. ${result.title}`);
      console.log(`   ${result.short_description}`);
      console.log(`   ${result.url}`);
    });
  })
  .catch(error => console.error(error));
```

### Python/Requests
```python
import requests
from urllib.parse import quote

def search_wikipedia(query):
    """Search Wikipedia articles using Chakshu API."""
    url = f"http://localhost:8000/api/search/?q={quote(query)}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'success':
            print(f"Found {data['result_count']} results for '{data['query']}'")
            return data['results']
        else:
            raise Exception(data['message'])
            
    except requests.RequestException as e:
        print(f"Search failed: {e}")
        raise

# Usage
try:
    results = search_wikipedia('Machine Learning')
    for result in results:
        print(f"{result['id']}. {result['title']}")
        print(f"   {result['short_description']}")
        print(f"   {result['url']}")
        print()
except Exception as e:
    print(f"Error: {e}")
```

### cURL Examples
```bash
# Basic search
curl "http://localhost:8000/api/search/?q=Python"

# Search with JSON output formatting
curl -s "http://localhost:8000/api/search/?q=Python" | jq '.'

# Extract just the titles
curl -s "http://localhost:8000/api/search/?q=Python" | jq -r '.results[].title'

# Get the first result URL
curl -s "http://localhost:8000/api/search/?q=Python" | jq -r '.results[0].url'
```

## Best Practices

### Query Optimization
- **Be Specific**: More specific queries return more relevant results
- **Use Keywords**: Include important keywords related to your topic
- **Avoid Very Long Queries**: Keep queries under 255 characters
- **Handle Special Characters**: Let your HTTP client handle URL encoding

### Error Handling
- **Check Status**: Always check the `status` field in responses
- **Handle Empty Results**: Check `result_count` before processing results
- **Implement Retries**: For network errors and timeouts
- **Validate Input**: Ensure queries are not empty or too long

### Performance Considerations
- **Cache Results**: Avoid repeated searches for the same query
- **Batch Processing**: If searching multiple terms, space out requests
- **Handle Timeouts**: Set appropriate timeout values for your use case

### Accessibility Integration
- **Announce Results**: Inform screen reader users about the number of results
- **Provide Context**: Read out article titles and descriptions clearly
- **Enable Navigation**: Allow users to navigate through results easily

## Rate Limiting

The Search API includes rate limiting to prevent abuse:

- **Default Limit**: 5 requests per minute per IP address
- **Rate Limit Headers**: Check response headers for current limits
- **Exceeded Limit**: Returns HTTP 429 with retry information

### Handling Rate Limits
```javascript
async function searchWithRetry(query, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || 60;
        console.log(`Rate limited. Retrying after ${retryAfter} seconds...`);
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }
      
      return await response.json();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
    }
  }
}
```

## Integration with Other Endpoints

The Search API is typically used as the first step in a three-part workflow:

1. **Search** → Find articles matching your query
2. **[Select](processing_api.md#select-endpoint)** → Choose an article and see processing options
3. **[Process](processing_api.md#process-endpoint)** → Extract specific content from the chosen article

### Complete Workflow Example
```python
# 1. Search for articles
results = search_wikipedia('Artificial Intelligence')

# 2. Select the first result
if results:
    article_url = results[0]['url']
    
    # 3. Get processing options
    options_response = requests.get(f"/api/select/?link={quote(article_url)}")
    
    # 4. Process the article (get summary)
    summary_response = requests.get(f"/api/process/?link={quote(article_url)}&option=2")
```

## Next Steps

- **[Content Processing API](processing_api.md)** - Learn about the Select and Process endpoints
- **[Response Examples](response_examples.md)** - See complete response examples
- **[Error Handling](error_handling.md)** - Comprehensive error handling guide