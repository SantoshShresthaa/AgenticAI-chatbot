
from chatbot.fileParser import parser


def getUserProfile ():
    # Extract the content from the uploaded resume
    extracted_resume_content = parser.pdfParser()

    # Extract summary from the txt file
    self_intro_summary = parser.summeryExtractor()

    return extracted_resume_content, self_intro_summary