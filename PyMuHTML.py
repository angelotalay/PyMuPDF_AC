from bs4 import BeautifulSoup


class PyMuHTML:
    def __init__(self, file):
        self.soup = BeautifulSoup(file, 'html5lib')
        self.paragraphs = None

    ''' Remove unnecessary tags/lines that contain images or Author manuscript text, to execute first '''

    # TODO: CHANGE LOGIC TO INCORPORATE OTHER PDFs THAT ARE NOT PMC - EG. INCLUDE TEXT FILE FOR DIFFERENT PUBLISHERS
    def remove_lines(self) -> None:
        # Find lines that contain Author Manuscript and image tags and other unnecessary information
        for author_man in self.soup.find_all(name=["p", "span"], string="Author Manuscript"):
            author_man.decompose()

        images = self.soup.find_all(name='img')

        for n in range(len(images)):
            self.soup.img.decompose()

        with open('TEST_OUT.html', mode='w') as out:  # For test purposes only
            out.write(str(self.soup))

    # TODO: TEST FOR CASE WHERE THERE'S A B TAG FOUND WITHIN THE P-TAG - THESE REPRESENT SUBHEADINGS NOT PARAGRAPHS
    # TODO: STOP AUTHORS AND FOOTER TEXT FROM BEING EXTRACTED - WHAT OTHER TAGS AND ATTRIBUTES DO THEY HAVE?
    # TODO: APPLY THIS FIND FUNCTION TO BE ABLE TO FIND OTHER TAGS SUCH AS THE TITLE T0 CONCATENATE THEM
    def find_sections(self) -> tuple:
        soup = self.soup
        p_tags = soup.find_all(name="p")
        section = []

        # Get the nested span tags
        for tag in p_tags:
            try:
                spans = tag.find(name="span", attrs={"style": "font-family:Times,serif;font-size:10pt"})
                text = spans.getText()

                # Add the spans that contain text and append to the section list. This will be used to obtain that
                # sourceline numbers
                if text is not None:
                    section.append(spans)

            except AttributeError:  # Capture the case where tag.find() function is None.
                continue

        source_lines = [n.sourceline for n in section]
        return section, source_lines

    @staticmethod
    def connect_section(paras: list, source_lines: list) -> list:  # Method for getting all the paragraphs
        span_template = paras[0].replace_with('')
        connected_sections = {'section': []}
        test_number = 0  # Test purposes only - to determine the number of lines that are being added together
        all_paras = []
        for n in range(len(paras)):
            line = paras[n]
            line_number = source_lines[n]
            if line_number != source_lines[-1]:
                next_line = paras[n + 1]
                next_line_number = source_lines[n + 1]
                if line_number - next_line_number == -1:
                    if line not in connected_sections['section']:
                        connected_sections['section'].append(line)
                    else:
                        connected_sections['section'].append(next_line)

                else:
                    if source_lines[n - 1] != line_number - 1:
                        all_paras.append(line)
                    test_number += len(connected_sections['section'])  # Testing to see if all lines have been
                    # connected
                    whole_para = [n for n in connected_sections['section']]
                    all_paras.append(whole_para)
                    connected_sections['section'].clear()
        return all_paras

    def text_insert(self, tag: object, string: str) -> object:
        soup = self.soup
        first_line = soup.find('span', text=tag.text)
        complete = tag.text + string

        if first_line is not None:
            first_line.string.replace_with(complete)
            first_line.text

        return complete, tag.sourceline  # Do we need to return anything?

    def decompose_lines(self, lines: list):  # TODO: Need to decompose outer tag as well -> only spans being removed
        soup = self.soup
        if len(lines) == 0:
            to_delete = soup.find(lines[0])
            to_delete.decompose()

        else:
            for line in lines[1:]:
                to_delete = soup.find('span', string=line.text)
                parent = to_delete.find_parent() # Find the outer tag of the span and remove
                parent.decompose()


    def merge(self, connected_section):  # Method to merge the paragraphs into one entity.
        paragraphs_to_merge = connected_section
        merged = []
        for section in paragraphs_to_merge:
            if type(section) == list and len(section) != 0:
                first_line = section[0]
                concatenated_string = ''.join([n.text for n in section[1:]])
                complete, source_number = self.text_insert(first_line, concatenated_string)
                merged.append((source_number, complete))
                self.decompose_lines(section)
            elif type(section) != list:  # Skips over None values
                continue

        return merged

    # def reformat(self, merged_section:tuple):
