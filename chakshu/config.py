# Captioner
MODEL_URL = "http://20.219.173.103:11434/api/generate"

MODEL_NAME = "llava"

LLAVA_IMAGE_CAPTIONER_PROMPT = """
Analyze and describe the content of the image based on the metadata provided. Use the following guidelines:

1. Identify and name any individuals, places, or objects mentioned in the metadata.
2. Describe their positions and actions within the scene (e.g., who is on the left, right, etc.).
3. Include any notable interactions or movements.
4. Provide a detailed overview of the image that a blind person could understand, including visual cues like colors, lighting, and emotions where possible.

Use the following metadata to guide your description:

Image Metadata:
Title: {Title}
Description: {Description}

Ensure the description incorporates the names of people or places mentioned, along with their actions and relationships in the scene suitable for a blind person. Do not include any technical details like links, metadata, etc. The description should focus on helping a blind person understand the visual content.
"""

METADATA_IMAGE_CAPTIONER_PROMPT = """
Create an image description that incorporates the context provided in {context}.
If the context is brief, use {full_description} to provide a more complete description of what is happening in the image.
Write a clear, concise description of 30-40 words that communicates the key details about the image.
The description should be in simple, easy-to-understand English, suitable for someone who cannot see the image.
Focus strictly on what is visible and happening in the image, without mentioning any technical details such as image quality, resolution, or licensing."
"""
