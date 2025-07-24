# Captioner App (`captioner`)

The `captioner` app is responsible for providing captions for images found on Wikipedia pages.

## Responsibilities

* **Image Identification**: Potentially identifying images on a page (though image URLs might be passed from the `scraper` app).
* **Caption Retrieval/Generation**:
    * Fetching existing captions (e.g., from HTML `alt` text, `figcaption` elements, or surrounding text).
    * Utilizing metadata associated with images, if available (as suggested by `metadata_image_captioner.py`).
    * Possibly integrating with AI models for generating captions if no explicit captions are found (though this is an advanced feature not explicitly shown).
* **Data Formatting**: Presenting the captions in a usable format.

## Key Files and Components

* **`views.py`**:
    * `Workspace_and_process_images(selected_link)`:
        * This is the primary function exposed by the `captioner` app, called by `core.views.ProcessOptionView` when `option=4` is selected.
        * The exact implementation is not provided, but it would involve:
            1.  Getting image URLs for the `selected_link` (likely by calling a function from the `scraper` app, e.g., `scraper.views.get_image_urls()`).
            2.  For each image, attempting to find or generate a caption using logic from `image_captioner.py` and/or `metadata_image_captioner.py`.
            3.  Aggregating these captions and returning them. The return format is `ls_captions`, which is then passed to `JsonResponse` in `core.views`.

* **`image_captioner.py`**:
    * This file is expected to contain the core logic for deriving captions from image context or simple attributes.
    * This might involve:
        * Scraping the HTML around an image tag.
        * Looking for `<figcaption>` elements.
        * Using `alt` text or `title` attributes of `<img>` tags.
        * Basic heuristics based on surrounding text.
    * *Developer Note: The specific strategies used in this file will determine the quality and source of the captions.*

* **`metadata_image_captioner.py`**:
    * This file suggests an alternative or supplementary approach to captioning, focusing on metadata.
    * This could involve:
        * Fetching image metadata if images are hosted on platforms like Wikimedia Commons, which often have structured descriptions.
        * Parsing EXIF data if accessible (less likely in a web context).
    * *Developer Note: Understanding how this module complements or differs from `image_captioner.py` is important.*

* **`models.py`**:
    * The file structure shows `captioner/models.py` and a migration `0001_initial.py`. This implies that the `captioner` app might store data, such as:
        * Cached captions to avoid re-processing.
        * Associations between image URLs and their captions.
    * Developers should inspect the current models to understand what data is persisted.

* **`admin.py`, `apps.py`, `tests.py`**: Standard Django app files. `admin.py` would be used to register any `captioner` models with the Django admin interface.

## Interaction with Other Modules

* **`core` app**: The `core.views.ProcessOptionView` calls `captioner.views.fetch_and_process_images`.
* **`scraper` app (Likely)**: The `captioner` app will likely need image URLs from the `scraper` app to know which images to process. This could be a direct function call (e.g., `captioner.views` calling `scraper.views.get_image_urls()`) or image URLs could be passed into `Workspace_and_process_images`.

## Development Considerations

* **Caption Sources**: Determine the priority and reliability of different caption sources (alt text, figcaption, metadata, generated).
* **Accuracy**: The accuracy of captions is crucial. If generating captions, the quality of the model or heuristics will be important.
* **Performance**: Captioning multiple images can be time-consuming. Consider:
    * Batch processing.
    * Caching results in `captioner.models`.
    * Asynchronous processing if caption generation is slow (though the current `core.views` call is synchronous).
* **Handling Missing Captions**: Define a clear strategy for images where no caption can be found.
* **External Libraries/Services**: If using advanced AI captioning models, manage those dependencies and any associated API keys or model files. The current snippets do not show such advanced features.