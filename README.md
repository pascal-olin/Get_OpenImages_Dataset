# Get_OpenImages_Dataset
---
### Some help for those who want to download a partial copy of the huge openimages Dataset V6 (https://storage.googleapis.com/openimages/web/index.html)
#### I am interested only in a small subset of the openimages dataset for my yolov5 robotic experiment.
---
This repo is simply publishing the simple tools I am using to get the annotated image rather than doing a lot of labeling myself. 

This said, the directory structure I have used for output is compatible with labelImg (https://github.com/tzutalin/labelImg) so that the openimages downloaded images and annotation can be verified (at least partially) before getting in some heavy and expensive CNN training computation. 

## usage :
edit getOpenImagesSubsetForYolov5.py  variables : 
  myCategories (list of categories you are interested with, must be subset (case sensitive) of https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv 
  maxImagesPerCategory (number of files of EACH category you want to get) 
  
then : 

download a copy of BOXed images names at : https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv 
keep only a subset of this file (for example the first million record : head -n 1000000 <downloaded big file name> > <new smaller file name> 
it will be our --imageids parameter file 
then download a copy of class names at  : https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
it will be our --categories parameter file 

 run "python getOpenImagesSubsetForYolov5.py --categories <name of the downloaded categories file> --imageids <name of the subset of images files names obtained above> --oputpath <path where you want to store the resulting file> "
  
This will create a file outpath+"/"+"filesToGet.txt" 
then using the downloader.py facility, you can download the files python downloader.py outpath+"/"+"filesToGet.txt --download_folder=$DOWNLOAD_FOLDER --num_processes=5

Contact me if these instructions seem messy, happy to help !
  
  PO
  
  
