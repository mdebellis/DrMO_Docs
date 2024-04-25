import pdfminer
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import io
from pathlib import Path

def traverse_dir(root_dir):
    l = []
    root_path = Path(root_dir)
    for path in root_path.rglob('*'): # rglob method is used for recursive globbing
        l.append(path)
    return l
# Example usage
#traverse_dir('/Users/aadarshbalaji/Desktop/nameoffolder)

def pdf_to_html():
    # Output stream for the HTML content
    folder_path = str(input("Enter the folder path that contains the pdfs: "))
    pdf_list = traverse_dir(folder_path)
    count = 0
    for pdf_path in pdf_list:
        #print(str(pdf_path))
        if str(pdf_path)[-3:].lower() == 'pdf':  # Ensure case-insensitive matching
            html_path = str(pdf_path).replace('pdfs', 'htmls')[:-3] + 'html'
            try:
                with open(pdf_path, 'rb') as pdf_file, io.open(html_path, 'w', encoding='utf-8') as output:
                    extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None)
                    count += 1
            except pdfminer.pdfparser.PDFSyntaxError as e:
                print(f"Error processing {pdf_path}: {e}")
    # Extract text to the HTML file
    print("Converted " + str(count) + " files!")

# Usage

pdf_to_html()