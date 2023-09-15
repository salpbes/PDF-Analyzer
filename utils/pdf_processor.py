from PyPDF2 import PdfReader

def extract_title_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        metadata_title = None
        
        try:
            metadata_title = reader.Info.get("/Title")
        except AttributeError:
            pass
        
        # If title exists in metadata, return it
        if metadata_title:
            return metadata_title.strip()

        # Otherwise, use simple logic to guess the title from the first page
        first_page = reader.pages[0].extract_text()
        first_line = first_page.split('\n')[0].strip()
        if first_line:
            return first_line
        else:
            return "Title Unknown. It is not possible to estimate the title."

