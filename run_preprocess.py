import PyMuHTML
import PyMuPDF
from sys import argv


# TODO: Remember to allow user to set input and output directories and select PDF files

def run_conversion(converter_object) -> object:
    converter_object.convert_pdf()
    merged_pages = converter_object.merge_pages()
    converter_object.write_page(final=merged_pages)
    return str(merged_pages)


def concatenate_sections(pre_processing_object):
    """ Connected sections """
    section, source_lines = pre_processing_object.find_sections()
    connected_section = pre_processing_object.connect_section(section, source_lines)
    merging = pre_processing_object.merge(connected_section)
    print(merging)


converter = PyMuPDF.PDF_Convert()
merged = run_conversion(converter)

pre_processing = PyMuHTML.PyMuHTML(merged)
concatenate_sections(pre_processing)
print(pre_processing.soup)