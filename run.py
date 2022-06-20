import PDF_Conversion
import FormatHTML
import handle_path
import configuration
import argparse
import os


# TODO: Remember to allow user to set input and output directories and select PDF files

def read_args() -> tuple[str, str, str, str]:
    """ Check for CLI arguments and return"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="Input PDF file path.")
    parser.add_argument("-o", help="Path for the output HTML file.")
    parser.add_argument("-c", help="Path to configuration JSON file.")
    parser.add_argument("-d", help="Input PDF directory path")
    args = parser.parse_args()

    filepath = args.f
    output_path = args.o
    config_path = args.c
    directory_filepath = args.d
    return filepath, output_path, config_path, directory_filepath


def sort_configuration(config_path) -> None:
    """ Reads configuration and sets attributes for class"""
    config = configuration.Configuration(config_path)
    config.read_configuration()


def run_conversion(converter_object: object) -> object:
    converter_object.convert_pdf()
    merged_pages = converter_object.merge_pages()
    return str(merged_pages)


def concatenate_sections(pre_processing_object: object, json_information: dict) -> object:
    """ Function that finds sections and merges them together """
    json_tag = json_information[0]
    json_attribute = json_information[1]

    pre_processing_object.reformat_file()
    section, source_lines = pre_processing_object.find_sections(config_tag=json_tag, config_attribute=json_attribute)
    connected_section = pre_processing_object.connect_section(section, source_lines)
    pre_processing_object.merge(connected_section)
    pre_processing_object.reformat_file()
    return pre_processing_object


def concatenate_all(pre_processing_object: object, config_class: object) -> object:
    """ Function that utilises the concatenate_section function to merge all sections"""
    sections = [config_class.title, config_class.headers, config_class.subheadings, config_class.paragraphs]
    pre_process = pre_processing_object
    for section in sections:
        pre_process = concatenate_sections(pre_process, section)

    return pre_process


# TODO: Remove repeat code and refactor
def run_file(file_path: str, configuration_obj: object):
    """Run program with single file"""
    converter = PDF_Conversion.PDF_Convert(file_path)
    merged = run_conversion(converter)
    pre_processing = FormatHTML.PyMuHTML(merged)
    pre_processed = concatenate_all(pre_processing, configuration_obj)
    pre_processed.unwrap_tags()
    return pre_processed, converter


# TODO: OUTPATH IS BEING CONCATENATED HERE WHY?
def run_dir(directory_path: str, out_path: str, configuration_obj: object):
    output_path = out_path
    for file in os.listdir(directory_path):
        full_path = os.path.join(directory_path, file)
        out_path = os.path.join(output_path, file)
        out, converter = run_file(full_path, configuration_obj)
        out.remove_repetitive()
        out.reformat_file()
        converter.write_page(final=out.soup, outfile_name=out_path, is_dir=True, prefix=file)


if __name__ == '__main__':
    # Parse arguments and input config file path into configuration class, return dictionary of tags and attributes
    arguments = read_args()
    paths = handle_path.HandlePath(file_path=arguments[0], dir_path=arguments[3], out_path=arguments[1])
    configuration_class = configuration.Configuration(arguments[2])
    configuration_class.read_configuration()

    if paths.dir_path is not None:
        paths.check_dir()
        run_dir(directory_path=paths.dir_path, out_path=paths.out_path, configuration_obj=configuration_class)

    elif paths.file_path is not None:
        paths.check_file_path()
        out_file, converter = run_file(file_path=paths.file_path, configuration_obj=configuration_class)
        out_file.remove_repetitive()
        out_file.reformat_file()
        converter.write_page(final=out_file.soup, outfile_name=paths.out_path, is_dir=False)
