#!/usr/bin/python
# Mockup script demonstrating pipeline for JXqc with remote prospector search.

from prospectorManipulations import *
import os
import re
from sys import argv

# Directory Structure:

dirTree = {
    'topDir': "/home/socr/c/users2/prospector/prospectorJX",
    'peaklistDir': "peaklists",
    'projectDir': "projects",
    'batchTagDir': "batchtags",
    'searchCompDir': "searchcompares",
    'outputDir': "outputs",
    'btTemplate': "/templates/bt_template_JXSTD.xml",
    'scTemplate': "/templates/sc_template_JXSTD.xml"
}

topDir = os.path.realpath(dirTree['topDir'])
del dirTree['topDir']
for key, dirName in dirTree.items():
    dirTree[key] = os.path.join(topDir, dirName)

peaklistFile = os.path.basename(argv[1])
projectName = re.sub('(\_|\.).+$', '', peaklistFile)
peaklistFile = os.path.join(dirTree['peaklistDir'], peaklistFile)

makeProjectFromPeaklist(peaklistFile, dirTree['projectDir'])
makeBatchTagFromTemplate(dirTree['btTemplate'], projectName, dirTree['projectDir'], dirTree['batchTagDir'], dirTree['outputDir'])
makeSearchCompareFromTemplate(dirTree['scTemplate'], projectName, dirTree['searchCompDir'], dirTree['outputDir'])

#dirTree['peaklistFile'] = peaklistFile
#for k, v in dirTree.items():
#    print(k + ":" + v)


