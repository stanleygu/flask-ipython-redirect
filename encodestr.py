# -*- coding: utf-8 -*-

import os, sys
import base64 as b64
import binascii as bi 
from string import Template

print """intPDF encodestr module v0.2 May 23 2014
Author: Kiri Choi
University of Washington
kirichoi@uw.edu

encodestr converts combine archive into either base64 or hex string."""

def inq():
    print "The current working directory of this script is",os.getcwd(),"\nIf you want to manually locate the file, enter y"
    print "If this script is located in the same folder as the target file, enter n"
    usrinput = raw_input("Yes or no? (y/n) = ")
    return usrinput

def deffilename():
    print "Define the model name."
    usrinput = raw_input("Model name = ")
    return usrinput

def encodetype():
    print "You can encode combine archive in either base64 or hex. Which one?"
    usrinput = raw_input("base64 (b) or hex (h)? (b/h) = ")
    return usrinput

def loc():
    ans = inq()
    while(True):
        if ans == 'y' or ans == 'Y':
            currloc = raw_input("Enter the path = ")
            return currloc
        elif ans == 'n' or ans == 'N':
            fname = raw_input("Enter the file name (.zip) = ")
            currloc = os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)
            return currloc
        elif ans == 'exit' or ans == 'Exit':
            exit(0)
        else:
            print "Wrong input \n"
            ans = inq()
            
def instnl(instr, stlgth = 100):
    return '\n'.join(instr[i : i + stlgth] for i in xrange(0, len(instr), stlgth))
    
def encodestr(output):
    locid = loc()
    fname = deffilename()
    strform = encodetype()
        
    fin = open(locid, "rb")
    finput = fin.read()
    
    if strform == 'base64' or strform == 'b':
        outputloc = locid.replace('.zip','_b64.txt')
        enstr = b64.urlsafe_b64encode(finput)
        entype = 'base64'
    elif strform == 'hex' or strform == 'hexadecimal' or strform == 'h':
        outputloc = locid.replace('.zip','_hex.txt')
        enstr = bi.hexlify(finput)
        entype = 'hex'
    elif strform == 'exit' or strform == 'Exit':
        exit(0)
    else:
        print "Wrong input"
        strform = encodetype()
    outstr = instnl(enstr)

    fout = open(outputloc, "wb")
    temp = Template("http://localhost:5000/redirect?title=$name&format=$formtype&archive=$code")
    fstr = temp.substitute(name = fname, formtype = entype, code = outstr)
    fout.write(fstr)
    fin.close()
    fout.close()
    print "Converted \n"

def exitseq():
    raw_input('Press enter to exit.')
    exit(0)
    
encodestr(sys.argv[0])

exitseq()
