#!/usr/bin/env python

"""
archiveInfo.py: recrusivly extract archive and list found [timestamp](\.[\d])+\.dat(\.[gz|tar\.gz|tar.bz2|tgz|tbz])+
"""

import sys, os, io, getopt
import re
import tarfile

dataFile = re.compile('^\d+.*\.dat(\.)?.*$')
archiveFile = re.compile('^.*\.(tar\.gz|tgz|tar\.bz2|tbz)$')

def walkFs(path):
    for root, dirs, files in os.walk(path):
        count = 0
        for name in files:
            n = os.path.join(root,name)
            if os.path.exists(n) and os.path.isfile(n):
#                print "checking: %s" % n
                if dataFile.match(name):
                    try: 
                    	tarball = open(n, 'rb')
                        walkArchive(root, name, io.BytesIO(tarball.read()))
                    except Exception, e:
                        sys.stderr.write("1:Error opening %s\n" % n)
#        if count > 0:
#            print "%s: %d data files" % (root, count)

def walkArchive(root, fn, fh):
    t = tarfile.open(fileobj=fh)
    root = os.path.join(root, fn)
    count = 0
    for f in t.getmembers():
        if dataFile.match(f.name):
#            count += 1
             print root + " " + f.name
        elif archiveFile.match(f.name):
            walkArchive(root, f.name, io.BytesIO(t.extractfile(f).read()))
#    if count > 0:
#        print "File: %s (%d dat files)"% (root, count)



def main():
    options, args = getopt.getopt(sys.argv[1:],"")
    if len(args) != 1:
        raise getopt.GetoptError('Need exactly one directory path', None)
    walkFs(args[0])

if __name__ == '__main__':
    main()

