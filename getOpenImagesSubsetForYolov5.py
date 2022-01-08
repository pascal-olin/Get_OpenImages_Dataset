#!/usr/bin/env python
""" get images files with annotation from https://storage.googleapis.com/openimages/web/download.html
this code will help to find and download relevant image files and annotation from the gigantic openimages repository to create a personal dataset aimed for object recognition (e.g. Yolo_

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Pascal Olin"
__authors__ = ["Pascal Olin"]
__contact__ = "polin1962@gmail.com"
__copyright__ = "Copyright 2022, PO"
__credits__ = ["Pascal Olin", "see contributors at https://storage.googleapis.com/openimages/web/extras.html"]
__date__ = "2022/01/08"
__deprecated__ = False
__email__ =  "polin1962@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Pascal Olin"
__status__ = "Production"
__version__ = "0.1.1"

# first download a copy of BOXed images names at : https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv 
# keep only a subset of this file (for example the first million record : head -n 1000000 <downloaded big file name> > <new smaller file name> 
# it will be our --imageids parameter file 
# then download a copy of class names at  : https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
# it will be our --categories parameter file 


import os 
import argparse
import csv
import shutil
parser = argparse.ArgumentParser()
parser.add_argument("-c","--categories", help="Code/category filename")
parser.add_argument("-i","--imagesids", help="imageids  filename")
parser.add_argument("-o","--outpath", help="output directory",default="./outpath")
args = parser.parse_args()
# codeCategoryFile is extracted from : https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
# Categories we are interested with 
myCategories= ["Cat","Sunglasses","Laptop","Person",
                        "Toothbrush","Apple","Toaster",
                        "Chair","Door","Coffee",
                        "Scissors",
                        "Computer mouse",
                        "Coin",
                        "Computer monitor",
                        "Table",
                        "Knife",
                        "Bottle",
                        "Human head",
                        "Man",
                        "Tool",
                        "Book",
                        "Candle",
                        "Spoon",
                        "Fork",
                        "Stool",
                        "Glasses",
                        "Human hand",
                        "Remote control",
                        "Woman"]
# create output directory
os.makedirs(args.outpath, exist_ok=True)
# output files and folders
labelsDir=args.outpath+"/"+"labels"
os.makedirs(labelsDir, exist_ok=True)
imagesDir=args.outpath+"/"+"images"
os.makedirs(imagesDir, exist_ok=True)
classestxt=labelsDir+"/"+"classes.txt"
dataDir=args.outpath+"/"+"images"+"/data"
os.makedirs(dataDir, exist_ok=True)

filesToGet=args.outpath+"/"+"filesToGet.txt"
# input files 
codeCategoryFile=args.categories 
imageIdsSubsetFile=args.imagesids
# processing variables
fieldnames = ['Code', 'Category']
CC = {}
CI = {}
CatRefCounter={}
maxImagesPerCategory = 1200 
# create categories dictionnary by filtering input categories file with our myCategories variable, then create classes.txt

with open (codeCategoryFile) as csvfile:
    CCreader = csv.DictReader(csvfile,delimiter=',',fieldnames=fieldnames)
    _ndx=0
    for row in CCreader:
        if (row['Category'] in myCategories):
            print (row['Category'] , row['Code'])
            CC[row['Code']]=row['Category']
            CI[row['Category']]=_ndx
            _ndx+=1
            CatRefCounter[row['Category']]=0 # simple category counter
            tclasseshandle = open(classestxt,"a")  # known overkill 
            tclasseshandle.write(row['Category']+"\r\n")
            tclasseshandle.close() # known overkill 
# copy classes.txt to images/data/predefined_classes.txt, required if we want to use labelImg for veirications
shutil.copyfile(classestxt,dataDir+"/predefined_classes.txt") 
# now we have our dictionnary of codes/category in CC and our index in CI
# find the images of these categories in the subset of imageids we have 
# image ids are extracted from a large download in https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
# for those image records where Code corresponds to ou CC[row[category]] 
# we will then 
# 1) get image name and X/Y values that we will transform to Yolov5 txt X/Y values. 
# 1.1) update the ../labels/classes.txt for the categories 
# 2) output Train/image name to file for future use with downloader.py (to retrieve the images files) 
# 3) for each image name selected, 
# 3.1)read subset of imageids and parse in _t 
# 3.2)compute box center and width, write them to our <imagefilename.txt> file in /label 
# 3.3) output "train/<filename>"to our "files to download file to be used by downloader.py (see reference in https://storage.googleapis.com/openimages/web/download.html) 
_n=0
spin='|\\-/'
with  open(imageIdsSubsetFile, "r") as subset: 
    for _l in subset:
        _t=_l.split(',',9) 
        _fn=_t[0]
        _label=_t[2]
        _category=CC.get(_label)
        _ndx = CI.get(_category)    
        #print ("-------") 
        print('\b'+spin[_n],end='') 
        #print(_n)
        _n=_n+1 if _n<=2 else 0
        #print (_ndx) 
        #print (_label)
        if (_category in myCategories):
            #print ("======") 
            #print ("%s %s "% (_category, _fn)) 
            if(int(CatRefCounter[_category] ) < maxImagesPerCategory ):
        
                _xmin=float(_t[4])
                _xmax=float(_t[5])
                _ymin=float(_t[6])
                _ymax=float(_t[7])
                _xcenter=(_xmin+_xmax)/2
                _ycenter=(_ymin+_ymax)/2
                _xwidth=(_xmax-_xmin)
                _ywidth=(_ymax-_ymin)
                #print (_label,_fn,_xcenter,_ycenter,_xwidth,_ywidth,_category,_ndx) 
                # write label file with image filename 
                tlabelhandle = open(labelsDir+"/"+_fn+".txt","a")  # known overkill 
                tlabelhandle.write("%s %s %s %s %s \r\n" % (str(_ndx),str(_xcenter),str(_ycenter),str(_xwidth),str(_ywidth)))
                #print("%s %s %s %s %s \r\n" % (str(_ndx),str(_xcenter),str(_ycenter),str(_xwidth),str(_ywidth)))
                tlabelhandle.close()
                filestogethandle = open(filesToGet,"a")  # known overkill 
                filestogethandle.write("%s%s%s\r\n" % ("train","/",str(_fn)))
                filestogethandle.close()
                CatRefCounter[_category] = CatRefCounter[_category] +1
            
if (os.path.isfile(filesToGet)):
    print("file %s has been created, you can now download the images files from OpenImages by using" % (filesToGet))
    print ("python downloader.py %s  --download_folder=./tempo?/images/" % (filesToGet))
    print (CI)
    print (CC)
    # show our stats
    print (CatRefCounter) 
