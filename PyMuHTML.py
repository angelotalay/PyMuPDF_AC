from bs4 import BeautifulSoup
import os

TEST = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestOutput/PyMuPDF/pmcPDF/PMC5511775_full_PMC.html'


class PyMuPHTML:
    def __init__(self, file):
        with open(file, mode='r') as f:
            file = f.read()
            f.seek(0)
            self.file_lines = f.readlines()
        self.soup = BeautifulSoup(file, 'html5lib')

    ''' Remove unnecessary tags/lines that contain images or Author manuscript text, to execute first'''

    def remove_lines(self) -> None:
        # Find lines that contain Author Manuscript and image tags and other unnecessary information
        copy = self.soup
        count = 1

        # Have to re-run code below through while loop since, not all tags detected through first parse
        while count > 0:
            author_man = copy.find_all(name=["p", "span"], string="Author Manuscript")
            count = len(author_man)
            line_numbers = [int(n.sourceline) for n in author_man]

            lines = self.file_lines
            for number in line_numbers:
                lines.pop(number - 1)
            next_copy = ''.join(lines)
            copy = BeautifulSoup(next_copy, 'html5lib')

        images = copy.find_all(name='img')
        for n in range(len(images)):
            copy.img.decompose()

        with open('TEST_OUT.html', mode='w') as out:  # For test purposes only
            out.write(str(copy))

        self.soup = copy

    # TODO: TEST FOR CASE WHERE THERE'S A B TAG FOUND WITHIN THE P-TAG - THESE REPRESENT SUBHEADINGS NOT PARAGRAPHS
    # TODO: STOP AUTHORS AND FOOTER TEXT FROM BEING EXTRACTED - WHAT OTHER TAGS AND ATTRIBUTES DO THEY HAVE?
    def find_paragraphs(self) -> tuple:
        copy = self.soup
        p_tags = copy.find_all(name="p")
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
        test_number = 0
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
                    test_number += len(connected_paragraphs['paragraph'])
                    whole_para = [n for n in connected_paragraphs['paragraph']]
                    all_paras.append(whole_para)
                    connected_paragraphs['paragraph'].clear()
        print(all_paras)
        return all_paras

    def merge(self, connected_paras):  # Method to merge the paragraphs into one entity.
        soup = self.s







output = PyMuPHTML(TEST)
output.remove_lines()
paragraphs, line_numbers = output.find_paragraphs()
all_paragraphs = output.connect_paragraphs(paragraphs, line_numbers)
output.merge(all_paragraphs)
