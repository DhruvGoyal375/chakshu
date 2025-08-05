## Search Query

**Endpoint:** `http://127.0.0.1:8000/api/search/?q=Italy`

**Response:**
```json
{
  "status": "success",
  "message": "Select the article you want to read",
  "results": [
    {
      "id": 1,
      "url": "https://en.wikipedia.org/wiki/Italy",
      "title": "Italy",
      "short_description": "Country in Southern Europe"
    },
    {
      "id": 2,
      "url": "https://en.wikipedia.org/wiki/Kingdom_of_Italy",
      "title": "Kingdom of Italy",
      "short_description": "Country in Southern Europe (1861–1946)"
    },
    {
      "id": 3,
      "url": "https://en.wikipedia.org/wiki/Italy_national_football_team",
      "title": "Italy national football team",
      "short_description": "Men's association football team"
    },
    {
      "id": 4,
      "url": "https://en.wikipedia.org/wiki/Economy_of_Italy",
      "title": "Economy of Italy",
      "short_description": "No short description available."
    },
    {
      "id": 5,
      "url": "https://en.wikipedia.org/wiki/Tourism_in_Italy",
      "title": "Tourism in Italy",
      "short_description": "No short description available."
    }
  ],
  "query": "Italy",
  "result_count": 5
}
```

<br>

## Select Link Query

**Endpoint:** `http://127.0.0.1:8000/api/select/?link=https://en.wikipedia.org/wiki/Italy`

**Response:**
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
  "article_url": "https://en.wikipedia.org/wiki/Italy",
  "article_title": "Italy"
}
```

<br>

## Process Link Query

### Option 1: Short Summary

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=1`

**Response:**

```json
{
  "status": "success",
  "type": "short_description",
  "content": "Country in Southern Europe",
  "article_url": "https://en.wikipedia.org/wiki/Italy",
  "article_title": "Italy"
}
```

### Option 2: Summary

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=2`

**Response:**

```json
{
  "status": "success",
  "type": "summary",
  "content": "Italy, officially the Italian Republic, is a country in Southern and Western Europe. It consists of a peninsula that extends into the Mediterranean Sea, with the Alps on its northern land border, as well as nearly 800 islands, notably Sicily and Sardinia. Italy shares land borders with France to the west; Switzerland and Austria to the north; Slovenia to the east; and the two enclaves of Vatican City and San Marino. It is the tenth-largest country in Europe by area, covering 301,340 km2 (116,350 sq mi), and the third-most populous member state of the European Union, with nearly 59 million inhabitants. Italy's capital and largest city is Rome; other major cities include Milan, Naples, Turin, Palermo, Bologna, Florence, Genoa, and Venice. The history of Italy goes back to numerous Italic peoples—notably including the ancient Romans, who conquered the Mediterranean world during the Roman Republic and ruled it for centuries during the Roman Empire. With the spread of Christianity, Rome became the seat of the Catholic Church and the Papacy. Barbarian invasions and other factors led to the decline and fall of the Western Roman Empire between late antiquity and the Early Middle Ages. By the 11th century, Italian city-states and maritime republics expanded, bringing renewed prosperity through commerce and laying the groundwork for modern capitalism. The Italian Renaissance flourished during the 15th and 16th centuries and spread to the rest of Europe. Italian explorers discovered new routes to the Far East and the New World, contributing significantly to the Age of Discovery. After centuries of political and territorial divisions, Italy was almost entirely unified in 1861, following wars of independence and the Expedition of the Thousand, establishing the Kingdom of Italy. From the late 19th to the early 20th century, Italy industrialised—mainly in the north—and acquired a colonial empire, while the south remained largely impoverished, fueling a large immigrant diaspora to the Americas. From 1915 to 1918, Italy took part in World War I with the Entente against the Central Powers. In 1922, the Italian fascist dictatorship was established. During World War II, Italy was first part of the Axis until an armistice with the Allied powers (1940–1943), then a co-belligerent of the Allies during the Italian resistance and the liberation of Italy (1943–1945). Following the war, the monarchy was replaced by a republic and the country enjoyed a strong recovery. A developed country with an advanced economy, Italy has the eighth-largest nominal GDP in the world, the second-largest manufacturing sector in Europe, and plays a significant role in regional and—to a lesser extent—global economic, military, cultural, and political affairs. It is a founding and leading member of the European Union and the Council of Europe, and is part of numerous other international organizations and forums. As a cultural superpower, Italy has long been a renowned global centre of art, music, literature, cuisine, fashion, science and technology, and the source of multiple inventions and discoveries. It has the highest number of World Heritage Sites (60) and is the fourth-most visited country in the world.",
  "article_url": "https://en.wikipedia.org/wiki/Italy",
  "article_title": "Italy"
}
```

### Option 3: Full Content

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=3`

