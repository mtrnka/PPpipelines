import os
import re
import xml.etree.ElementTree as ET

def indent(elem, level=0):
#Some function I copied off of internet to help make xml output more readable
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

def makeProjectFromPeaklist(target, outputDir="./"):
#Takes either single mgf or directory as input
    path = os.path.realpath(target)
    print path
    if os.path.isdir(path):
        projectName = os.path.basename(path)
        peaklists = [f for f in os.listdir(path) if re.search(r"^[A-Z].*\d{6}\-\d{2}.*\.(txt)|(mgf)$",f)]
        target = path
    else:
        target = os.path.split(path)[0]
        f = os.path.split(path)[1]
        projectName = re.sub('(\_|\.).+$', '', f)
        peaklists = [f]
    outputFile = os.path.join(outputDir, projectName + ".xml")
    project = ET.Element("project")
    ET.SubElement(project,"project_name").text = projectName
    for f in peaklists:
        filePath = target + "/" + f
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

def makeBatchTagFromTemplate(btTemplateFile, projFileName, projDir, batchTagDir, outDir):
    batchTagFileName = "bt_" + projFileName + ".xml"
    batchTagFile = os.path.join(batchTagDir, batchTagFileName)
    outFileName = projFileName + "_BTout"
    print(batchTagFile)

    templ = open(btTemplateFile, "r")
    templ = templ.read()
    templ = templ.replace("___PROJFILENAME___", projFileName)
    templ = templ.replace("___OUTFILENAME___", outFileName)
    templ = templ.replace("___PROJPATH___", projDir)
    templ = templ.replace("___OUTPATH___", outDir)
    bf = open(batchTagFile, "w+")
    bf.write(templ)
    bf.close()

def makeSearchCompareFromTemplate(scTemplateFile, projFileName, searchCompDir, outDir):
    searchCompareFileName = "sc_" + projFileName + ".xml"
    searchCompareFile = os.path.join(searchCompDir, searchCompareFileName)
    outFileName = projFileName + "_SCout.txt"
    btOutFileName = projFileName + "_BTout.xml"
    resultsFullPath = os.path.join(outDir, btOutFileName)
    print(searchCompareFile)
    print(os.path.join(outDir, outFileName))

    templ = open(scTemplateFile, "r")
    templ = templ.read()
    templ = templ.replace("___OUTFILENAME___", outFileName)
    templ = templ.replace("___OUTPATH___", outDir)
    templ = templ.replace("___RESFULLPATH___", resultsFullPath)
    bf = open(searchCompareFile, "w+")
    bf.write(templ)
    bf.close()

