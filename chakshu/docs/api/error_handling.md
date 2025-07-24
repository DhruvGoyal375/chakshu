# Error Handling

This guide provides comprehensive information about error handling in the Chakshu API, including error types, response formats, and best practices for handling errors in client applications.

## Error Response Format

All API errors follow a consistent JSON structure:

```json
{
  "status": "error",
  "message": "Human-readable error description",
  "error_code": "OPTIONAL_ERROR_CODE"
}
```

### Response Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | Always "error" for error responses |
| `message` | string | Yes | Human-readable error description |
| `error_code` | string | No | Machine-readable error code (when applicable) |

## HTTP Status Codes

Chakshu API uses standard HTTP status codes to indicate the type of error:

| Code | Status | Description | When It Occurs |
|------|--------|-------------|----------------|
| 400 | Bad Request | Invalid request parameters | Missing/invalid parameters, malformed URLs |
| 404 | Not Found | Resource not found | Invalid endpoints, non-existent articles |
| 429 | Too Many Requests | Rate limit exceeded | Too many requests from same IP |
| 500 | Internal Server Error | Server-side error | Unexpected server errors |
| 503 | Service Unavailable | External service unavailable | AI services down, Wikipedia unavailable |

## Error Categories

### 1. Parameter Validation Errors

These errors occur when request parameters are missing, invalid, or malformed.

#### Missing Required Parameters

**Scenario**: Required parameter not provided

**Example Request**:
```bash
curl "http://localhost:8000/api/search/"
```

**Response**:
```json
{
  "status": "error",
  "message": "Missing required parameter: q"
}
```

**HTTP Status**: 400 Bad Request

#### Parameter Too Long

**Scenario**: Parameter exceeds maximum length

**Example Request**:
```bash
curl "http://localhost:8000/api/search/?q=very_long_query_that_exceeds_255_characters..."
```

**Response**:
```json
{
  "status": "error",
  "message": "q is too long (max 255 characters)"
}
```

**HTTP Status**: 400 Bad Request

#### Invalid URL Format

**Scenario**: Wikipedia URL doesn't match required format

**Example Request**:
```bash
curl "http://localhost:8000/api/select/?link=https://example.com/invalid"
```

**Response**:
```json
{
  "status": "error",
  "message": "Invalid Wikipedia URL format. Must be a full 'https://en.wikipedia.org/wiki/...' URL."
}
```

**HTTP Status**: 400 Bad Request

#### Invalid Option Value

**Scenario**: Processing option is not in valid range (1-6)

**Example Request**:
```bash
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=7"
```

**Response**:
```json
{
  "status": "error",
  "message": "Invalid option. Please select a valid option (1-6)."
}
```

**HTTP Status**: 400 Bad Request

### 2. Rate Limiting Errors

These errors occur when the API rate limits are exceeded.

#### Rate Limit Exceeded

**Scenario**: Too many requests from the same IP address

**Response**:
```json
{
  "status": "error",
  "message": "Rate limit exceeded. Please try again later.",
  "error_code": "RATE_LIMIT_EXCEEDED"
}
```

**HTTP Status**: 429 Too Many Requests

**Headers**:
```
Retry-After: 60
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
```

### 3. External Service Errors

These errors occur when external services (AI models, Wikipedia, etc.) are unavailable.

#### AI Service Unavailable

**Scenario**: Ollama or image captioning service is down

**Response**:
```json
{
  "status": "error",
  "message": "Failed to connect to external services.",
  "error_code": "SERVICE_UNAVAILABLE"
}
```

**HTTP Status**: 503 Service Unavailable

#### Wikipedia API Error

**Scenario**: Wikipedia API is unavailable or returns errors

**Response**:
```json
{
  "status": "error",
  "message": "Failed to fetch content from Wikipedia.",
  "error_code": "WIKIPEDIA_UNAVAILABLE"
}
```

**HTTP Status**: 503 Service Unavailable

#### LaTeX Service Error

**Scenario**: LaTeX-to-text conversion service is unavailable

**Response**:
```json
{
  "status": "error",
  "message": "Mathematical content processing unavailable.",
  "error_code": "LATEX_SERVICE_UNAVAILABLE"
}
```

**HTTP Status**: 503 Service Unavailable

### 4. Content Processing Errors

These errors occur during content processing operations.

#### No Content Found

**Scenario**: Article exists but has no processable content

**Response**:
```json
{
  "status": "error",
  "message": "No processable content found for the requested option.",
  "error_code": "NO_CONTENT"
}
```

**HTTP Status**: 404 Not Found

#### Processing Timeout

**Scenario**: Content processing takes too long

