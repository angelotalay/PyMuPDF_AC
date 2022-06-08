import PyMuHTML
import PyMuPDF
import configuration
import argparse


# TODO: Remember to allow user to set input and output directories and select PDF files
def read_args() -> tuple[str, str, str]:
    """ Check for CLI arguments and return as dictionary"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Input PDF file path.")
    parser.add_argument("-o", help="Path for the output HTML file.")
    parser.add_argument("-c", help="Path to configuration JSON file.")
    args = parser.parse_args()

    filepath = args.f
    output_path = args.o
    config_path = args.c

    return filepath, output_path, config_path


def run_conversion(converter_object: object) -> object:
    converter_object.convert_pdf()
    merged_pages = converter_object.merge_pages()
    return str(merged_pages)


def concatenate_sections(pre_processing_object: object):
    """ Connected sections """
    pre_processing_object.reformat_file()
    section, source_lines = pre_processing_object.find_sections()
    connected_section = pre_processing_object.connect_section(section, source_lines)
    pre_processing_object.merge(connected_section)
    pre_processing_object.reformat_file()
    return pre_processing_object


if __name__ == '__main__':
    arguments = read_args()
    configs =
    converter = PyMuPDF.PDF_Convert()
    merged = run_conversion(converter)
    pre_processing = PyMuHTML.PyMuHTML(merged)
    pre_processing = concatenate_sections(pre_processing)
    for n in range(0, 1):
        pre_processing.unwrap_tags()

    converter.write_page(pre_processing.soup)
# TODO: AT THE END OF PRE-PROCESSING WRITE OUTPUT AS PRETTIFIED STRING
