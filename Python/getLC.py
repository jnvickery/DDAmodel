# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 11:18:37 2016

@author: jnvicker

Purpose:
    Pass ISBNs to OCLC's Classify web service to get LC classification
    for DDAmodel items that have XX... sortcall

    Sample URL: http://classify.oclc.org/classify2/Classify?isbn=9782763790428&summary=true
    XML response
    Failed response = <response code="101"/>
    
    Classify API: http://www.oclc.org/developer/develop/web-services/classify.en.html

NOTES:
    use next() function in csv.reader to skip the header

"""

import csv
import itertools      # use below to avoid processing entire csv file
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

# input file and URL for Syndetics
fname = 'ISBNforLC.csv'
serviceurl = 'http://classify.oclc.org/classify2/Classify?isbn='
suffix = '&summary=true'

# range of input file to process
start = 1001
stop  = 3443

lst = list()
with open(fname, newline='') as f:
    reader = csv.reader(f)
    for row in itertools.islice(reader, start, stop):
        datalst = list()
        datalst.append(row[0])
        for index, isbn in enumerate(row[1:len(row)-1], start=1):
            if len(datalst) < 2:  # only loop if haven't retrieved summary for ISBN yet
                if row[index]:
                    url = serviceurl+isbn+suffix
                    handle = urllib.request.urlopen(url)
                    data = handle.read()
                    tree = ET.fromstring(data)
                    for l in tree.findall('.//{http://classify.oclc.org}lcc'):
                        mp = l.find('{http://classify.oclc.org}mostPopular')
                        datalst.append(mp.get('nsfa'))
                        lst.append(datalst)

# output to CSV
outfile = 'LC\LC_' + str(start) + '-' + str(stop) + '.csv'

with open(outfile, "w", encoding='utf-8', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(lst)

# close the file
f.close()
