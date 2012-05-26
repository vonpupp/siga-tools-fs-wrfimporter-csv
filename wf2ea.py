# -*- coding: utf-8 -*-
#!/usr/bin/env python

#   Project:			SIGA-CCB
#   Component Name:		wf2ea
#   Language:			bash
#
#   License: 			GNU Public License
#       This file is part of the project.
#	This is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#       without even the implied warranty of MERCHANTABILITY or
#       FITNESS FOR A PARTICULAR PURPOSE.
#       See the GNU General Public License for more details.
#       <http://www.gnu.org/licenses/>
#
#   Author:			Albert De La Fuente (www.albertdelafuente.com)
#   E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01w-AN5Lq7Y3PxXFPUMAurig==&c=5RdpY03cYkLHKGAfUQ_0RBQWTiOfBrBreDLUqwD6Dr4=
#
#   Description:		This script will parse a full hierarchy from a path
#        and build a csv representing the wireframes from the project
#
#   Limitations:		Error handling is not implemented, time constraints
#	The code is not clean and elegant as it should, again, time constraints
#   Database tables used:	None 
#   Thread Safe:	        No
#   Extendable:			No
#   Platform Dependencies:	Linux (openSUSE used)
#   Compiler Options:		

"""
    Create a CSV file with the wireframe data based on a hierarchy.

    Command Line Usage:
        wf2ea {<option> <argument>}

    Options:
        -h, --help              Print this help and exit.
        
        -p, --path <path>                   Path to process.
        -r. --replace <path>                Path to be replaced (old) on each wireframe with the given one by the --fix option.
        -f, --fix <path>                    Path which will replace (new) each wireframe. Use in conjuntion with the --replace option.
        -o, --out <outfile>                 Generated csv file.
        -v, --verbose <level>               Verbose output. Level in 2..4
        -l, --log <logfile>                 log to file.
        
    Examples:
        wf2ea.py -p ./wf -o ./out.csv          Will parse ./wf and produce the out.csv file
        wf2ea.py -p ./wf -o ./out.csv -v 3     Same as above with level 3 __verbosity
        wf2ea.py -p ~/siga/siga-svn/DesenvolvimentoSiga/PROJETO_SIGA/3.TEP\ -\ Consolidado/ \\
                 -r /home/afu/siga/siga-svn/ \\
                 -f C:\\SIGA\\DesenvolvimentoSiga\\PROJETO_SIGA\\3.TEP - Consolidado\\3. Wireframes\\ \\
                 -o ./out.csv -v 2
"""

import getopt
import logging
import sys
import os
import csv

#---- exceptions

#---- global data

VERB_NON = 0
VERB_MIN = 1
VERB_MED = 2
VERB_MAX = 3

class WF():
    """ Main problem class
    Attributes:
        - path, prependpath, replacepath, outfile: string
    """
    
    def __init__(self):
        # TODO: Private / protected
        self.__verbosity = 0
        self.__logger = logging.getLogger('wf2ea')
        self.__loghdlr = None
        self.__formatter = None
        self.__wflist = []
        self.__wfcount = 0
        self.csvhdlr = None
        # Public
        self.path = ""
        self.prependpath = ""
        self.replacepath = ""
        self.outfile = "" # sys.stdout
        pass
    
    #---- internal support stuff
    
    def logv(self, v, str):
        #print "logv().v=%d" % v
        #print "main().__verbosity=%d" % __verbosity
        if self.__verbosity == v:
            print str

    def isVerbose(self):
        return self.__verbosity > 1
    
    def setLogger(self, str):
        self.__loghdlr = logging.FileHandler(str)
        self.__formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.__loghdlr.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__loghdlr)
        if self.__verbosity == 2:
            self.__logger.setLevel(logging.INFO)
            self.__logger.info("Starting to log (INFO)...")
        elif self.__verbosity == 3:
            self.__logger.setLevel(logging.DEBUG)
            self.__logger.info("Starting to log (DEBUG)...")

    def fixpath(self, path, old, new):
        path = path.replace(old, new)
        path = path.replace("/", "\\")
        #self.logv(VERB_MIN, "fixpath().path=" + path + "\n")
        return path
        pass
   
    def parseDir(self):
        self.logv(VERB_MIN, "-> parsedir()")
        self.__wflist = []
        self.__wfcount = 0
        #if self.path == ""
        for dirname, dirnames, filenames in os.walk(self.path):
            if '.svn' in dirnames:
                dirnames.remove('.svn')
            for subdirname in dirnames:
                pass
            for filename in filenames:
                if filename.endswith(('.png')):
                    self.__wfcount += 1
                    wffile = os.path.join(dirname, filename)
                    #self.logv(VERB_MIN, "parsedir().wffile=%s" % (wffile))
                    
                    wffile = self.fixpath(wffile, "/home/afu/siga/siga-svn/", "C:\\SIGA\\")
                    
                    wftuple = [filename, 'Artifact',
                        '<a href="' + wffile + '"><font color="#0000ff"><u>' + wffile + '</u></font></a>',
                        'File', 'Albert De La Fuente', filename, wffile]
                    
                    #self.logv(2, "parsedir().wftuple=" + str(wftuple))
                    #self.logv(2, "parsedir().wftuple=%s" .join(map(str, wftuple)))
                    self.__wflist.append(wftuple)
                    pass
        self.logv(VERB_MIN, "parsedir().result=%d" % self.__wfcount)
        self.logv(VERB_MIN, "-> parsedir()")
        return self.__wfcount

    def writecsv(self):
        if self.outfile != "":
            fh = open(self.outfile, 'wb')
            #fh = codecs.open(self.outfile, 'wb', encoding="utf-8")
        else:
            fh = sys.stdout

        csvhdlr = csv.writer(fh, delimiter='\t')#, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
        csvhdlr.writerow(["Name", "Type", "Notes", "Stereotype", "Author", "Alias", "GenFile"])
        for row in self.__wflist:
            csvhdlr.writerow(row)
            #self.logv(2, "writecsv().row = " + str(row))
        #self.logv(2, "writecsv().outfile = " + self.outfile)
    
    #---- mainline

