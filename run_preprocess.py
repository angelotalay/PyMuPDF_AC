import PyMuHTML
import PyMuPDF
from sys import argv


# TODO: Remember to allow user to set input and output directories and select PDF files
def run_conversion():
    converter = PyMuPDF.PDF_Convert()
    converter.convert_pdf()
    merged_pages = converter.merge_pages()
    converter.write_page(final=merged_pages)


run_conversion()


