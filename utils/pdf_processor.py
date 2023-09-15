from PyPDF2 import PdfReader

def extract_metadata_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)

        # Extracting metadata
        title = reader.metadata.get("/Title")
        author = reader.metadata.get("/Author")
        subject = reader.metadata.get("/Subject")

        # Rule 1: If a title exists, use it in any case for our file title
        if title:
            # Rule 2: If the author and subject also exist, concatenate all three
            if author and subject:
                return f"{title}-{author}-{subject}"
            return title

        # Rule 3: If a title doesn't exist but the author and subject exist at the same time, use the author and subject
        if author and subject:
            return f"{author}-{subject}"

        # Rule 4 and 5: If a title doesn't exist but only one of the author or subject exists, 
        # or if neither the title, author, nor subject exist, guess the title from the first page
        first_page = reader.pages[0].extract_text()
        guessed_title = first_page.split('\n')[0].strip()
        if not guessed_title:
            guessed_title = "Title Unknown. It is not possible to estimate the title."

        return guessed_title
