import os
from typing import List, Tuple
import fitz


class HighlightExtractor:
    def extract(self, filepath: str) -> (str, list):
        """
        Extracts the highlighted text from the pdf path given
        :param filepath: path to pdf
        :return: the name of the pdf, a list of highlighted text
        """
        filename = os.path.split(filepath)[1]
        doc = fitz.open(filepath)
        highlights = []
        for page in doc:
            highlights += self.handle_page(page)
        # print('File:', filename)
        # print(highlights)
        return filename, highlights

    def parse_highlight(self, annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
        points = annot.vertices
        quad_count = int(len(points) / 4)
        sentences = []
        for i in range(quad_count):
            # where the highlighted part is
            r = fitz.Quad(points[i * 4: i * 4 + 4]).rect

            words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
            sentences.append(" ".join(w[4] for w in words))
        sentence = " ".join(sentences)
        return sentence

    def handle_page(self, page):
        wordlist = page.get_text("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

        highlights = []
        annot = page.firstAnnot
        while annot:
            if annot.type[0] == 8:
                highlights.append(self.parse_highlight(annot, wordlist))
            annot = annot.next
        return highlights


if __name__ == "__main__":
    highlight_extractor = HighlightExtractor()
    highlight_extractor.extract('path_to_dir')
