#!/usr/bin/env python

"""
dupeCheck.py: diff directories and flag duplicated (>75%) subdirectories
"""
import sys
import getopt
from filecmp import dircmp
def printDupe(dcmp, s=1):
  sys.stdout.write("-"*s + "/" + dcmp.left)
  if (len(dcmp.left_list) != 0):
    p = int(float(len(dcmp.same_files + dcmp.common_dirs)) / float(len(dcmp.left_list)) * 100)
    if (p >= 75):
      sys.stdout.write("[" + str(p) + "%]")
  elif (len(dcmp.right_list) == 0):
    sys.stdout.write(" [100%(empty)]")
  print
  s += 1
  for sub in dcmp.subdirs.values():
    printDupe(sub,s)

if __name__ == '__main__':
  options, args = getopt.getopt(sys.argv[1:],"")
  if len(args) != 2:
    raise getopt.GetoptError('Need exactly two directory paths', None)
  print "/",sys.argv[1]," (",sys.argv[2],")"
  dcmp = dircmp(sys.argv[1], sys.argv[2])
  printDupe(dcmp)
  print



  

