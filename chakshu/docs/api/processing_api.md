# Content Processing API

The Content Processing API consists of two endpoints that work together to extract and process Wikipedia article content in an accessibility-focused format.

## Select Endpoint

The Select endpoint provides available processing options for a chosen Wikipedia article.

### Endpoint
```
GET /api/select/
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `link` | string | Yes | Full Wikipedia article URL |

#### Parameter Details

**Link (`link`)**
- **Format**: Full Wikipedia URL
- **Pattern**: `https://en.wikipedia.org/wiki/Article_Title`
- **Max Length**: 500 characters
- **Validation**: Must be a valid English Wikipedia URL

### Request Examples

```bash
# Basic select request
curl "http://localhost:8000/api/select/?link=https://en.wikipedia.org/wiki/Python"

# URL-encoded link (recommended)
curl "http://localhost:8000/api/select/?link=https%3A//en.wikipedia.org/wiki/Python"
```

### Response Format

```json
{
  "status": "success",
  "message": "Select an option",
  "options": [
    {
      "id": 1,
      "description": "Read short description of the page"
    },
    {
      "id": 2,
      "description": "Read summary of the page"
    },
    {
      "id": 3,
      "description": "Read the full page content"
    },
    {
      "id": 4,
      "description": "Read captions of images on the page"
    },
    {
      "id": 5,
      "description": "Read tables on the page"
    },
    {
      "id": 6,
      "description": "Read references and citations on the page"
    }
  ],
  "article_url": "https://en.wikipedia.org/wiki/Python",
  "article_title": "Python"
}
```

## Process Endpoint

The Process endpoint extracts specific content types from Wikipedia articles based on the selected option.

### Endpoint
```
GET /api/process/
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `link` | string | Yes | Full Wikipedia article URL |
| `option` | integer | Yes | Processing option (1-6) |

#### Parameter Details

**Link (`link`)**
- Same validation as Select endpoint

**Option (`option`)**
- **Range**: 1-6
- **Type**: Integer
- **Options**:
  - `1`: Short description
  - `2`: Page summary  
  - `3`: Full content
  - `4`: Image captions
  - `5`: Table analysis
  - `6`: References and citations

### Request Examples

```bash
# Get article summary (option 2)
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=2"

# Get image captions (option 4)
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=4"

