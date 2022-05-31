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
            self.soup.img['src'] = 'None'

        with open('TEST_OUT.html', mode='w') as out:  # For test purposes only
            out.write(str(self.soup))

    # TODO: TEST FOR CASE WHERE THERE'S A B TAG FOUND WITHIN THE P-TAG - THESE REPRESENT SUBHEADINGS NOT PARAGRAPHS
    # TODO: STOP AUTHORS AND FOOTER TEXT FROM BEING EXTRACTED - WHAT OTHER TAGS AND ATTRIBUTES DO THEY HAVE?
    def find_paragraphs(self) -> tuple:
        soup = self.soup
        p_tags = soup.find_all(name="p")
        paragraphs = []

        # Get the nested span tags
        for tag in p_tags:
            try:
                spans = tag.find(name="span", attrs={"style": "font-family:Times,serif;font-size:10pt"})
                text = spans.getText()

                # Add the spans that contain text and append to the paragraphs list. This will be used to obtain that
                # sourceline numbers
                if text is not None:
                    paragraphs.append(spans)

            except AttributeError:  # Capture the case where tag.find() function is None.
                continue

        # For test purposes only - seeing whether all text is actually present.
        # with open('out_text.txt', mode='w') as out:
        #     for line in paragraphs:
        #         out.write(line.getText() + '\n')

        source_lines = [n.sourceline for n in paragraphs]
        return paragraphs, source_lines

    @staticmethod
    def connect_paragraphs(paras: list, source_lines: list) -> list:  # Method for getting all the paragraphs
        span_template = paras[0].replace_with('')
        connected_paragraphs = {'paragraph': []}
        test_number = 0  # Test purposes only - to determine the number of lines that are being added together
        all_paras = []
        for n in range(len(paras)):
            line = paras[n]
            line_number = source_lines[n]
            if line_number != source_lines[-1]:
                next_line = paras[n + 1]
                next_line_number = source_lines[n + 1]
                if line_number - next_line_number == -1:
                    if line not in connected_paragraphs['paragraph']:
                        connected_paragraphs['paragraph'].append(line)
                    else:
                        connected_paragraphs['paragraph'].append(next_line)

                else:
                    if source_lines[n - 1] != line_number - 1:
                        all_paras.append(line)
                    test_number += len(connected_paragraphs['paragraph'])  # Testing to see if all lines have been
                    # connected
                    whole_para = [n for n in connected_paragraphs['paragraph']]
                    all_paras.append(whole_para)
                    connected_paragraphs['paragraph'].clear()
        return all_paras

    @staticmethod
    def text_insert(tag: object, string: str) -> object:
        print(tag.text + string)

    def decompose_lines(self, lines: list):
        soup = self.soup

        for line in lines[1:]:
            to_delete = soup.find(line)
            print(to_delete)

        self.soup = soup

    def merge(self, connected_paras):  # Method to merge the paragraphs into one entity.
        soup = self.soup
        paragraphs_to_merge = connected_paras
        for paragraph in paragraphs_to_merge:
            if type(paragraph) == list and len(paragraph) != 0:
                first_line = paragraph[0]
                concatenated_string = ''.join([n.text for n in paragraph[1:]])
                self.text_insert(first_line, concatenated_string)
                self.decompose_lines(paragraphs_to_merge)
            elif type(paragraph) != list:
                continue


if __name__ == '__main__':
    output = PyMuHTML(TEST)
    output.remove_lines()
    paragraphs, line_numbers = output.find_paragraphs()
    all_paragraphs = output.connect_paragraphs(paragraphs, line_numbers)
# output.merge(all_paragraphs)
