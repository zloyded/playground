#!/usr/bin/env python3
import time, argparse

class Passports:

  def __init__(self):
    parser = argparse.ArgumentParser(description="Find some numbers in file", usage='''./range.py -n <number> ''')
    parser.add_argument('-n', dest="number")
    results = parser.parse_args()
    self.findNums(results.number)
    print("--- %s seconds ---" % (time.time() - self.start_time))

  def findNums(self, number):
    with open('fl','r') as f:
      data = f.read().split('\n')
    f.close()
    self.start_time = time.time()
    if bin(int(number)) in data:
      print('True')
    else:
      print('False')
    data=''
    
    
if __name__ == '__main__':
  Passports()