def main(argv):
    wfl = WF()
    try:
        optlist, args = getopt.getopt(argv[1:], 'hp:r:f:o:v:l:', ['help', 'path', 'replace', 'fix', 'out', 'verbose', 'log'])
    except getopt.GetoptError, msg:
        sys.stderr.write("wf2ea: error: %s" % msg)
        sys.stderr.write("See 'wf2ea --help'.\n")
        return 1

    print str(optlist)
    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ('-p', '--path'):
            wfl.path = optarg
            pass
        elif opt in ('-r', '--replace'):
            wfl.replacepath = optarg # "/home/afu/siga/siga-svn/"
            pass
        elif opt in ('-f', '--fix'):
            wfl.prependpath = optarg # "C:\\SIGA\\"
            pass
        elif opt in ('-o', '--out'):
            wfl.outfile = optarg
            print "(-o) OUTPUT:  " + optarg
            pass
        elif opt in ('-v', '--verbose'):
            #hdlr = logging.FileHandler('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
            #__formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            #hdlr.setFormatter(__formatter)
            #__logger.addHandler(hdlr)
            wfl.__verbosity = int(optarg)
            wfl.logv(2, "main.optarg[%d]" % len(optlist))
            wfl.logv(2, "main.optarg = " .join(map(str, optarg)))
            wfl.logv(2, "main.optlist = " .join(map(str, optlist)))
            #print "__verbosity=%d" % __verbosity
            #wfl.__verbosity = int(optarg)
            #print "__verbosity=%d" % __verbosity
            #print "optarg=%s" % optarg
            #if __verbosity == 2:
            #    __logger.setLevel(logging.INFO)
            #    __logger.info("Starting to log (INFO)...")
            #elif __verbosity == 3:
            #    __logger.setLevel(logging.DEBUG)
            #    __logger.info("Starting to log (DEBUG)...")
            pass
        elif opt in ('-l', '--log'):
            wfl.logfile = optarg            
            wfl.logv(2, "main.optarg = " .join(map(str, optarg)))
            if wfl.isVerbose:
                #wfl.logv(2, "main.optarg = " + optarg)
                wfl.setLogger('/home/afu/Dropbox/mnt-ccb/siga/siga-tools/siga-tools-wf2ea/myapp.log')
            pass

    wfl.parseDir()
    #wfl.logv(VERB_NON, "main.optarg = " .join(map(str, optarg)))
    #wfl.logv(1, "main.wfl.optarg = " .join(map(str, wfl.__wflist)))
    wfl.writecsv()
    print "INPUT:   " + wfl.path
    print "OUTPUT:  " + wfl.outfile
    print " * Replace:  " + wfl.replacepath
    print " * Fix with: " + wfl.prependpath

    #if len(args) == 0:
    #    sys.stderr.write("wf2ea: error: incorrect number of "\
    #                     "arguments: argv=%r\n" % argv)
    #    return 1
    #else:
#    elif len(args) <= 1:
        #path = args[0]
        #if len(args) <= 2:
        #    outfile = argv[1]

    #try:
        #wfl.processDir(path) #, outfile) #, defines)
        #print "path=" + path
        #wfl.parseDir(path)
        #wfl.logv(2, "main.wfl.optarg = " .join(map(str, wfl.__wflist)))
        #wfl.fixpaths()
        #wfl.writecsv()
        
        #wfl.processWF(path)
        #wfl.writecsv()
    #except: # PreprocessError, ex:
    #    sys.stderr.write("wf2ea: error: %s\n") # % str(ex))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
