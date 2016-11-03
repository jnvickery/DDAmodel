# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 09:53:28 2016

@author: john vickery

Purpose:
    Pass ISBNs to Syndetics web service to get book summary
    Subscription to Syndetics is required
    Sample URL: http://www.syndetics.com/index.aspx?isbn=1619026279/SUMMARY.XML&client=<CLIENTID HERE>
    XML response
    <Notes>
        <Fld520 I1="BLANK" I2="BLANK">
            <a>
                SUMMARY	

   The form of the input CSV file is assumed to be:
   CATKEY (or other ILS identifier), ISBN1, ISBN2, ISBN3,.....,ISBN<n>
   
"""

import csv
import itertools      # use below to avoid processing entire csv file
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# input file and URL for Syndetics
fname = 'isbn.csv'
serviceurl = 'http://www.syndetics.com/index.aspx?isbn='
suffix = '/SUMMARY.XML&client=<CLIENTID HERE>'

# range of input file to process
start = 0
stop  = 100

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
                    soup = BeautifulSoup(data, 'html.parser')
                    if len(soup.find_all('title')) == 0:
                        tree = ET.fromstring(data)
                        summary = tree.findall('VarFlds/VarDFlds/Notes/Fld520')
                        for a in summary:
                            datalst.append(a.find('a').text)
                            lst.append(datalst)

# output to CSV
outfile = 'Syndetic\SyndeticSummary_' + str(start) + '-' + str(stop) + '.csv'

with open(outfile, "w", encoding='utf-8', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(lst)

# close the file
f.close()
