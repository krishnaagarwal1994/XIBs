import os
from xml.etree import ElementTree
import sys

# filter files with the given extension
def filterFilesWithExtension(fileName, fileExtension):
    return fileName.endswith(fileExtension)

# filter files with .swift extension
def filter_swift_files(fileName):
    return filterFilesWithExtension(fileName, ".swift")

# filter files with .xib extension
def filter_xib_files(fileName):
    return filterFilesWithExtension(fileName, ".xib")

# Return all the classes declared in a swift file
def getClassesInAFile(fileName, directory):
    filePath = "%s/%s"% (directory, fileName)
    f = open(filePath, "r")
    classes = []
    for line in f:
        if "class " in line:
            words = line.split()
            try:
                classNameIndex = words.index("class") + 1
                wordNextToClassKeyword = words[classNameIndex]
            except ValueError:
                continue
            if wordNextToClassKeyword in ["func", "is", "var", "{", "{}"]:
                continue
            if ":" in wordNextToClassKeyword:
                wordNextToClassKeyword = wordNextToClassKeyword[0: len(wordNextToClassKeyword) - 1]
            classes.append(wordNextToClassKeyword)
    f.close()
    return classes

# Return the class name to which the xib belong
def getCustomClassNameForXib(xibName, xibPath):
    customClassNames = []
    filePath = "%s/%s"% (xibPath, xibName)
    xmltreeRoot = ElementTree.parse(filePath).getroot()
    for tag in xmltreeRoot.findall("objects/placeholder"):
        value = tag.get("customClass")
        if value is not None and value != "UIResponder":
            customClassNames.append(value)
    for tag in xmltreeRoot.findall("objects/tableViewCell"):
        value = tag.get("customClass")
        if value is not None and value != "UIResponder":
            customClassNames.append(value)
    for tag in xmltreeRoot.findall("objects/collectionViewCell"):
        value = tag.get("customClass")
        if value is not None and value != "UIResponder":
            customClassNames.append(value)
    for tag in xmltreeRoot.findall("objects/view"):
        value = tag.get("customClass")
        if value is not None and value != "UIResponder":
            customClassNames.append(value)
    return customClassNames

# Return the target name to which the xib's class name belong
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

# XIB class declaration
class XIB:
    def __init__(self, xibName, xibPath, customClassName, customModuleName):
        self.xibName = xibName
        self.xibPath = xibPath
        self.customClassName = customClassName
        self.customModuleName = customModuleName

    def __str__(self):
        return self.xibName + " - Module name = " + self.customModuleName

# Returns the list of XIB type from the current os path
def getXibListAtPath(pathString):
    xibList = []
    for root, dirs, files in os.walk(pathString):
        xibFiles = list(filter(filter_xib_files, files))
        for xib in xibFiles:
            customClassName = getCustomClassNameForXib(xib, root)
            customModuleName = getCustomModuleNameForXib(xib, root)
            if customModuleName == None:
                customModuleName = ""
            xibObject = XIB(xib, root, customClassName[0], customModuleName)
            xibList.append(xibObject)
    return xibList

# Returns array of swift classes at the given path
def getSwiftClassesAtPath(file_source_path):
    swiftClasses = []
    for root, dirs, files in os.walk(file_source_path):
        swiftFiles = list(filter(filter_swift_files, files))
        for file in swiftFiles:
            classList = getClassesInAFile(file, root)
            if len(classList) != 0:
                swiftClasses.extend(classList)
    return swiftClasses

# Prints all the XIB's that are present in file_source_path
def printUnusedXibs(file_source_path):
    os.chdir(file_source_path)
    xibList = getXibListAtPath(os.getcwd())
    swiftClasses = getSwiftClassesAtPath(os.getcwd())

    print("\nTotal XIB's", len(xibList))
    print("List of unused XIB's")
    print("===================")
    paringAvailable = 0
    for xib in xibList:
        paringAvailable = 0
        for swiftClass in swiftClasses:
            if xib.customClassName == swiftClass:
                paringAvailable = 1
        if paringAvailable == 0:
            print(xib.xibName)

if len(sys.argv) == 2:
    file_source_path = sys.argv[1]
    printUnusedXibs(file_source_path)
else:
    print("Please enter the source files path as the script argument.")