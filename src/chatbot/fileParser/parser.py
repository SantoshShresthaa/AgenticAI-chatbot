from pypdf import PdfReader

def pdfParser():
    read_file = PdfReader('./bio/Profile.pdf')

    resume_profile = ""

    for page in read_file.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            resume_profile += extracted_text
    
    return resume_profile

# Extract text from txt file
def summeryExtractor():
    with open('./bio/self_intro.txt', 'r',  encoding="utf-8") as f:
        return f.read()

