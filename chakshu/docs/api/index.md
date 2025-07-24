# API Documentation

Chakshu provides a simple yet powerful REST API for accessing Wikipedia content in an accessibility-focused format. The API is designed to work seamlessly with screen readers and text-to-speech systems.

## API Overview

The Chakshu API follows a three-step workflow:

1. **Search** - Find Wikipedia articles matching your query
2. **Select** - Choose an article and see available processing options
3. **Process** - Extract specific content types from the selected article

## Base URL

```
http://localhost:8000/api/
```

For production deployments, replace `localhost:8000` with your domain.

## Authentication

Currently, Chakshu API does not require authentication. All endpoints are publicly accessible.

!!! note "Rate Limiting"
    The API includes rate limiting to prevent abuse. Default limits are 5 requests per minute per IP address for certain endpoints.

## Quick Start

Here's a complete example of using the API:

```bash
# 1. Search for articles about Python
curl "http://localhost:8000/api/search/?q=Python"

# 2. Select the first result and get options
curl "http://localhost:8000/api/select/?link=https://en.wikipedia.org/wiki/Python"

# 3. Get the article summary (option 2)
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=2"
```

## API Endpoints

### Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/search/` | GET | Search Wikipedia articles |
| `/select/` | GET | Get processing options for an article |
| `/process/` | GET | Extract specific content from an article |

### Content Processing Options

When you call the `/process/` endpoint, you can specify one of these options:

| Option | Content Type | Description |
|--------|--------------|-------------|
| 1 | Short Description | Brief article overview |
| 2 | Summary | Detailed Wikipedia summary |
| 3 | Full Content | Complete article text |
| 4 | Image Captions | AI-generated image descriptions |
| 5 | Table Analysis | Screen-reader friendly table descriptions |
| 6 | References | Citations and bibliography |

## Response Format

All API responses follow a consistent JSON structure:

```json
{
  "status": "success|error",
  "message": "Human-readable message",
  "data": "Response-specific data",
  // Additional fields based on endpoint
}
```

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  // Endpoint-specific data fields
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Description of what went wrong",
  "error_code": "OPTIONAL_ERROR_CODE"
}
```

## Content Types

### Text Content
Most endpoints return structured text optimized for screen readers:

- **Headings** are clearly marked with "Heading:" prefix
- **Paragraphs** are separated with proper spacing
- **Lists** are formatted with clear item separation
- **Mathematical content** is converted to readable text

### Image Captions
AI-generated image descriptions include:

- **Detailed visual descriptions** of the image content
- **Context information** from Wikipedia metadata
- **Accessibility-focused language** suitable for screen readers

### Table Analysis
Complex Wikipedia tables are converted to:

- **Structured descriptions** of table purpose and content
- **Row-by-row data** in readable format
- **Column header information** for context

## Error Handling

The API includes comprehensive error handling:

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters or malformed request |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | External service unavailable |

### Error Response Examples

**Invalid URL Format:**
```json
{
  "status": "error",
  "message": "Invalid Wikipedia URL format. Must be a full 'https://en.wikipedia.org/wiki/...' URL."
}
```

**Missing Required Parameter:**
```json
{
  "status": "error",
  "message": "Missing required parameter: q"
}
```

**Rate Limit Exceeded:**
```json
{
  "status": "error",
  "message": "Rate limit exceeded. Please try again later."
}
```

## Performance Considerations

### Caching
- Search results are cached for 1 hour
- Processed content is cached for 1 hour
- Image captions are cached indefinitely (until updated)

### Parallel Processing
- Image processing uses parallel workers for better performance
- Multiple content types can be processed simultaneously
- Timeouts prevent long-running requests from blocking the service

### Response Times
Typical response times:

| Endpoint | Expected Time | Notes |
|----------|---------------|-------|
| Search | < 2 seconds | Depends on Google Search API |
| Select | < 500ms | Cached after first request |
| Process (text) | < 3 seconds | Depends on article length |
| Process (images) | 10-30 seconds | AI processing required |
| Process (tables) | 15-45 seconds | Screenshot + AI analysis |

## Best Practices

### For Client Applications

1. **Handle Async Operations**: Image and table processing can take time
2. **Implement Retry Logic**: For network errors and timeouts
3. **Cache Responses**: Avoid repeated requests for the same content
4. **Show Progress Indicators**: For long-running operations
5. **Validate URLs**: Ensure Wikipedia URLs before sending to API

### For Screen Reader Integration

1. **Use Structured Content**: Leverage the heading hierarchy in responses
2. **Announce Loading States**: Inform users when processing is happening
3. **Handle Long Content**: Break up long responses for better navigation
4. **Provide Skip Options**: Allow users to skip to different content sections

### Example Client Code

**JavaScript/Fetch Example:**
```javascript
async function searchWikipedia(query) {
  try {
    const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    
    if (data.status === 'success') {
      return data.results;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Search failed:', error);
    throw error;
  }
}

async function getImageCaptions(articleUrl) {
  try {
    const response = await fetch(`/api/process/?link=${encodeURIComponent(articleUrl)}&option=4`);
    const data = await response.json();
    
    if (data.status === 'success') {
      return data.content;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error('Image caption processing failed:', error);
    throw error;
  }
}
```

**Python/Requests Example:**
```python
import requests
from urllib.parse import quote

def search_wikipedia(query):
    """Search for Wikipedia articles."""
    url = f"http://localhost:8000/api/search/?q={quote(query)}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'success':
            return data['results']
        else:
            raise Exception(data['message'])
            
    except requests.RequestException as e:
        print(f"Search failed: {e}")
        raise

def get_article_summary(article_url):
    """Get article summary."""
    url = f"http://localhost:8000/api/process/?link={quote(article_url)}&option=2"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'success':
            return data['content']
        else:
            raise Exception(data['message'])
            
    except requests.RequestException as e:
        print(f"Summary processing failed: {e}")
        raise
```

## Next Steps

- **[Search API](search_api.md)** - Detailed search endpoint documentation
- **[Processing API](processing_api.md)** - Content processing endpoints
- **[Response Examples](response_examples.md)** - Complete response examples
- **[Error Handling](error_handling.md)** - Comprehensive error reference