import PyMuHTML
import PyMuPDF
import configuration
import argparse
import itertools


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


def sort_configuration(config_path) -> dict[str, dict]:
    config = configuration.Configuration(config_path)
    config.read_configuration()
    config_dict = config.__dict__

    return config_dict


def run_conversion(converter_object: object) -> object:
    converter_object.convert_pdf()
    merged_pages = converter_object.merge_pages()
    return str(merged_pages)


def concatenate_sections(pre_processing_object: object, json_information: dict):
    """ Function that finds sections and merges them together """
    json_tag = json_information[0]
    json_attribute = json_information[1]

    pre_processing_object.reformat_file()
    section, source_lines = pre_processing_object.find_sections(config_tag=json_tag, config_attribute=json_attribute)
    connected_section = pre_processing_object.connect_section(section, source_lines)
    pre_processing_object.merge(connected_section)
    pre_processing_object.reformat_file()
    return pre_processing_object


if __name__ == '__main__':
    # Parse arguments and input config file path into configuration class, return dictionary of tags and attributes
    arguments = read_args()
    configuration_class = configuration.Configuration(arguments[-1])
    configuration_class.read_configuration()

    outfile = arguments[1]

    converter = PyMuPDF.PDF_Convert()
    merged = run_conversion(converter)
    pre_processing = PyMuHTML.PyMuHTML(merged)

    step1 = concatenate_sections(pre_processing, configuration_class.title)
    step2 = concatenate_sections(step1, configuration_class.paragraph)
    # for n in range(0, 1):
    #     pre_processing.unwrap_tags()

    converter.write_page(pre_processing.soup, arguments[1])
