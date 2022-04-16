import os

from highlight_extractor import HighlightExtractor
from doc_writer import DocWriter

if __name__ == '__main__':
    path = input('Enter path to highlighted pdfs:\n')
    output = input('Enter output file name:\n')
    doc_writer = DocWriter()
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            highlight_extractor = HighlightExtractor()
            filename, highlighted_text = highlight_extractor.extract(os.path.join(path, file))
            if len(highlighted_text) > 0:
                doc_writer.write(filename, highlighted_text)
    doc_writer.save(os.path.join(path, output + '.docx'))
