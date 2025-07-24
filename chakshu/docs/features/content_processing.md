# Content Processing Features

Chakshu's content processing capabilities are designed from the ground up to make Wikipedia articles accessible to blind and visually impaired users. This page details the accessibility-focused features and how they work.

## Overview

Chakshu transforms complex Wikipedia articles into structured, screen-reader-friendly content through six specialized processing options:

1. **Short Description** - Quick article overview
2. **Page Summary** - Detailed introduction
3. **Full Content** - Complete article with structured formatting
4. **Image Captions** - AI-generated visual descriptions
5. **Table Analysis** - Screen-reader friendly table descriptions
6. **References** - Citations and bibliography

## Accessibility-First Design Principles

### 1. Structured Content Hierarchy

All text content is processed to create a clear, navigable structure:

```
Heading: Main Article Title
  Paragraph: Introduction paragraph...
  
  Heading: Section Title
    Paragraph: Section content...
    
    Heading: Subsection Title
      Paragraph: Subsection content...
```

**Benefits for Screen Readers:**
- Clear heading navigation (H1, H2, H3 levels)
- Proper content flow and structure
- Easy section jumping and navigation

### 2. Clean, Readable Text

Wikipedia's complex markup is cleaned and optimized:

**Before Processing:**
```html
<p>The <a href="/wiki/Python">Python</a> programming language<sup>[1]</sup> 
was created by <a href="/wiki/Guido_van_Rossum">Guido van Rossum</a>.</p>
```

**After Processing:**
```
Paragraph: The Python programming language was created by Guido van Rossum.
```

**Accessibility Improvements:**
- Reference links removed (available separately via option 6)
- HTML tags stripped
- Proper spacing and formatting
- Link text preserved without navigation clutter

### 3. Mathematical Content Conversion

Complex mathematical equations are converted to readable text:

**LaTeX Input:**
```latex
E = mc^2
```

**Readable Output:**
```
E equals m c raised to the power 2
```

**Chemical Formulas:**
```
Input: H₂SO₄
Output: H 2 S O 4 (sulfuric acid)
```

## Content Processing Options Detailed

### Option 1: Short Description

**Purpose**: Provides a brief, one-sentence description of the article topic.

**Example Output**:
```json
{
  "content": "Country in Southern Europe"
}
```

**Accessibility Features**:
- Concise overview for quick understanding
- Perfect for search result previews
- Helps users decide if article is relevant

**Use Cases**:
- Article selection assistance
- Quick topic identification
- Search result summaries

### Option 2: Page Summary

**Purpose**: Returns the Wikipedia article's lead section (introduction).

**Example Output**:
```json
{
  "content": "Italy, officially the Italian Republic, is a country in Southern and Western Europe. It consists of a peninsula that extends into the Mediterranean Sea, with the Alps on its northern land border, as well as nearly 800 islands, notably Sicily and Sardinia..."
}
```

**Accessibility Features**:
- Complete introduction without navigation clutter
- Mathematical content converted to readable text
- Proper sentence structure and flow
- Reference markers removed

**Processing Steps**:
1. Fetch article summary via Wikipedia API
2. Clean HTML tags and formatting
3. Convert mathematical notation
4. Remove reference links
5. Optimize for text-to-speech

### Option 3: Full Content

**Purpose**: Provides the complete article content with structured formatting.

**Example Output**:
```
Heading: Italy

Paragraph: Italy, officially the Italian Republic, is a country in Southern and Western Europe...

Heading: Etymology

Paragraph: The name Italy comes from the ancient Greek name...

Heading: History

Heading: Prehistory and antiquity

Paragraph: Thousands of years before the Roman Empire...
```

**Accessibility Features**:
- **Hierarchical Structure**: Clear heading levels for navigation
- **Content Segmentation**: Paragraphs clearly marked
- **List Processing**: Bullet points and numbered lists properly formatted
- **Mathematical Conversion**: Equations converted to readable text
- **Chemical Notation**: Scientific formulas made accessible

