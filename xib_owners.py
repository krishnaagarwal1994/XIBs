import os
from xml.etree import ElementTree
import sys

def filterFilesWithExtension(fileName, fileExtension):
    return fileName.endswith(fileExtension)

def filter_xib_files(fileName):
    return filterFilesWithExtension(fileName, ".xib")

def getCustomModuleNameForXib(xibName, xibPath):
    filePath = "%s/%s"% (xibPath, xibName)
    xmltreeRoot = ElementTree.parse(filePath).getroot()
    for tag in xmltreeRoot.findall("objects/placeholder"):
        value = tag.get("customModule")
        if value is not None:
            return value
    for tag in xmltreeRoot.findall("objects/tableViewCell"):
        value = tag.get("customModule")
        if value is not None:
            return value
    for tag in xmltreeRoot.findall("objects/collectionViewCell"):
        value = tag.get("customModule")
        if value is not None:
            return value
    for tag in xmltreeRoot.findall("objects/view"):
        value = tag.get("customModule")
        if value is not None:
            return value
    return None

def prepareModuleXibMapping():
    os.chdir(source_file_path)
    moduleXibMapping = {}
    for root, directories, files in os.walk(os.getcwd()):
        xibs = list(filter(filter_xib_files, files))
        for xibFile in xibs:
            xibModuleName = getCustomModuleNameForXib(xibFile, root)
            if xibModuleName is not None:
                if xibModuleName in moduleXibMapping:
                    moduleXibMapping[xibModuleName].append(xibFile)    
                else:
                    moduleXibMapping[xibModuleName] = [xibFile]
    return moduleXibMapping

def print_mapping(moduleXibMapping):
    for key, value in moduleXibMapping.items():
        print("Total number XIB's in Module", key, "=",len(value))
        print("===================================================================")
        for item in value:
            print(item)
        print("\n")


if len(sys.argv) == 2:
    source_file_path = sys.argv[1]
    moduleXibMapping = prepareModuleXibMapping()
    print_mapping(moduleXibMapping)
else:
    print("Please enter the source files path as the script argument.")