import fitz
from FormatHTML import PyMuHTML


# TODO: Make the write page method to be able to write at any stage.
class PDF_Convert:
    def __init__(self, file_path):
        self.file_pages = None
        self.can_write = False
        self.file_path = file_path

    def convert_pdf(self):  # Method to convert the pdf pages - then store each page in file_pages.
        self.file_pages = []
        document = fitz.open(self.file_path)

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

    @staticmethod
    def write_page(final: object, outfile_name: str, is_dir: bool) -> None:
        if not is_dir:
            if outfile_name[-5:] != '.html':
                with open(f"{outfile_name}.html", mode='w') as out:
                    out.write(str(final))
            else:
                with open(outfile_name, mode="w") as out:
                    out.write(str(final))
        elif is_dir:
            if outfile_name[-4:] == '.pdf':
                with open(f"{outfile_name[:-4]}.html", mode="w+") as out:
                    out.write(str(final))
            else:
                with open(f"{outfile_name}.html", mode="w+") as out:
                    out.write(str(final))
