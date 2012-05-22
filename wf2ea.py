#!/usr/bin/env python

#   Project:			SIGA-CCB
#   Component Name:		wf2ea
#   Language:			bash
#
#   License: 			GNU Public License
#       This file is part of req2ea.
#	This is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Foobar is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Foobar.  If not, see <http://www.gnu.org/licenses/>. 
#
#   Author:			Albert De La Fuente (www.albertdelafuente.com)
#   E-Mail:			vonpupp@gmail.com
#
#   Description:		This script will parse a full hierarchy from a path
#        and build a cvs representing the wireframes from the project
#
#   Limitations:		Error handling is not implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		

"""
    Create a CVS with the wireframe data based on a hierarchy.

    Command Line Usage:
        wf2ea [<options>...] <dir>

    Options:
        -h, --help              Print this help and exit.
        
        -v, --verbose <level>   Verbose output. Level in 2..4
        -l, --log <logfile>     log to file
        -o, --out <outfile>            Generated csv file.
"""

import getopt
import logging
import sys
import os
import csv

#---- exceptions

#---- global data

class WF(object):
    """Class"""

    #log = logging.getLogger("wf2ea-log")
    
    #verbosity = None
    #logger = None
    
    def __init__(self):
        self.verbosity = 1
        self.logger = logging.getLogger('wf2ea')
        self.outfile = sys.stdout
        self.loghdlr = None
        self.formatter = None
        self.wflist = []
        self.wfcount = 0
        self.csvhdlr = None
        pass
    
    #---- internal support stuff
    
    def logv(self, v, str):
        #print "logv().v=%d" % v
        #print "main().verbosity=%d" % verbosity
        if self.verbosity == v:
            print str
            
    def setLogger(self, str, verb):
        self.loghdlr = logging.FileHandler(str)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.loghdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.loghdlr)
        self.verbosity = verb
        #print "verbosity=%d" % verbosity
        #print "optarg=%s" % optarg
        if self.verbosity == 2:
            self.logger.setLevel(logging.INFO)
            self.logger.info("Starting to log (INFO)...")
        elif self.verbosity == 3:
            self.logger.setLevel(logging.DEBUG)
            self.logger.info("Starting to log (DEBUG)...")

    
    def fixpath(self, path, old, new):
        path = path.replace(old, new)
        path = path.replace("/", "\\")
        self.logv(2, "fixpath().path=" + path + "\n")
        return path
        pass
    
    def fixpaths(self, prefix):
        for csvname, csvtype, csvnotes, csvstereotype, csvauthor, csvalias, csvgenfile in lis:
            csvnotes = fixpath(csvnotes, prefix)
            print "fixedpaths: " + csvgenfile + "\n"
            csvgenfile = self.fixpath(csvgenfile, prefix)
            print "fixedpaths: " + csvgenfile + "\n"
        pass
    
    def parsedir(self, path):
        #lis = [];
        self.wfcount = 0
        for dirname, dirnames, filenames in os.walk(path):
            if '.svn' in dirnames:
                dirnames.remove('.svn')
            #print " d:%s" % (dirname)
            for subdirname in dirnames:
                #print "     sd:%s" % (os.path.join(dirname, subdirname))
                pass
            for filename in filenames:
                if filename.endswith(('.png')):
                    self.wfcount += 1
                    wffile = os.path.join(dirname, filename)
                    wffile = self.fixpath(wffile, "/home/afu/siga/siga-svn/", "C:\\SIGA\\")
                    self.logger.debug("parsedir().filename=%s", filename)
                    self.wflist.append([filename, 'Artifact', '<a href="' + wffile + '"><font color="#0000ff"><u>' + wffile + '</u></font></a>', 'File', 'Albert De La Fuente', filename, wffile])
                    #print "         f:%s" % (wffile)
                    pass
                #print "%s %s %s" % (os.path.join(dirname, filename), " ext: ", filename.lower())
                #log.info("mainwf2ea(path=%r, outfile=%r)",
                #path, outfile)
        self.logv(2, "parsedir().result=%d" % self.wfcount)
        return self.wfcount
    
    def writecsv(self, csvhdlr):
        #self.csvhdlr.
        csvhdlr.writerow(["Name", "Type", "Notes", "Stereotype", "Author", "Alias", "GenFile"])
        #csv.DictWriter(self.csvhdlr).writerow(["Name", "Type", "Notes", "Stereotype", "Author", "Alias", "GenFile"])
        for row in self.wflist:
            #print "writecvs: " + row[6] + "\n"
            csvhdlr.writerow(row)
    
    def processWF(self, path): #, outfile):
        #Name, Type, Notes, Stereotype, Author, Alias, GenFile
        # lavrar_ata_trimestral_cadastro.png, Artifact, <a href="path"><font color="#0000ff"><u>file.png</u></font></a>, File, Albert De La Fuente,	path.png
        fh = open('eggs.csv', 'wb')
        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        self.wflist = []
        self.wfcount = self.parsedir(path)
        #print "number of wf = %d" % wfcount
        #fixpaths(lis, "C:\\doc\\")
        self.writecsv(csvhdlr)
        #print lis
    
    #---- mainline

def main(argv):
    wfl = WF()
    try:
        optlist, args = getopt.getopt(argv[1:], 'hv:l:o:', ['help', 'verbose', 'log', 'out'])
    except getopt.GetoptError, msg:
        sys.stderr.write("wf2ea: error: %s" % msg)
        sys.stderr.write("See 'wf2ea --help'.\n")
        return 1
    #wfl.outfile = sys.stdout
    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ('-v', '--verbose'):
            #hdlr = logging.FileHandler('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
            #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            #hdlr.setFormatter(formatter)
            #logger.addHandler(hdlr)
            wfl.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log', int(optarg))
            #print "verbosity=%d" % verbosity
            #wfl.verbosity = int(optarg)
            #print "verbosity=%d" % verbosity
            #print "optarg=%s" % optarg
            #if verbosity == 2:
            #    logger.setLevel(logging.INFO)
            #    logger.info("Starting to log (INFO)...")
            #elif verbosity == 3:
            #    logger.setLevel(logging.DEBUG)
            #    logger.info("Starting to log (DEBUG)...")
            pass
        elif opt in ('-l', '--log'):
            pass
        elif opt in ('-o', '--out'):
            outfile = optarg
            pass
        

    #log.info("main(len(args)=%r)", len(args))

    if len(args) == 0:
        sys.stderr.write("wf2ea: error: incorrect number of "\
                         "arguments: argv=%r\n" % argv)
        return 1
    elif len(args) <= 1:
        path = args[0]
        #if len(args) <= 2:
        #    outfile = argv[1]

    #try:
        #wfl.processDir(path) #, outfile) #, defines)
        wfl.processWF(path)
    #except: # PreprocessError, ex:
    #    sys.stderr.write("wf2ea: error: %s\n") # % str(ex))

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
