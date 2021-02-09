## About
This repository contains some basic python scripts to deal with xib's in iOS.

## Overview
- A Xib file in iOS usually specifies a view of some kind eg, UIViewController, UIView, UITableViewCell, UICollectionViewCell, etc.
- Each XIB is mapped to a class that belongs to a target.
- XIB file is nothing just a huge XML file.
- At build time the Xcode compiles your xib file to a binary file known as nibs, **nibs** are loaded at runtime in the memory and used for creation of Views.
- Checking the usage of each XIB in code manually would be a tedious and time consuming task.

## Problem Statements
- Identify the unused XIB's or dead XIB's in the iOS project codebase and list them down.
- Prepare the mapping of Xcode Targets and XIB's. 

## Solution Approach
<ol type=1>
  <li>Each XIB file contains information about the view class it is mapped to.</li>
  <li>Simply iterate over all the XIB.</li>
  <li>Open XIB in XML format and read the custom module tag value.</li>
  <li>Simply map the XIB's to custom classes</li>
  <li>Iterate the swift files present in src/Payments/Internal and prepare the list of all swift classes</li>
  <li>Simply check if Xib custom class is available in the list of swift classes.</li>
  <li>Any Xib whose custom class name is not present in the list of Swift classes should be the dead XIB.</li>
</ol>

## unused_xibs.py
This script will simply list down the list of unused xib's in the source file path being passed to the script. 

## xib_owners.py
This script will prepare the XIB's and module mapping. i.e which XIB belong to which target.

## Setup
You need to have python3 installed on your machine.

## Usage
unused_xibs.py
```
python3 unused_xibs.py source_files_path
```
Sample Output -
```
List of unused XIB's
===================
a.xib
b.xib
c.xib
```

xib_owners.py
```
python3 xib_owners.py source_files_path
```
Sample Output
```
Total number Xib's in Module {module_name/target_name} = {total xib's count}
===================================================================
a.xib
b.xib
c.xib
```