**Response**:
```json
{
  "status": "error",
  "message": "Content processing timed out. Please try again.",
  "error_code": "PROCESSING_TIMEOUT"
}
```

**HTTP Status**: 500 Internal Server Error

#### Partial Processing Failure

**Scenario**: Some content processed successfully, others failed

**Response**:
```json
{
  "status": "success",
  "type": "image_captions",
  "content": [
    {
      "image_url": "https://example.com/image1.jpg",
      "final_caption": "Successfully processed image"
    }
  ],
  "article_url": "https://en.wikipedia.org/wiki/Article",
  "article_title": "Article",
  "image_count": 1,
  "processing_warnings": [
    "Failed to process 2 images due to service unavailability"
  ]
}
```

**Note**: This is still a success response, but includes warnings about partial failures.

### 5. Server Errors

These are unexpected server-side errors.

#### Internal Server Error

**Scenario**: Unexpected server-side error

**Response**:
```json
{
  "status": "error",
  "message": "An internal server error occurred. Please try again later.",
  "error_code": "INTERNAL_ERROR"
}
```

**HTTP Status**: 500 Internal Server Error

## Error Handling Best Practices

### 1. Client-Side Error Handling

#### JavaScript Example

```javascript
class ChakshuAPIError extends Error {
  constructor(message, status, errorCode) {
    super(message);
    this.name = 'ChakshuAPIError';
    this.status = status;
    this.errorCode = errorCode;
  }
}

async function makeAPIRequest(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.status === 'error') {
      throw new ChakshuAPIError(
        data.message, 
        response.status, 
        data.error_code
      );
    }
    
    return data;
  } catch (error) {
    if (error instanceof ChakshuAPIError) {
      handleAPIError(error);
    } else {
      handleNetworkError(error);
    }
    throw error;
  }
}

function handleAPIError(error) {
  switch (error.status) {
    case 400:
      console.error('Invalid request:', error.message);
      // Show user-friendly validation error
      break;
    case 429:
      console.error('Rate limited:', error.message);
      // Implement retry with backoff
      break;
    case 503:
      console.error('Service unavailable:', error.message);
      // Show service unavailable message
      break;
    default:
      console.error('API error:', error.message);
  }
}

function handleNetworkError(error) {
  console.error('Network error:', error);
  // Show network connectivity error
}
```

#### Python Example

```python
import requests
import time
from typing import Optional

class ChakshuAPIError(Exception):
    def __init__(self, message: str, status_code: int, error_code: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code

class ChakshuClient:
    def __init__(self, base_url: str, max_retries: int = 3):
        self.base_url = base_url
        self.max_retries = max_retries
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: dict) -> dict:
        url = f"{self.base_url}/{endpoint}/"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                data = response.json()
                
                if data.get('status') == 'error':
                    raise ChakshuAPIError(
                        data['message'], 
                        response.status_code, 
                        data.get('error_code')
                    )
                
                return data
                
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    raise ChakshuAPIError("Request timed out", 408)
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.ConnectionError:
                if attempt == self.max_retries - 1:
                    raise ChakshuAPIError("Connection failed", 503)
                time.sleep(2 ** attempt)
                
            except ChakshuAPIError as e:
                if e.status_code == 429:  # Rate limited
                    retry_after = response.headers.get('Retry-After', 60)
                    time.sleep(int(retry_after))
                    continue
                raise
        
        raise ChakshuAPIError("Max retries exceeded", 500)

    def search(self, query: str) -> dict:
        try:
            return self._make_request('search', {'q': query})
        except ChakshuAPIError as e:
            self._handle_error(e, 'search')
            raise

    def _handle_error(self, error: ChakshuAPIError, operation: str):
        if error.status_code == 400:
            print(f"Invalid {operation} request: {error}")
        elif error.status_code == 429:
            print(f"Rate limited during {operation}: {error}")
        elif error.status_code == 503:
            print(f"Service unavailable during {operation}: {error}")
        else:
            print(f"Unexpected error during {operation}: {error}")
```

### 2. Retry Strategies

#### Exponential Backoff

```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Usage
const result = await retryWithBackoff(async () => {
  return await fetch('/api/search/?q=Python');
});
```

#### Rate Limit Handling

```javascript
async function handleRateLimit(response) {
  if (response.status === 429) {
    const retryAfter = response.headers.get('Retry-After') || 60;
    console.log(`Rate limited. Waiting ${retryAfter} seconds...`);
    await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
    return true; // Indicate retry should happen
  }
  return false;
}
```

### 3. User Experience Considerations

#### Error Messages for Users