**Response:**

```json
{
  "status": "success",
  "type": "full_content",
  "content": "91% Italian 9% other \n  84% Christianity 12% no religion 4% other \n  Paragraph: Italy, officially the Italian Republic, is a country in Southern and Western Europe. It consists of a peninsula that extends into the Mediterranean Sea, with the Alps on its northern land border, as well as nearly 800 islands, notably Sicily and Sardinia. Italy shares land borders with France to the west; Switzerland and Austria to the north; Slovenia to the east; and the two enclaves of Vatican City and San Marino. It is the tenth-largest country in Europe by area, covering 301,340 km`2 (116,350 sq mi), and the third-most populous member state of the European Union, with nearly 59 million inhabitants. Italy's capital and largest city is Rome; other major cities include Milan, Naples, Turin, Palermo, Bologna, Florence, Genoa, and Venice.\n \n  Paragraph: The history of Italy goes back to numerous Italic peoples—notably including the ancient Romans, who conquered the Mediterranean world during the Roman Republic and ruled it for centuries during the Roman Empire. With the spread of Christianity, Rome became the seat of the Catholic Church and the Papacy. Barbarian invasions and other factors led to the decline and fall of the Western Roman Empire between late antiquity and the Early Middle Ages. By the 11th century, Italian city-states and maritime republics expanded, bringing renewed prosperity through commerce and laying the groundwork for modern capitalism.  Paragraph: During the war, more than 650,000 Italian soldiers and as many civilians died, and the kingdom was on the brink of bankruptcy. The Treaty of Saint-Germain-en-Laye (1919) and Treaty of Rapallo (1920) allowed for annexation of Trentino Alto-Adige, the Julian March, Istria, the Kvarner Gulf, and the Dalmatian city of Zara. The subsequent Treaty of Rome (1924) led to annexation of Fiume by Italy. Italy did not receive other territories promised by the Treaty of London, so this outcome was denounced as a \"mutilated victory\", by Benito Mussolini, which helped lead to the rise of Italian fascism. Historians regard \"mutilated victory\" as a \"political myth\", used by fascists to fuel Italian imperialism. Italy gained a permanent seat in the League of Nations's executive council.\n",
  "article_url": "https://en.wikipedia.org/wiki/Italy",
  "article_title": "Italy"
}
```

### Option 4: Captions of Images

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/James_Bond&option=4`

**Response:**