**Processing Pipeline**:
1. **HTML Parsing**: Extract content from Wikipedia's HTML
2. **Structure Analysis**: Identify headings, paragraphs, lists
3. **Content Cleaning**: Remove navigation elements, references
4. **Mathematical Processing**: Convert LaTeX and chemical formulas
5. **Accessibility Formatting**: Add structure markers for screen readers

### Option 4: Image Captions

**Purpose**: Generates detailed, accessibility-focused descriptions of all images.

**Example Output**:
```json
{
  "content": [
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Aston.db5.coupe.300pix.jpg",
      "final_caption": "The image showcases a classic Aston Martin DB5, a sleek silver sports car, parked on a paved area. The car's polished chrome grille and round headlights are prominently visible, reflecting its iconic design. In the background, other cars and greenery are faintly visible, suggesting a parking lot or a similar outdoor setting."
    }
  ],
  "image_count": 7
}
```

**AI-Powered Features**:
- **Context-Aware Descriptions**: Uses article title and existing captions for context
- **Detailed Visual Analysis**: Comprehensive descriptions of visual elements
- **Accessibility Language**: Optimized for screen readers and text-to-speech
- **High-Resolution Processing**: Analyzes highest quality images available

**Processing Workflow**:
1. **Image Discovery**: Find all images on the Wikipedia page
2. **Metadata Extraction**: Gather existing captions and descriptions
3. **High-Resolution Fetching**: Get the best quality version of each image
4. **AI Analysis**: Process images with Qwen2.5-VL vision model
5. **Caption Generation**: Create detailed, accessible descriptions
6. **Quality Assurance**: Filter out failed or low-quality captions

**Caption Quality Features**:
- **Spatial Relationships**: Describes positioning and layout
- **Color and Lighting**: Mentions relevant visual characteristics
- **Context Integration**: Incorporates article topic and existing metadata
- **Action Descriptions**: Explains what people or objects are doing
- **Background Details**: Includes relevant environmental information

### Option 5: Table Analysis

**Purpose**: Converts complex visual tables into screen-reader friendly descriptions.

**Example Output**:
```json
{
  "content": {
    "analyses": [
      {
        "success": true,
        "analysis": "The table provides a chronological list of James Bond novels and their associated short story collections and editions.\n\n### Table Purpose:\nThe table provides a chronological list of James Bond novels...\n\n### Column Headers:\n- **Left Column:** Publication Year and Novel Title\n- **Right Column:** Publication Year and Short Story Collection/Edition Title\n\n### Data Rows:\n\n| Left Column | Right Column |\n|---|---|\n| 1953 Casino Royale[22] | 1960 For Your Eyes Only[29] |\n| 1954 Live and Let Die[23] | 1961 Thunderball[30] |"
      }
    ],
    "tables_found": 3,
    "successful_analyses": 3
  }
}
```

**Advanced Processing**:
- **Screenshot Capture**: Uses Playwright to capture table images
- **AI Vision Analysis**: Qwen2.5-VL model analyzes table structure
- **Structured Description**: Converts visual layout to readable format
- **Data Extraction**: Identifies headers, rows, and relationships

**Table Processing Pipeline**:
1. **Page Analysis**: Scan Wikipedia page for table elements
2. **Screenshot Capture**: Take high-quality images of each table
3. **AI Processing**: Analyze table structure and content
4. **Description Generation**: Create accessible table descriptions
5. **Quality Validation**: Ensure descriptions are complete and accurate

**Accessibility Benefits**:
- **Structure Explanation**: Describes table purpose and organization
- **Header Identification**: Clearly identifies column and row headers
- **Data Relationships**: Explains how data points relate to each other
- **Navigation Guidance**: Provides logical reading order for table data

### Option 6: References and Citations

**Purpose**: Extracts all references and citations from the article.

**Example Output**:
```json
{
  "content": [
    "Ian Fleming, The New Yorker, 21 April 1962",
    "Reilly, Liam (20 February 2025). \"Amazon MGM Studios takes creative control of James Bond franchise\". CNN. CNN Business.",
    "Macintyre, Ben (5 April 2008). \"Bond – the real Bond\". The Times. p. 36."
  ],
  "citation_count": 220
}
```

