import os
import re
from sys import argv
import xml.etree.ElementTree as ET

directory = argv[1]
outDir = argv[2]

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def get_peaklists(dir, outputDir="./"):
    path = os.path.realpath(dir)
    print path
    if os.path.isdir(path):
        projectName = os.path.basename(path)
        peaklists = [f for f in os.listdir(path) if re.search(r"^[A-Z].*\d{6}\-\d{2}.*\.(txt)|(mgf)$",f)]
        dir = path
    else:
        dir = os.path.split(path)[0]
        f = os.path.split(path)[1]
        projectName = re.sub('\..+', '', f)
        projectName = re.sub('\_.+', '', f)
        peaklists = [f]
    outputFile = outputDir + projectName + ".xml"
    project = ET.Element("project")
    ET.SubElement(project,"project_name").text = projectName
    for f in peaklists:
        filePath = dir + "/" + f
        file = ET.SubElement(project, "file")
        ET.SubElement(file, "centroid").text = filePath
        peaklist_file = open(filePath, "r")
        count = peaklist_file.read().count("BEGIN IONS")
        print f + ":\t" + str(count) + " spectra"
        ET.SubElement(file, "num_msms_spectra").text = str(count)
        peaklist_file.close()
        ET.SubElement(file, "centroid_name").text = f
    indent(project)
    ET.ElementTree(project).write(outputFile, encoding="UTF-8")


get_peaklists(directory, outDir)