```json
{
  "status": "success",
  "type": "image_captions",
  "content": [
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Aston.db5.coupe.300pix.jpg",
      "final_caption": "The image showcases a classic Aston Martin DB5, a sleek silver sports car, parked on a paved area. The car's polished chrome grille and round headlights are prominently visible, reflecting its iconic design. In the background, other cars and greenery are faintly visible, suggesting a parking lot or a similar outdoor setting."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Daniel_Craig_-_Film_Premiere_%22Spectre%22_007_-_on_the_Red_Carpet_in_Berlin_%2822387409720%29_%28cropped%29.jpg",
      "final_caption": "The image shows Daniel Craig, dressed in a dark suit and tie, standing on a red carpet at the Berlin premiere of \"Spectre.\" He is positioned in the foreground, facing slightly to the left, with a backdrop featuring the event's branding."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/GoldeneyeEstate.jpg",
      "final_caption": "The image shows a white, single-story house with a gray roof, situated in a lush, tropical environment. The house features wooden shutters on the windows and a covered porch area. Palm trees and other greenery surround the property, creating a serene and secluded atmosphere. The sky is clear and blue, indicating a sunny day."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/57/Goldfinger_-_Aston_Martin_DB5_%26_Sean_Connery.jpg",
      "final_caption": "The image showcases a classic Aston Martin DB5, a sleek, silver sports car, prominently displayed in a museum-like setting. Beside the car stands a life-sized wax figure of Sean Connery, dressed in a sharp black suit and bow tie, with his arms crossed. In the background, a projected image of Connery in a suit is visible, adding context to the display. The setting includes a wall with sketches and a plaque, enhancing the historical and thematic presentation."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Hoagy_Carmichael_-_1947.jpg",
      "final_caption": "The image is a black-and-white portrait of Hoagy Carmichael, a jazz composer and actor, taken in 1947. He is dressed in a suit and tie, with his head slightly tilted forward, looking directly at the camera. The background is plain and out of focus, emphasizing the subject."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/67/James_Bond_%28Daniel_Craig%29_figure_at_Madame_Tussauds_London_%2830318318754%29_b.jpg",
      "final_caption": "The image depicts a waxwork of Daniel Craig, portraying James Bond, standing in a formal pose. He is dressed in a classic black tuxedo with a white shirt and black bow tie, hands in his pockets, and a watch on his left wrist. The background features a circular design with shades of purple and white, suggesting a themed setting, likely at Madame Tussauds in London."
    },
    {
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2a/James_Bond_Island.JPG",
      "final_caption": "The image showcases James Bond Island, a striking natural formation in Thailand. A prominent, tall rock formation rises from the water, surrounded by lush greenery and towering cliffs. The sky is clear and blue, enhancing the serene and picturesque setting. The water reflects the surrounding landscape, adding to the tranquil atmosphere."
    }
  ],
  "article_url": "https://en.wikipedia.org/wiki/James_Bond",
  "article_title": "James Bond",
  "image_count": 7
}
```

### Option 5: Tables

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=5`

**Response:**

```json
{
  "status": "success",
  "type": "tables",
  "content": {
    "url": "https://en.wikipedia.org/wiki/James_Bond",
    "tables_found": 9,
    "screenshots": [
      "Screenshots deleted after analysis"
    ],
    "analyses": [
      {
        "success": true,
        "image_path": "screenshots/table_1_1753245794.png",
        "analysis": "The table provided lists the publication years and titles of James Bond novels, along with their corresponding short story collections and editions. The table is divided into two columns: the left column lists the publication years and titles of the novels, while the right column lists the publication years and titles of the short story collections and editions.\n\nHere is a detailed description of the table:\n\n### Table Purpose:\nThe table provides a chronological list of James Bond novels and their associated short story collections and editions.\n\n### Column Headers:\n- **Left Column:** Publication Year and Novel Title\n- **Right Column:** Publication Year and Short Story Collection/Edition Title\n\n### Data Rows:\n\n| Left Column (Publication Year and Novel Title) | Right Column (Publication Year and Short Story Collection/Edition Title) |\n|---|---|\n| 1953 Casino Royale[22] | 1960 For Your Eyes Only[29] (short stories) |\n| 1954 Live and Let Die[23] | 1961 Thunderball[30] |\n| 1955 Moonraker[24] | 1962 The Spy Who Loved Me[31] |\n| 1956 Diamonds Are Forever[25] | 1963 On Her Majesty's Secret Service[32] |\n| 1957 From Russia, with Love[26] | 1964 You Only Live Twice[33] |\n| 1958 Dr. No[27] | 1965 The Man with the Golden Gun[34] |\n| 1959 Goldfinger[28] | 1966 Octopussy and The Living Daylights[35] (short stories; \"The Property of a Lady\" added to subsequent editions) |\n\nThis table serves as a reference for the publication history of James Bond novels and their associated short story collections and editions.",
	      },
      {
        "success": true,
        "image_path": "screenshots/table_4_1753245794.png",
        "analysis": "The table provided lists the years and titles of various works, presumably from a series or a collection. Here is a detailed description of the table:\n\n### Table Description:\n\n#### Purpose:\nThe table lists the years and titles of works, likely from a series or a collection, with a focus on the years 2008 to 2023.\n\n#### Column Headers:\nThe table has two columns:\n1. **Year**\n2. **Title**\n\n#### Data Rows:\nThe table contains the following rows:\n\n1. **2008** - **Devil May Care**\n2. **2011** - **Carte Blanche**\n3. **2013** - **Solo**\n4. **2015** - **Trigger Mortis**\n5. **2018** - **Forever and a Day**\n6. **2022** - **With a Mind to Kill**\n7. **2023** - **On His Majesty's Secret Service**\n\nThis table appears to be a chronological list of works, possibly from a series, with the years indicating when each work was published or released.",
      },
    ],
    "success": true,
    "successful_analyses": 9,
    "failed_analyses": 0
  },
  "article_url": "https://en.wikipedia.org/wiki/James_Bond",
  "article_title": "James Bond",
  "table_count": 0
}
```

### Option 6: References

**Endpoint:** `http://127.0.0.1:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=6`

