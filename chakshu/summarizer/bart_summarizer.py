import torch
from transformers import BartForConditionalGeneration, BartTokenizer


class BartSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: str = "cuda"):
        self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name).to(self.device)

        self.model.eval()

        self.max_input_length = 1024
        self.max_output_length = 100

    def chunk_text(self, text: str, chunk_size: int = 1024):
        words = text.split()
        return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

    @torch.no_grad()
    def summarize(self, text: str):
        torch.cuda.empty_cache()
        chunks = self.chunk_text(text)
        summaries = []

        for chunk in chunks:
            inputs = self.tokenizer(chunk, max_length=self.max_input_length, truncation=True, return_tensors="pt").to(
                self.device
            )
            summary_ids = self.model.generate(
                inputs["input_ids"],
                num_beams=4,
                length_penalty=2.0,
                max_length=self.max_output_length,
                min_length=30,
                no_repeat_ngram_size=3,
            )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        return " ".join(summaries)


if __name__ == "__main__":
    summarizer = BartSummarizer()
    wikipedia_page = """Italy,[a] officially the Italian Republic,[b] is a country in Southern[12] and Western[13][c] Europe. It is on a peninsula that extends into the Mediterranean Sea, with the Alps on its northern land border, as well as islands, notably Sicily and Sardinia.[15] Italy shares its borders with France, Switzerland, Austria, Slovenia and two enclaves: Vatican City and San Marino. It is the tenth-largest country in Europe, covering an area of 301,340 km2 (116,350 sq mi),[3] and third-most populous member state of the European Union, with a population of nearly 60 million.[16] Its capital and largest city is Rome; other major urban areas include Milan, Naples, Turin, Florence, and Venice.

                        In antiquity, Italy was home to numerous peoples; the Latin city of Rome, founded as a Kingdom, became a Republic that conquered the Mediterranean world and ruled it for centuries as an Empire.[17] With the spread of Christianity, Rome became the seat of the Catholic Church and the Papacy. During the Early Middle Ages, Italy experienced the fall of the Western Roman Empire and inward migration from Germanic tribes. By the 11th century, Italian city-states and maritime republics expanded, bringing renewed prosperity through commerce and laying the groundwork for modern capitalism.[18][19] The Italian Renaissance flourished during the 15th and 16th centuries and spread to the rest of Europe. Italian explorers discovered new routes to the Far East and the New World, leading the European Age of Discovery. However, centuries of rivalry and infighting between city-states left the peninsula divided.[20] During the 17th and 18th centuries, Italian economic importance waned significantly.[21]

                        After centuries of political and territorial divisions, Italy was almost entirely unified in 1861, following wars of independence and the Expedition of the Thousand, establishing the Kingdom of Italy.[22] From the late 19th to the early 20th century, Italy rapidly industrialized, mainly in the north, and acquired a colonial empire,[23] while the south remained largely impoverished, fueling a large immigrant diaspora to the Americas.[24] From 1915 to 1918, Italy took part in World War I with the Entente against the Central Powers. In 1922, the Italian fascist dictatorship was established. During World War II, Italy was first part of the Axis until its surrender to the Allied powers (1940–1943), then a co-belligerent of the Allies during the Italian resistance and the liberation of Italy (1943–1945). Following the war, the monarchy was replaced by a republic and the country enjoyed a strong recovery.[25]

                        A developed country, Italy has the ninth-largest nominal GDP in the world, the second-largest manufacturing industry in Europe,[26] and plays a significant role in regional[27] and global[28] economic, military, cultural, and diplomatic affairs. Italy is a founding and leading member of the European Union, and is part of numerous international institutions, including NATO, the G7 and G20, the Latin Union and the Union for the Mediterranean. As a cultural superpower, Italy has long been a renowned centre of art, music, literature, cuisine, fashion, science and technology, and the source of multiple inventions and discoveries.[29] It has the world's highest number of World Heritage Sites (59), and is the fifth-most visited country."""
    summary = summarizer.summarize(wikipedia_page)
    print(summary)
