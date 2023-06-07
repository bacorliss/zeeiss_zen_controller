#!/usr/bin/env python
"""
Copyright (c) 2012, Bruce A. Corliss
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the BACETech Consulting nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Bruce A. Corliss BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import os
import sys
import re

script_path = os.path.dirname(sys.argv[0])
print "Script Path: " + script_path

proj_path = os.path.abspath(os.path.join(script_path, os.path.pardir))

with open(os.path.join(proj_path, 'css','main.css'), 'r') as f:
    css_text = f.read()


files = [f for f in os.listdir('.') if re.match('.*bas$|.*cls', f)]
files.reverse()

fido = open(os.path.join(proj_path, 'tcp_commands.html'), 'w')
fido.write('<!DOCTYPE html>\n<html>\n')
fido.write('<head>\n\n<title> Zen Controller TCP Commands </title>\n')
fido.write('<style media="screen" type="text/css">\n' + css_text + '\n</style>\n')
fido.write('</head>\n\n')
fido.write('<body>\n\n<h1>Index of TCP Command for Zen Controller</h1>\n')


def print_h2(line):
    print "h2: " + re.sub(r'\'', '', line).strip()
    fido.write('<br>\n<br>\n<h2>' + line + '</h2>\n')
    
def print_h3(line):
    print "h3: " + re.sub(r'\'', '', line).strip()
    fido.write('<br>\n<h3>' + line + '</h3>\n')
    
def print_p(line):
    print "p : " + re.sub(r'\'', '', line).strip()
    fido.write('<p>' + line + '</p>\n')

for fname in files:
    print "Scraping: " + fname
    fidi = open(fname, 'r')
    txt = fidi.read()
    fidi.close()

    WITHIN_SWITCH = False
    WITHIN_CASE = False
    WITHIN_COMMENT = False
    for idx,line in enumerate(txt.splitlines()):
        #print idx,line
        if len(line.strip())==0: continue
        elif re.match(r'.*Select Case ',line):
            WITHIN_SWITCH = True
            print_h2(txt.splitlines()[idx-1].replace('\'',''))
        elif re.match(r'.*End Select', line):
            WITHIN_SWITCH = False
        elif re.match(r'.*Case.*', line) and WITHIN_SWITCH:
            
            print_h3(re.sub(r'\"','',line.replace('Case','')))
            WITHIN_CASE = True
            WITHIN_COMMENT = True
        elif re.match(r'^\s*\'', line) and WITHIN_COMMENT:
            print_p(re.sub(r'\'','',line))
        else:
            WITHIN_CASE = True
            WITHIN_COMMENT = False    


fido.write('\n<br><br><br>\n</body>\n</html>')
fido.close()
