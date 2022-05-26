import os

import fitz

INPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestPDF/pmcPDF/'
OUTPUT_DIR = '/home/aagt1/Documents/IndependentResearchProject/TestData/TestOutput/PyMuPDF/pmcPDF_xhtml/'


def test_pdf_output(input: str, output: str) -> None:
    for file in os.listdir(input):
        full_path = os.path.join(input, file)
        print(full_path)
        document = fitz.open(full_path)
        all_text = []
        output_file = file[:-4]
        for page in document:
            text = page.get_text('html') + '\n'
            all_text.append(text)
        document.close()

        with open(f'{OUTPUT_DIR}{output_file}.html', mode='w') as file:
            for text in all_text:
                file.write(text)


test_pdf_output(INPUT_DIR, OUTPUT_DIR)
