import os
import fitz
from PyMuHTML import PyMuHTML

INPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestPDF/pmcPDF/'
OUTPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestOutput/PyMuPDF/pmcPDF_xhtml/'


# TODO: Create class to convert pdfs and to merge pages together within single body tag.
class PDF_Convert:
    def __init__(self):
        self.input = INPUT_DIR
        self.output = OUTPUT_DIR
        self.file_pages = None
        self.can_write = False

    def convert_pdf(self):  # Method to convert the pdf pages - then store each page in file_pages.
        self.file_pages = []
        for file in os.listdir(self.input):
            full_path = os.path.join(self.input, file)
            document = fitz.open(full_path)

            for page in document:
                text = page.get_text('html')
                clean = PyMuHTML(text)
                clean.remove_lines()

                self.file_pages.append(clean)

    def merge_pages(self) -> object:
        if self.file_pages is None:
            print("Convert a desired PDF document first using converted_pdf function")
        elif type(self.file_pages) == list:
            first_page = self.file_pages[0]

            for file in self.file_pages[1:]:  # Add all the elements of each page to the body tag within the first page.
                for element in file.body:
                    first_page.body.append(element)

            self.can_write = True
            return first_page

    def write_page(self, final) -> None:
        outfile_name = input("Write outfile name for HTML document: ")
        if self.can_write:
            final_path = os.path.join(self.output, outfile_name)
            with open(f"{final_path}.html") as out:
                out.write(str(final))
