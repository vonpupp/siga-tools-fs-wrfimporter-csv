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
        -h, --help      Print this help and exit.
        -v, --verbose   Give verbose output for errors.
        
        -o <outfile>    Write output to the given file instead of to stdout.

    Module Usage:
        from preprocess import preprocess
        preprocess(infile, outfile=sys.stdout, defines={})

"""

import getopt
import logging
import sys
import os
import csv

#---- exceptions

#---- global data

#log = logging.getLogger("wf2ea")


#---- internal support stuff

def parsedir(path):
    lis = [];
    for dirname, dirnames, filenames in os.walk(path):
        if '.svn' in dirnames:
            dirnames.remove('.svn')
        #print " d:%s" % (dirname)
        for subdirname in dirnames:
            #print "     sd:%s" % (os.path.join(dirname, subdirname))
            pass
        for filename in filenames:
            if filename.endswith(('.png')):
                wffile = os.path.join(dirname, filename)
                lis.append([filename, 'Artifact', '<a href="' + wffile + '"><font color="#0000ff"><u>' + wffile + '</u></font></a>', 'File', 'Albert De La Fuente', wffile])
                print "         f:%s" % (wffile)
                pass
            #print "%s %s %s" % (os.path.join(dirname, filename), " ext: ", filename.lower())
    #log.info("mainwf2ea(path=%r, outfile=%r)",
             #path, outfile)
    return lis

def mainwf2ea(path, outfile):
    #Name, Type, Notes, Stereotype, Author, Alias, GenFile
    # lavrar_ata_trimestral_cadastro.png, Artifact, <a href="path"><font color="#0000ff"><u>file.png</u></font></a>, File, Albert De La Fuente,	path.png
    fh = open('eggs.csv', 'wb')
    wr = csv.writer(fh, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    lis = parsedir(path)
    wr.writerow(lis)
    print lis

#---- mainline

def main(argv):
    try:
        optlist, args = getopt.getopt(argv[1:], 'hvo:', ['help', 'verbose'])
    except getopt.GetoptError, msg:
        sys.stderr.write("wf2ea: error: %s" % msg)
        sys.stderr.write("See 'wf2ea --help'.\n")
        return 1
    outfile = sys.stdout
    defines = {}
    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            sys.stdout.write(__doc__)
            return 0
        elif opt in ('-v', '--verbose'):
            pass
            #log = logging.getLogger("sample")
            #log.setLevel(logging.DEBUG)
            #log.basi logging.basicConfig(filename='cvs.log',level=logging.DEBUG)
        elif opt == '-o':
            outfile = optarg
        #elif opt == '-D':
        #    if optarg.find('=') != -1:
        #        var, val = optarg.split('=', 1)
        #        try:
        #            val = eval(val, {}, {})
        #        except:
        #            pass
        #    else:
        #        var, val = optarg, None
        #    defines[var] = val

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
        mainwf2ea(path, outfile) #, defines)
    #except: # PreprocessError, ex:
    #    sys.stderr.write("wf2ea: error: %s\n") # % str(ex))

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