**Response:**

```json
{
  "status": "success",
  "type": "citations",
  "content": [
    "Ian Fleming, The New Yorker, 21 April 1962",
    "—David Arnold",
    "—Q, to Bond, Licence to Kill",
    "Reilly, Liam (20 February 2025). \"Amazon MGM Studios takes creative control of James Bond franchise\". CNN. CNN Business. Archived from the original on 21 February 2025. Retrieved 27 February 2025.",
    "Uddin, Rafe (20 February 2025). \"Amazon MGM to take over creative direction of James Bond franchise\". Financial Times. Retrieved 20 February 2025.",
    "Macintyre, Ben (5 April 2008). \"Bond – the real Bond\". The Times. p. 36.",
    "\"Obituary: Colonel Peter Fleming, Author and explorer\". The Times. 20 August 1971. p. 14.",
    "Hall, Chris (22 March 2020). \"From the archive: the real James Bond, 1973\". The Guardian. Retrieved 28 February 2023.",
    "\"James Bond, Ornithologist, 89; Fleming Adopted Name for 007\". The New York Times. 17 February 1989. Archived from the original on 2 May 2019. Retrieved 22 August 2019.",
    "Hellman, Geoffrey T. (21 April 1962). \"Bond's Creator\". The New Yorker. p. 32. section \"Talk of the Town\". Archived from the original on 21 January 2012. Retrieved 9 September 2011.",
    "Cook, William (28 June 2004). \"Novel man\". New Statesman. p. 40.",
    "Lycett, Andrew (2004). \"Fleming, Ian Lancaster (1908–1964) (subscription needed)\". Oxford Dictionary of National Biography (online ed.). Oxford University Press. doi:10.1093/ref:odnb/33168. Retrieved 7 September 2011.",
    "\"Casino Royale\". The Books. Ian Fleming Publications. Archived from the original on 17 March 2012. Retrieved 31 October 2011.",
    "\"Live and Let Die\". The Books. Ian Fleming Publications. Archived from the original on 17 March 2012. Retrieved 31 October 2011.",
    "\"Moonraker\". The Books. Ian Fleming Publications. Archived from the original on 16 September 2011. Retrieved 31 October 2011.",
    "\"Diamonds are Forever\". The Books. Ian Fleming Publications. Archived from the original on 17 March 2012. Retrieved 31 October 2011.",
    "\"From Russia, with Love\". The Books. Ian Fleming Publications. Archived from the original on 1 April 2012. Retrieved 31 October 2011."
  ],
  "article_url": "https://en.wikipedia.org/wiki/James_Bond",
  "article_title": "James Bond",
  "citation_count": 220
}
```