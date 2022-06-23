from bs4 import BeautifulSoup
import re


class PyMuHTML:
    def __init__(self, file):
        self.soup = BeautifulSoup(file, 'html5lib')
        self.configuration = None

    # TODO: CHANGE LOGIC TO USE CONFIG RATHER THAN HARD CODING SPECIFIC TAGS
    def remove_lines(self) -> None:
        """ Remove specific lines specified by inspector of PDF files. Also removes lines related to images since
        they can span over many lines within the HTML file. """
        soup = self.soup
        # Find lines that contain Author Manuscript and image tags and other unnecessary information
        for author_man in soup.find_all(name=["p", "span"], string="Author Manuscript"):
            author_man.decompose()

        images = soup.find_all(name='img')

        for n in range(len(images)):
            soup.img.decompose()

        self.soup = soup

    def remove_repetitive(self) -> None:
        """ Method to remove repetitive lines within soup object, similar to remove lines but less specific"""
        soup = self.soup
        text_count = {}
        for line in soup.find_all(name=["p", "span"]):
            if line not in text_count.keys():
                text_count[line] = 1
            else:
                text_count[line] += 1
        more_than_10 = {k: v for (k, v) in text_count.items() if v > 10}
        for key in more_than_10.keys():
            tag_name = key.name
            tag_text = key.getText()
            found = soup.find_all(name=tag_name, string=tag_text)
            for line in found:
                line.decompose()
        self.soup = soup

    # TODO: STOP AUTHORS AND FOOTER TEXT FROM BEING EXTRACTED - WHAT OTHER TAGS AND ATTRIBUTES DO THEY HAVE?
    def find_sections(self, config_tag, config_attribute) -> tuple:
        soup = self.soup
        p_tags = soup.find_all(name="p")
        section = []

        # Get the nested span tags
        for tag in p_tags:

            if config_tag == 'b' or config_tag == 'i':
                try:
                    span = tag.find(name='span',attrs={"style":re.compile(config_attribute)})
                    text = span.getText()

                    if text is not None:
                        section.append(span)
                except AttributeError:  # Capture the case where tag.find() is None
                    continue

            else:
                try:
                    span = tag.find(name=config_tag, attrs={"style":re.compile(config_attribute)})
                    text = span.getText()

                    # Add the spans that contain text and append to the section list. This will be used to obtain that
                    # sourceline numbers
                    if text is not None:
                        section.append(span)

                except AttributeError:  # Capture the case where tag.find() function is None.
                    continue

        source_lines = [n.sourceline for n in section]
        return section, source_lines

    @staticmethod
    def connect_section(paras: list, source_lines: list) -> list:  # Method for getting all the paragraphs
        connected_sections = {'section': []}
        test_number = 0  # Test purposes only - to determine the number of lines that are being added together
        all_paras = []
        for n in range(len(paras)):
            line = paras[n]
            line_number = source_lines[n]
            if line_number != source_lines[-1]:  # For all lines from the first paragraph until the second to last
                next_line = paras[n + 1]
                next_line_number = source_lines[n + 1]

                if line_number - next_line_number == -1:  # Append the next paragraph if they're on the next line
                    if line not in connected_sections['section']:
                        connected_sections['section'].append(line)
                    # else:
                    #     connected_sections['section'].append(next_line)
                elif line_number - next_line_number < -1:  # If the next line number is more than one line away from
                    # the current line number
                    if line_number != source_lines[0]:
                        previous_line_number = source_lines[n - 1]
                        if previous_line_number == source_lines[n - 1]:
                            connected_sections['section'].append(line)
                            whole_para = [n for n in connected_sections['section']]
                            all_paras.append(whole_para)
                            connected_sections['section'].clear()
            elif line_number == source_lines[-1]:
                previous_line_number = source_lines[n - 1]
                if previous_line_number == source_lines[n - 1]:
                    connected_sections['section'].append(line)
                    whole_para = [n for n in connected_sections['section']]
                    all_paras.append(whole_para)
                    connected_sections['section'].clear()

            else:
                all_paras.append(line)
                whole_para = [n for n in connected_sections['section']]
                all_paras.append(whole_para)
                connected_sections['section'].clear()
        return all_paras

    def insert_text(self, tag: object, string: str) -> None:
        """ Method for inserting strings of the same section into the first line of the section. The method also
        extracts and returns the attribute """
        soup = self.soup
        first_line = soup.find('span', text=tag.text)
        complete = tag.text + string

        if first_line is not None:
            first_line.string.replace_with(complete)
            first_line.text

        self.soup = soup

    def decompose_lines(self, lines: list):
        """ Method to decompose/remove duplicated lines after concatenation of sections """
        soup = self.soup
        if len(lines) == 0:  # Some sections only consist of one line
            pass

        else:
            for line in lines[1:]:
                try:
                    to_delete = soup.find('span', string=line.text)
                    parent = to_delete.find_parent()  # Find the outer tag of the span and remove
                    parent.decompose()
                except AttributeError:  # Case where find_parent is None
                    continue

        self.soup = soup

    def reformat_file(self):  # Reformat function in order to remove whitespaces
        """ Removal of newline characters after decomposition of tags. Useful to use before merging sections together
        as source line numbers should be reset as the output is re-parsed into BeautifulSoup """
        soup = self.soup

        for tag in soup.find_all(name='p'):  # Iterate over lines to remove empty tags
            if len(tag.get_text()) == 0:
                tag.decompose()
        self.soup = soup

        soup = self.soup
        string = str(soup)
        list_html = string.split('\n')
        out_html_list = [n + '\n' for n in list_html if n != '']
        out_string = ''.join(out_html_list)
        self.soup = BeautifulSoup(out_string, 'html5lib')  # Re-parsing should also reset stored sourcelines

    def merge(self, connected_section):
        """" Method to merge the paragraphs into one entity and remove remaining lines
         that have already been concatenated with first line of the section. """
        paragraphs_to_merge = connected_section
        for section in paragraphs_to_merge:
            if type(section) == list and len(section) != 0:
                first_line = section[0]
                concatenated_string = ''.join([n.text for n in section[1:]])
                self.insert_text(first_line, concatenated_string)
                self.decompose_lines(section)
            elif type(section) != list:  # Skips over None values
                continue

    def unwrap_tags(self):
        """ Method that unwraps the nested tags but keeps attributes of the inner tag containing the texts"""
        soup = self.soup
        all_tags = soup.body.div.find_all(recursive=False)

        # Get all elements, find all child elements and recur
        for element in all_tags:
            # Get children parent and attribute to reformat lines
            children = element.findChildren()  # To get the nested tags
            last_child = children[-1]
            parent = last_child.parent

            attribute = last_child.get('style')
            last_child.unwrap()
            parent['style'] = attribute

        self.soup = soup
