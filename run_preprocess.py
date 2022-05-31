import PyMuHTML
import PyMuPDF
from sys import argv


# TODO: Remember to allow user to set input and output directories and select PDF files
def run_conversion() -> object:
    converter = PyMuPDF.PDF_Convert()
    converter.convert_pdf()
    merged_pages = converter.merge_pages()
    converter.write_page(final=merged_pages)
    return merged_pages


def concatenate_sections(merged_file):
    file = merged_file

    ''' Connected paragraphs '''
    paragraphs, source_lines = file.find_paragraphs()
    connected_paragraphs = file.connect_paragraphs(paragraphs, source_lines)




run_conversion()
