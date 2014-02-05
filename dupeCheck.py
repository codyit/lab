#!/usr/bin/env python

"""
dupeCheck.py: diff directories and flag duplicated (>75%) subdirectories
"""

import sys
import getopt
import os
from collections import defaultdict,deque
from hashlib import sha1
from zlib import crc32

class ChecksumCache(dict):
    ''' Deep check using SHA1 if no size given,
        otherwise create CRC32 cache of size. Cache result'''
    def __init__(self, size=None):
        dict.__init__(self)
        self.size = size

    def __getitem__(self, item):
        if item in self:
            return dict.__getitem__(self, item)
        else:
            try:
                h = open(item, 'rb')
            except IOError, e:
                sys.stderr.write("Error opening %s\n" % item)
                return -1 
            try:
                if self.size is not None:
                    chksum = crc32(h.read(self.size))
                else:
                    s = sha1(h.read())
                    chksum = s.digest()
            except IOError, e:
                sys.stderr.write("Error reading %s\n" % item)
                return -1
            finally:
                h.close()
            dict.__setitem__(self, item, chksum)
            return chksum 

class DirNode:
    def __init__(self, r, c, d, s):
        self.root = r
        self.filec = c
        self.dic = d
        self.subdir = s

def buildQueue(path):
    pathQueue = deque()
    for root, dirs, files in os.walk(path):
        d = DirNode(root, 0,defaultdict(list),dirs)
        for name in files:
            n = os.path.join(root,name)
            if os.path.exists(n) and os.path.isfile(n):
                d.filec += 1
                d.dic[os.path.getsize(n)].append(name)
        pathQueue.append(d)
    return pathQueue

def cmpDict(a, b, lmt, shallow, deep):
    minc, maxc = float(min(a.filec,b.filec)), float(max(a.filec,b.filec))
    if minc == 0 or minc/maxc * 100 < (100 - lmt):
        return -1

    dup =  uniq =  p = 0
    for size in a.dic.iterkeys():
        bfs = b.dic.get(size)
        if bfs is not None:
            sel = []
            for af in a.dic[size]:
                fnd = False
                for bf in bfs:
                    if bf in sel:
                        continue
                    afp, bfp = os.path.join(a.root, af), os.path.join(b.root, bf)
                    if shallow[afp] == shallow[bfp] and deep[afp] == deep[bfp]: 
                       sel.append(bf)
                       fnd = True
                       break
                if fnd:
                    dup += 1
                else:
                    uniq += 1 
        else:
           uniq += len(a.dic[size])
        if uniq/minc * 100 > (100 -lmt):
            return -1 
    return int(dup/maxc * 100)

def checkDupe(pds, lmt=75):
    shallow, deep = ChecksumCache(4096), ChecksumCache()
    while True:
        try:
            current = pds.popleft()
        except IndexError, e:
            break
        c = 0
        matches = []
        for target in list(pds):
            p = cmpDict(current, target, lmt, shallow, deep)
            if (p >= lmt):
                matches.append(target)
                if (c == 0):
                   print "%s" % current.root
                c += 1
                print "%s (%i%%)" % (target.root, p) 
        if (c > 0):
            print
        for ma in matches:
            pds.remove(ma) 

def main():
    options, args = getopt.getopt(sys.argv[1:],"")
    if len(args) != 1:
        raise getopt.GetoptError('Need exactly one directory path', None)
    pds = buildQueue(args[0])
    print "Duplicate directory pairs:"
    checkDupe(pds)

if __name__ == '__main__':
    main()
  

