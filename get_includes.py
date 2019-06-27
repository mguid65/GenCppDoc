from __future__ import print_function

import os
import sys

class BuildIncList():
  def __init__(self):
    self.filename = 'includes.txt';
    self.include_data = open(self.filename, 'r').readlines()
    if self.include_data[0][0] == '#':
      self.include_data.pop(0)

  def get_includes(self):
    include_list = list()
    for row in self.include_data:
      include_list.append('-isystem')
      include_list.append(str(row[0:-1]))

    return include_list

def main():
  inc_list = BuildIncList().get_includes()
  for item in inc_list:
    print('\'' + item + '\',', end='')
  print()

if __name__ == '__main__':
  main()
