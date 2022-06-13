import os
import fitz
from PyMuHTML import PyMuHTML

INPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestPDF/pmcPDF/PMC5612337_full_PMC.pdf'
OUTPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestOutput/PyMuPDF/pmcPDF_xhtml/'


# TODO: Create class to convert pdfs and to merge pages together within single body tag.
class PDF_Convert:
    def __init__(self):
        self.file_pages = None
        self.can_write = False

    def convert_pdf(self):  # Method to convert the pdf pages - then store each page in file_pages.
        self.file_pages = []
        full_path = INPUT_DIR
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
            first_page = self.file_pages[0].soup

            for file in self.file_pages[1:]:  # Add all the elements of each page to the body tag within the first page.
                soup = file.soup
                for element in list(soup.body.div)[1:]:  # Not sure whether to add into just the first page of the div
                    # or keep separate divs per page
                    first_page.body.div.append(element)

            self.can_write = True
            return first_page

    def write_page(self, final, outfile_name) -> None:
        if self.can_write:
            if outfile_name[-5:] != '.html':
                with open(f"{outfile_name}.html", mode='w') as out:
                    out.write(str(final))
            else:
                with open(outfile_name, mode="w") as out:
                    out.write(str(final))
        else:
            print("No HTML file to write.")
