#!/usr/bin/env python3
import argparse
import sys
from os import path
import PyPDF2 as pyPdf


class Pdfer(object):

  def __init__(self):
    parser = argparse.ArgumentParser(description="Pdf to text simple converter", usage='''pdf.py -i <input file> -o <out file> -w (dafault True)''')
    parser.add_argument('-o', action="store", dest="Out")
    parser.add_argument('-i', action="store", dest="Input")
    parser.add_argument('-w', action="store_false", dest="w", help="page wrapper per page in pdf insert onto txt each page")
    results = parser.parse_args()
    
    if(results.Input != None and results.Out != None):
      self.input = results.Input
      self.output = results.Out
      self.w = results.w
      self.toFileWr()
    else:
      print(parser.parse_args(['-h']))
  
  def getMyPdf(self):
    if(False == path.isfile(self.input)):
      print('File is no exists')
      return 1
    pdfFile = open(self.input, 'rb')
    pdfReader = pyPdf.PdfFileReader(pdfFile)
    pages = pdfReader.getNumPages()
    content = ""
    toolbar_width = pages
    print('Gathering text')
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    for line in range(0, pdfReader.getNumPages()):
      sys.stdout.write(".")
      sys.stdout.flush()
      pageWrapper = "\n Page: " + str(line) + "\n" if self.w else ""
      content += pdfReader.getPage(line).extractText() + pageWrapper
    return content 

  def toFileWr(self):
    content = self.getMyPdf()
    file = open(self.output, 'w+')
    file.write(content)
    file.close
    
if __name__ == '__main__':
  Pdfer()