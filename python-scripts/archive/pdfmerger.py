import PyPDF2
import sys
import os

#put the pdf that you want to combine into the directory where this python file is saved
#than sort them in the order you want them to be
#than run the program, you now have the combined pdf in the "combinedPdfDocs.pdf" file

#Disclaimer: the program doesn't work properly, it combines the pdfs, but more than once

merger = PyPDF2.PdfMerger()

for file in os.listdir(os.curdir):
    if file.endswith(".pdf"):
        print(file)
        merger.append(file)
    merger.write("combinedPdfDocs.pdf")