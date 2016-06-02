import glob
import os
import multiprocessing
from PyPDF2 import PdfFileWriter, PdfFileReader

try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 4   # arbitrary default

def pdf_excerpter(filename):
    input1 = PdfFileReader(open(filename, "rb"))
    #open
    a = input1.getNumPages()
    print(a)
    #extract text
    # for i in range(1, a):
    #     page = input1.getPage(a)
    #     print(page.extractText())
    #save file in output folder

if __name__ == "__main__":
    #glob pdf files in pdf folder
    pdf_files = glob.glob('./pdf/*.pdf')
    print(pdf_files)

    pool = multiprocessing.Pool(processes=cpus)
    #pdf_files will be a list
    output = pool.map(pdf_excerpter,pdf_files)