```javascript
function getUserFriendlyError(error) {
  const errorMessages = {
    'RATE_LIMIT_EXCEEDED': 'Too many requests. Please wait a moment and try again.',
    'SERVICE_UNAVAILABLE': 'The service is temporarily unavailable. Please try again later.',
    'WIKIPEDIA_UNAVAILABLE': 'Wikipedia is currently unavailable. Please try again later.',
    'NO_CONTENT': 'No content available for this article and option.',
    'PROCESSING_TIMEOUT': 'Processing is taking longer than expected. Please try again.',
    'INVALID_URL': 'Please provide a valid Wikipedia article URL.',
    'MISSING_PARAMETER': 'Please provide all required information.'
  };
  
  return errorMessages[error.error_code] || 'An unexpected error occurred. Please try again.';
}
```

#### Progress Indicators

```javascript
async function processWithProgress(articleUrl, option) {
  const progressElement = document.getElementById('progress');
  
  try {
    progressElement.textContent = 'Starting processing...';
    
    const result = await fetch(`/api/process/?link=${encodeURIComponent(articleUrl)}&option=${option}`);
    const data = await result.json();
    
    if (data.status === 'error') {
      progressElement.textContent = getUserFriendlyError(data);
      return null;
    }
    
    progressElement.textContent = 'Processing complete!';
    return data;
    
  } catch (error) {
    progressElement.textContent = 'Processing failed. Please try again.';
    throw error;
  }
}
```

### 4. Logging and Monitoring

#### Client-Side Error Logging

```javascript
function logError(error, context) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    error: {
      message: error.message,
      status: error.status,
      errorCode: error.errorCode
    },
    context: context,
    userAgent: navigator.userAgent,
    url: window.location.href
  };
  
  // Send to logging service
  console.error('Chakshu API Error:', errorLog);
  
  // Optional: Send to external logging service
  // sendToLoggingService(errorLog);
}
```

#### Server-Side Error Monitoring

Monitor these error patterns:
- High rate of 429 errors (may need rate limit adjustment)
- Frequent 503 errors (external service issues)
- Spike in 500 errors (server problems)
- Unusual error patterns (potential attacks)

## Testing Error Scenarios

### Manual Testing

```bash
# Test missing parameter
curl "http://localhost:8000/api/search/"

# Test invalid URL
curl "http://localhost:8000/api/select/?link=invalid-url"

# Test invalid option
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=10"

# Test rate limiting (make multiple rapid requests)
for i in {1..10}; do
  curl "http://localhost:8000/api/search/?q=test$i" &
done
```

### Automated Testing

```python
import pytest
import requests

def test_missing_parameter():
    response = requests.get('http://localhost:8000/api/search/')
    assert response.status_code == 400
    data = response.json()
    assert data['status'] == 'error'
    assert 'Missing required parameter' in data['message']

def test_invalid_url():
    response = requests.get('http://localhost:8000/api/select/?link=invalid')
    assert response.status_code == 400
    data = response.json()
    assert data['status'] == 'error'
    assert 'Invalid Wikipedia URL format' in data['message']

def test_invalid_option():
    url = 'http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=10'
    response = requests.get(url)
    assert response.status_code == 400
    data = response.json()
    assert data['status'] == 'error'
    assert 'Invalid option' in data['message']
```

## Error Recovery Strategies

### Graceful Degradation

```javascript
async function getArticleContent(articleUrl) {
  try {
    // Try to get full content with images
    const fullContent = await processContent(articleUrl, 3);
    const images = await processContent(articleUrl, 4);
    
    return {
      content: fullContent.content,
      images: images.content,
      hasImages: true
    };
  } catch (error) {
    if (error.errorCode === 'SERVICE_UNAVAILABLE') {
      // Fall back to text-only content
      try {
        const textContent = await processContent(articleUrl, 3);
        return {
          content: textContent.content,
          images: [],
          hasImages: false,
          warning: 'Image processing unavailable'
        };
      } catch (textError) {
        // Fall back to summary
        const summary = await processContent(articleUrl, 2);
        return {
          content: summary.content,
          images: [],
          hasImages: false,
          warning: 'Full content unavailable, showing summary'
        };
      }
    }
    throw error;
  }
}
```

### Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}

// Usage
const circuitBreaker = new CircuitBreaker();

async function safeAPICall(url) {
  return await circuitBreaker.call(async () => {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  });
}
```

## Next Steps

- **[API Overview](index.md)** - Return to API documentation overview
- **[Response Examples](response_examples.md)** - See complete response examples
- **[Features Documentation](../features/content_processing.md)** - Learn about accessibility features