# Get table analysis (option 5)
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=5"
```

## Processing Options Detailed

### Option 1: Short Description

Returns a brief description of the Wikipedia article.

**Response Format:**
```json
{
  "status": "success",
  "type": "short_description",
  "content": "Brief article description",
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title"
}
```

**Use Cases:**
- Quick article overview
- Search result previews
- Navigation assistance

### Option 2: Page Summary

Returns the Wikipedia article summary (lead section).

**Response Format:**
```json
{
  "status": "success",
  "type": "summary",
  "content": "Detailed article summary...",
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title"
}
```

**Features:**
- Complete lead section content
- Cleaned and formatted for screen readers
- Mathematical content converted to readable text

### Option 3: Full Content

Returns the complete article content with structured formatting.

**Response Format:**
```json
{
  "status": "success",
  "type": "full_content",
  "content": "Heading: Introduction\n\nParagraph: Article content...",
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title"
}
```

**Content Structure:**
- **Headings**: Prefixed with "Heading: "
- **Paragraphs**: Prefixed with "Paragraph: "
- **Lists**: Properly formatted list items
- **Mathematical Content**: Converted to readable text
- **Chemical Formulas**: Converted to spoken format

### Option 4: Image Captions

Returns AI-generated descriptions of all images on the page.

**Response Format:**
```json
{
  "status": "success",
  "type": "image_captions",
  "content": [
    {
      "image_url": "https://upload.wikimedia.org/...",
      "final_caption": "Detailed AI-generated description..."
    }
  ],
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title",
  "image_count": 5
}
```

**AI Features:**
- **Context-Aware**: Uses article title and existing captions for context
- **Detailed Descriptions**: Comprehensive visual descriptions
- **Accessibility Focused**: Optimized for screen readers
- **High Resolution**: Processes highest available image quality

**Processing Time**: 10-30 seconds depending on number of images

### Option 5: Table Analysis

Returns screen-reader friendly descriptions of all tables on the page.

**Response Format:**
```json
{
  "status": "success",
  "type": "tables",
  "content": {
    "url": "https://en.wikipedia.org/wiki/Article",
    "tables_found": 3,
    "analyses": [
      {
        "success": true,
        "analysis": "Detailed table description..."
      }
    ],
    "successful_analyses": 3,
    "failed_analyses": 0
  },
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title",
  "table_count": 3
}
```

**Processing Method:**
- **Screenshot Capture**: Uses Playwright to capture table images
- **AI Analysis**: Qwen2.5-VL model analyzes table structure and content
- **Accessibility Conversion**: Converts visual tables to readable descriptions

**Processing Time**: 15-45 seconds depending on number and complexity of tables

### Option 6: References and Citations

Returns all references and citations from the article.

**Response Format:**
```json
{
  "status": "success",
  "type": "citations",
  "content": [
    "Author, Title. Publication. Date.",
    "Another citation..."
  ],
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article Title",
  "citation_count": 25
}
```

**Features:**
- **Complete Bibliography**: All article references
- **Formatted Text**: Ready for screen reader consumption
- **Source Information**: Authors, titles, dates, and publications

## Error Handling

### Invalid URL Format

**Request:**
```bash
curl "http://localhost:8000/api/select/?link=https://example.com/invalid"
```

**Response:**
```json
{
  "status": "error",
  "message": "Invalid Wikipedia URL format. Must be a full 'https://en.wikipedia.org/wiki/...' URL."
}
```

### Missing Parameters

**Request:**
```bash
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python"
```

**Response:**
```json
{
  "status": "error",
  "message": "Missing required parameter: option"
}
```

### Invalid Option Value

**Request:**
```bash
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=7"
```

**Response:**
```json
{
  "status": "error",
  "message": "Invalid option. Please select a valid option (1-6)."
}
```

### Service Unavailable

When external AI services are unavailable:

**Response:**
```json
{
  "status": "error",
  "message": "Failed to connect to external services."
}
```

## Performance and Caching

### Caching Strategy
- **Text Content**: Cached for 1 hour
- **Image Captions**: Cached indefinitely (until article changes)
- **Table Analysis**: Cached for 1 hour
- **References**: Cached for 1 hour

### Performance Optimization
- **Parallel Processing**: Multiple images processed simultaneously
- **Timeout Handling**: Prevents long-running requests from blocking
- **Graceful Degradation**: Continues processing even if some operations fail

### Expected Response Times

| Option | Content Type | Typical Time | Notes |
|--------|--------------|--------------|-------|
| 1 | Short Description | < 1 second | Usually cached |
| 2 | Summary | 1-3 seconds | Text processing |
| 3 | Full Content | 2-5 seconds | Depends on article length |
| 4 | Image Captions | 10-30 seconds | AI processing required |
| 5 | Table Analysis | 15-45 seconds | Screenshot + AI analysis |
| 6 | References | 1-3 seconds | Text extraction |

## Usage Examples

### Complete Workflow (JavaScript)

```javascript
class ChakshuClient {
  constructor(baseUrl = 'http://localhost:8000/api') {
    this.baseUrl = baseUrl;
  }

  async search(query) {
    const response = await fetch(`${this.baseUrl}/search/?q=${encodeURIComponent(query)}`);
    return await response.json();
  }

  async getOptions(articleUrl) {
    const response = await fetch(`${this.baseUrl}/select/?link=${encodeURIComponent(articleUrl)}`);
    return await response.json();
  }

  async processContent(articleUrl, option) {
    const response = await fetch(`${this.baseUrl}/process/?link=${encodeURIComponent(articleUrl)}&option=${option}`);
    return await response.json();
  }

