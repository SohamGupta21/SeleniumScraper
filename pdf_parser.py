# from PyPDF4 import PdfFileReader

# def extract_information(pdf_path):
#     with open(pdf_path, 'rb') as f:
#         pdf = PdfFileReader(f)
#         information = pdf.getDocumentInfo()
#         number_of_pages = pdf.getNumPages()
#         page = pdf.getPage(0)
#         content = page.extractText()
#         content = " ".join(content.replace(u"\xa0", " ").strip().split())


#     txt = f"""
#     Information about {pdf_path}: 

#     Author: {information.author}
#     Creator: {information.creator}
#     Producer: {information.producer}
#     Subject: {information.subject}
#     Title: {information.title}
#     Number of pages: {number_of_pages}
#     """

#     print(txt)
    
#     for line in content.split('\n'):
#         #if re.match(r"^PDF", line):
#         print(line)
#     return information

# if __name__ == '__main__':
#     path = 'ACMPapers/3106328.3106329.pdf'
#     extract_information(path)

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



if __name__ == '__main__':
    path = 'ACMPapers/3106328.3106330.pdf'
    print(convert_pdf_to_txt(path))