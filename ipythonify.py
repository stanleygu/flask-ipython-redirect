# -*- coding: utf-8 -*-

import sys, os, errno, time, json
import binascii as bi
import zipfile as zi
import tellurium as te
import xml.etree.ElementTree as xe
import SedmlToRr as se
import fileinput as fi
import base64 as b64
from string import Template

print """ipythonify module v0.1 May 20 2014
Author: Kiri Choi
University of Washington
kirichoi@uw.edu

This module will convert hex string back to its original zip file and uncompress them within the same folder.\n"""

def pyprep(inputstr, dirpth, fname, encode):    #given a string, directory path, and output filename, it creates a py script and a folder with raw model
    zoutfname = fname + '.zip'
    zoutputloc = os.path.join(dircheck(dirpth), zoutfname)
    zipdirname = fname + '_raw_model'
    zipextloc = os.path.join(dircheck(dirpth), zipdirname)

    pymodelloc = os.path.join(dircheck(dirpth), fname + '.py')

    decodestr(inputstr, zoutputloc, zipextloc, encode)
    codestitch(pymodelloc, zipextloc, fname)
    codeanalysis(pymodelloc, zipextloc)

def dircheck(loc):    #directory checking and creation
    if not os.path.exists(loc):
        os.makedirs(loc)
    return loc

def decodestr(inputstr, outputloc, extloc, etype):    #takes a string in either hex or base64, creates zip file and extracts it
    str_nnl = inputstr.replace('\n','').replace('\r','')

    if etype == 'base64':
        decstr = b64.urlsafe_b64decode(str_nnl)
    elif etype == 'hex':
        decstr = bi.unhexlify(str_nnl)
    else:
        raise TypeError('String error: Cannot obtain format information from given link')

    f = open(outputloc, "wb")
    f.write(decstr)
    f.close()
    print "Zip file recovered"

    tarzip = zi.ZipFile(outputloc)
    tarzip.extractall(extloc)
    tarzip.close()

    print "Zip file decompressed, \n location = ", extloc

    delseq(outputloc)

    print "Zip file removed \n"

def manifestsearch(zipextloc):    #searching manifest file for appropriate sbml and sedml locations
    manifestloc = os.path.join(zipextloc, 'manifest.xml')
    manifest = xe.parse(manifestloc)
    root = manifest.getroot()
    for child in root:
        attribute = child.attrib
        formtype = attribute.get('format')
        loc = attribute.get('location')
        if 'sbml' in formtype:
            sbmlloc = loc
            sbmlloc = sbmlloc[1:]
        elif 'sedml' in formtype:
            sedmlloc = loc
            sedmlloc = sedmlloc[1:]
    #sbmlloc = sbmlloc.replace('/','\\')
    #sedmlloc = sedmlloc.replace('/','\\')
    return (sbmlloc, sedmlloc)

def sbmlconv(zipextloc):    #sbml conversion into antimony str
    sbmlloc, sedmlloc = manifestsearch(zipextloc)
    sbml = te.readFromFile(zipextloc + sbmlloc)
    sbmlantimony = te.sbmlToAntimony(sbml)
    return sbmlantimony

def sedmlconv(zipextloc):    #sedml conversion
    sbmlloc, sedmlloc = manifestsearch(zipextloc)
    sedml = se.sedml_to_python(zipextloc + sedmlloc)
    return sedml

def codestitch(pymodelloc, extloc, filename):    #creates a py script with both sbml and sedml included
    sbmlstr = sbmlconv(extloc)
    sedmlstr = sedmlconv(extloc)
    with open(pymodelloc, "w+") as filef:
        filef.seek(0)
        readf = filef.read()
        filef.write("# -*- coding: utf-8 -*-\n\n" + '"Generated by intPDF ' + time.strftime("%m/%d/%Y") + '"\n"' + filename + '"\n\n')
        if not "import tellurium" in readf:
            filef.write("import tellurium as te\n\n")
        filef.write("model = '''\n" + sbmlstr + "'''\n" + sedmlstr)
        filef.close()

def codeanalysis(pymodelloc, extloc):    #included in case of sedml codes not compatible with single model file approach
    sbmlloc, sedmlloc = manifestsearch(extloc)
    for line in fi.input(pymodelloc,inplace = 1):
        line = line.strip()
        if not '.xml' in line:
            if "roadrunner.RoadRunner()" in line:
                line = line.replace("roadrunner.RoadRunner()", "roadrunner.RoadRunner(model)")
            print line

def jsonify(pyloc, fname):    #given the location of py script, outputs json string
    srcfile = open(pyloc, "r+")
    srcfile.seek(0)
    srcread = srcfile.read().splitlines()
    modelcon = json.dumps(['%matplotlib inline'] + srcread)
    temp = Template("""{
 "metadata": {
  "name": "$filetitle",
  "signature": ""
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": $modeldes,
     "language": "python",
     "metadata": {},
     "outputs": []
    }
   ],
   "metadata": {}
  }
 ]
}
""")
    outputstr = temp.substitute(filetitle = str(fname), modeldes = str(modelcon))
    srcfile.close()
    return outputstr

def delseq(floc):
    try:
        os.remove(floc)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def exitseq():
    raw_input('Press enter to exit.')
    exit(0)

