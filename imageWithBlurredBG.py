# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:54:19 2020

Create image with blurred background

@author: Low
"""
import os
import cv2
 

def keepImageFilesOnly(files):
    #filteredFiles = [0] * 300
    filteredFiles = []
    j = 0
    for i in range(len(files)):
        #print(files)
        if files[i].find("jpg") > 1 or files[i].find("png") > 1:
            #filteredFiles[j] = files[i]
            filteredFiles.append(files[i])
            j+=1

    return filteredFiles

pictureDir = "pictures"

allFiles = os.listdir(pictureDir)
if(len(allFiles) == 0):
    print("Directory has no files")
    emptyDirectory = True
else:
    print("Directory is not empty")
    emptyDirectory = False

imageFiles = keepImageFilesOnly(allFiles)

for i in imageFiles:
    print(i)



#check for a portrait or landscape picture and resize for 720x1280

#360p
#minLength = 360
#maxLength = 480
#720p
minLength = 720
maxLength = 1280
#1080p
#minLength = 1080
#maxLength = 1920
videoOrientation = "portrait"
#videoOrientation = "landscape"


for pic in imageFiles:
    landscapeBlurTop = False
    portraitBlurSide = False
    fullpathFilename = pictureDir + "\\" + pic
    img = cv2.imread(fullpathFilename, cv2.IMREAD_UNCHANGED)
    print('Original Dimensions : ',img.shape)
    # resizing to fit screen
    if videoOrientation == "portrait":
        imgOrientation = "portrait"
        print("image is in portrait")
        height = int(img.shape[0]*(1+((minLength-img.shape[1])/(img.shape[1]))))
        width = minLength
        print(height,'x',width)
        dim = (width, height)
    if videoOrientation == "landscape":
        imgOrientation = "landscape"
        print("Image is in landscape")
        height = minLength
        width = int(img.shape[1]*(1+((minLength-img.shape[0])/(img.shape[0]))))
        print(height,'x',width)
        dim = (width, height)
    if videoOrientation == "landscape" and width > maxLength:
        landscapeBlurTop = True
        print("landscapeblurtop=True")
        print("Image is in landscape")
        height = int(img.shape[0]*(abs(maxLength-img.shape[1])/img.shape[1]))
        width = maxLength
        print(height,'x',width)
        dim = (width, height)
    if videoOrientation == "portrait" and height > maxLength:
        portraitBlurSide = True
        print("portraitBlurSide=True")
        print("Image is in portrait")
        height = maxLength
        width = int(img.shape[1]*(abs(maxLength-img.shape[0])/img.shape[0]))
        print(height,'x',width)
        dim = (width, height)
      
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
     
    if videoOrientation == "portrait":
        blurDim = (minLength,maxLength)
    if videoOrientation == "landscape":
        blurDim = (maxLength, minLength)
    
    imgBlur = cv2.GaussianBlur(img,(9,9),cv2.BORDER_DEFAULT)
    resizedBlur = cv2.resize(imgBlur, blurDim, interpolation = cv2.INTER_AREA)
    
    print('Resized Dimensions : ',resized.shape)
    
    # Blurs the top
    if imgOrientation == "portrait" and portraitBlurSide == False:
        centerLeft = int((maxLength-height)/2)
        for i in range(height):
            for j in range(int(width)):
                resizedBlur[i+centerLeft][j] = resized[i][j]
    # Blurs the side
    if imgOrientation == "landscape" and landscapeBlurTop == False:
        centerLeft = int((maxLength-width)/2)
        for i in range(height):
            for j in range(width):
                resizedBlur[i][j+centerLeft] = resized[i][j]
    
    # Blurs the top and bottom on landscape orientation
    if landscapeBlurTop:
        print('Blurs the top and bottom on landscape orientation')
        centerLeft = int((minLength-height)/2)
        for i in range(height):
            for j in range(width):
                resizedBlur[i+centerLeft][j] = resized[i][j]
    
    # Blurs the side on portrait orientation
    if portraitBlurSide == True:
        print('Blurs the side on portrait orientation')
        centerLeft = int(abs(minLength-width)/2)
        for i in range(height):
            for j in range(width):
                resizedBlur[i][j+centerLeft] = resized[i][j]

    filename = 'output\\' + pic
    print(filename)
    cv2.imwrite(filename, resizedBlur)
    #cv2.imshow("Resized image", resized)
    #cv2.imshow("Blurred image", resizedBlur)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()