**Features**:
- **Complete Bibliography**: All article references extracted
- **Clean Formatting**: Optimized for screen reader consumption
- **Source Information**: Authors, titles, dates, and publications included
- **Academic Standards**: Proper citation format maintained

## Performance Optimizations

### Parallel Processing

**Image Processing**:
```python
# Multiple images processed simultaneously
processed_results = Parallel(n_jobs=-1, backend="threading")(
    delayed(_process_single_image)(img, all_captions) 
    for img in images_to_process
)
```

**Benefits**:
- Faster processing of multiple images
- Better resource utilization
- Reduced overall response time

### Intelligent Caching

**Cache Strategy**:
- **Text Content**: 1 hour cache (articles change infrequently)
- **Image Captions**: Indefinite cache (images rarely change)
- **Table Analysis**: 1 hour cache (balance between freshness and performance)
- **Search Results**: 1 hour cache (search patterns are often repeated)

**Cache Benefits**:
- Faster response times for repeated requests
- Reduced load on external services
- Better user experience

### Error Handling and Graceful Degradation

**Robust Processing**:
```python
def safe_get_short_description(url):
    try:
        desc = get_short_description(url)
        return desc if desc else "Short description not available."
    except Exception as e:
        logger.error(f"Error getting short description for {url}: {str(e)}")
        return "Error fetching description."
```

**Benefits**:
- Continues processing even if some operations fail
- Provides partial results when possible
- Clear error messages for users

## Integration with Assistive Technologies

### Screen Reader Optimization

**Structured Output**:
- Proper heading hierarchy (H1 → H2 → H3)
- Clear content boundaries
- Logical reading order
- Skip navigation options

**ARIA-Compatible Structure**:
```html
<article>
  <h1>Article Title</h1>
  <section>
    <h2>Section Title</h2>
    <p>Paragraph content...</p>
  </section>
</article>
```

### Text-to-Speech Optimization

**Speech-Friendly Features**:
- Natural sentence structure
- Proper punctuation for pauses
- Phonetic spelling for complex terms
- Abbreviation expansion

**Mathematical Content**:
- Equations converted to speakable format
- Chemical formulas with proper pronunciation
- Units and measurements clearly stated

### Voice Command Integration

**Structured Navigation**:
- "Read next section"
- "Skip to references"
- "Describe images"
- "Read table data"

## Quality Assurance

### Content Validation

**Text Processing**:
- HTML tag removal verification
- Mathematical conversion accuracy
- Reference link cleanup
- Proper formatting validation

**AI-Generated Content**:
- Caption relevance checking
- Table description completeness
- Error detection and filtering
- Quality scoring and ranking

### Accessibility Testing

**Screen Reader Testing**:
- NVDA compatibility
- JAWS compatibility
- VoiceOver compatibility
- Proper navigation flow

**Text-to-Speech Testing**:
- Natural speech patterns
- Proper pronunciation
- Appropriate reading speed
- Clear content boundaries

## Future Enhancements

### Planned Features

**Enhanced AI Capabilities**:
- Multi-language image captioning
- Video content description
- Interactive element descriptions
- Real-time content updates

**Improved Accessibility**:
- Braille output formatting
- Customizable reading preferences
- Voice command integration
- Personalized content filtering

**Performance Improvements**:
- Edge caching for global users
- Predictive content processing
- Adaptive quality based on connection
- Progressive content loading

### Community Contributions

**Open Source Development**:
- Accessibility expert feedback
- Screen reader user testing
- Multi-language support
- Platform-specific optimizations

## Next Steps

- **[Image Captioning](image_captioning.md)** - Deep dive into AI-powered image descriptions
- **[Table Analysis](table_analysis.md)** - Detailed table processing capabilities
- **[Mathematical Content](mathematical_content.md)** - LaTeX and formula conversion
- **[API Documentation](../api/index.md)** - Technical API reference