import ollama
import tiktoken
from bs4 import BeautifulSoup


class WikipediaAccessibilityConverter:
    def __init__(self, ollama_model="llama3.1"):
        """
        Initialize the converter with Ollama LLM settings

        :param ollama_model: The Ollama language model to use (default: 'llama2')
        """
        self.ollama_model = ollama_model
        self.max_token_limit = 4000  # Adjust based on your model's context window
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def extract_text_from_html(self, html_path):
        """
        Extract text from HTML file using BeautifulSoup

        :param html_path: Path to the HTML file
        :return: Extracted text
        """
        with open(html_path, encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Remove script, style, and navigation elements
        for script in soup(["script", "style", "nav"]):
            script.decompose()

        # Extract main content (adjust selectors as needed)
        main_content = soup.find("div", class_=["mw-body-content", "mw-content"])
        if not main_content:
            main_content = soup.body

        # Extract text, preserving paragraphs
        paragraphs = main_content.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])

        return "\n\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

    def chunk_text(self, text):
        """
        Split text into manageable chunks

        :param text: Input text
        :return: List of text chunks
        """
        tokens = self.tokenizer.encode(text)
        chunks = []

        for i in range(0, len(tokens), self.max_token_limit):
            chunk_tokens = tokens[i : i + self.max_token_limit]
            chunks.append(self.tokenizer.decode(chunk_tokens))

        return chunks

    def convert_to_blind_friendly_format(self, text_chunk):
        """
        Convert text chunk to blind-friendly format using Ollama

        :param text_chunk: Text chunk to process
        :return: Processed text
        """
        prompt = f"""Convert this text to a blind-friendly format.
        Guidelines:
        1. Use clear, descriptive language
        2. Explain complex terms and concepts
        3. Break down long paragraphs
        4. Add context for any referenced visual elements
        5. Maintain the original meaning and tone
        6. Use simple, direct language
        7. Provide clear structural markers

        Text: {text_chunk}"""

        try:
            response = ollama.chat(model=self.ollama_model, messages=[{"role": "user", "content": prompt}])
            return response["message"]["content"]
        except Exception as e:
            print(f"Error processing chunk: {e}")
            return text_chunk

    def process_html(self, html_path, output_path):
        """
        Process entire HTML file and save blind-friendly version

        :param html_path: Path to input HTML file
        :param output_path: Path to save processed file
        """
        # Extract text
        raw_text = self.extract_text_from_html(html_path)

        # Chunk text
        text_chunks = self.chunk_text(raw_text)

        # Process chunks
        processed_chunks = []
        for chunk in text_chunks:
            processed_chunk = self.convert_to_blind_friendly_format(chunk)
            processed_chunks.append(processed_chunk)

        # Combine and save
        final_text = "\n\n".join(processed_chunks)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(final_text)

        print(f"Blind-friendly version saved to {output_path}")


# Example usage
def main():
    converter = WikipediaAccessibilityConverter(ollama_model="llama3.1")
    converter.process_html(r"C:\Users\Dhruv\Desktop\Wiki for Blind\chakshu\output.html", "blind_friendly_article.txt")


if __name__ == "__main__":
    main()