  async getArticleSummary(articleUrl) {
    return await this.processContent(articleUrl, 2);
  }

  async getImageCaptions(articleUrl) {
    return await this.processContent(articleUrl, 4);
  }

  async getTableAnalysis(articleUrl) {
    return await this.processContent(articleUrl, 5);
  }
}

// Usage example
async function demonstrateWorkflow() {
  const client = new ChakshuClient();

  try {
    // 1. Search for articles
    const searchResults = await client.search('Artificial Intelligence');
    console.log(`Found ${searchResults.result_count} articles`);

    if (searchResults.results.length > 0) {
      const firstArticle = searchResults.results[0];
      console.log(`Selected: ${firstArticle.title}`);

      // 2. Get processing options
      const options = await client.getOptions(firstArticle.url);
      console.log('Available options:', options.options);

      // 3. Get article summary
      const summary = await client.getArticleSummary(firstArticle.url);
      console.log('Summary:', summary.content.substring(0, 200) + '...');

      // 4. Get image captions (if needed)
      const images = await client.getImageCaptions(firstArticle.url);
      console.log(`Found ${images.image_count} images with captions`);
    }
  } catch (error) {
    console.error('Workflow failed:', error);
  }
}
```

### Python Client Example

```python
import requests
from urllib.parse import quote
import time

class ChakshuClient:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30

    def search(self, query):
        """Search for Wikipedia articles."""
        url = f"{self.base_url}/search/?q={quote(query)}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_options(self, article_url):
        """Get processing options for an article."""
        url = f"{self.base_url}/select/?link={quote(article_url)}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def process_content(self, article_url, option):
        """Process article content with specified option."""
        url = f"{self.base_url}/process/?link={quote(article_url)}&option={option}"
        
        # Longer timeout for AI processing
        timeout = 60 if option in [4, 5] else 30
        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def get_summary(self, article_url):
        """Get article summary."""
        return self.process_content(article_url, 2)

    def get_image_captions(self, article_url):
        """Get AI-generated image captions."""
        return self.process_content(article_url, 4)

    def get_table_analysis(self, article_url):
        """Get table analysis."""
        return self.process_content(article_url, 5)

# Usage example
def main():
    client = ChakshuClient()

    try:
        # Search for articles
        results = client.search('Machine Learning')
        print(f"Found {results['result_count']} articles")

        if results['results']:
            article = results['results'][0]
            print(f"Processing: {article['title']}")

            # Get summary
            summary = client.get_summary(article['url'])
            print(f"Summary length: {len(summary['content'])} characters")

            # Get image captions (this may take a while)
            print("Processing images...")
            images = client.get_image_captions(article['url'])
            print(f"Generated captions for {images['image_count']} images")

    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
```

## Best Practices

### For Client Applications

1. **Handle Long Operations**: Options 4 and 5 can take significant time
2. **Implement Progress Indicators**: Show users that processing is happening
3. **Cache Responses**: Avoid repeated requests for the same content
4. **Validate URLs**: Ensure Wikipedia URLs before sending to API
5. **Handle Errors Gracefully**: Provide meaningful error messages to users

### For Screen Reader Integration

1. **Announce Processing**: Inform users when long operations are starting
2. **Structure Content**: Use the heading hierarchy in full content responses
3. **Break Up Long Content**: Allow navigation through large responses
4. **Provide Summaries**: Offer content length information before reading

### Error Handling

```javascript
async function robustProcessing(articleUrl, option) {
  const maxRetries = 3;
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await processContent(articleUrl, option);
      
      if (result.status === 'success') {
        return result;
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      lastError = error;
      
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError;
}
```

## Next Steps

- **[Response Examples](response_examples.md)** - See complete response examples for all options
- **[Error Handling](error_handling.md)** - Comprehensive error handling guide
- **[Features Documentation](../features/content_processing.md)** - Learn about accessibility features