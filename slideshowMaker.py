# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:10:01 2020

Slideshow movie maker with audio

Creates a batch files for running with ffmpg

Limit with length of video - too many arguments and ffmpeg will not read it

@author: Low
"""

#pip3 install mutagen


import os
import random
from mutagen.mp3 import MP3

import cv2
import numpy as np
from matplotlib import pyplot as plt




dir1 = "pictures/"
#dir1 = "D:/Data/lm.com/audioCollection/audio-mien-lessons/"
counter = 0
totalDuration = 0
mp3File = []
mp3Audio = []
for i in os.listdir(dir1):
    if ".mp3" in i:
        fileName = dir1 + i
        mp3File.append(MP3(fileName))
        #print(fileName)
        length = mp3File[counter].info.length
        mp3Audio.append(length)
        totalDuration = totalDuration + length
        #print(length)
        counter += 1

print(f'Total duration: {totalDuration:.2f} seconds')

#VariableVideoDuration = [14,12.85,12.21,10.23,13.1,9.88,12.25,8.86,11.99,9.91,11.62,8,11.97,9.33,10.54,7.81,10.12,8.69,9.37,9.72,10.57,8.57,9.63,8.91,9.95,8.88,10.96,8.73,11.43,9.07,10.88,8.12,11.03,8.04,9.91,8.16,10.18,8.54,11.83,9.66,8.6,7.66,10.27,8.69,9.49,8.45,9.15,9.27,7.41,9.63,10.52,9.33,10.12,8.74,7.15,7.96,9.83,8.72,7.16,8.56,7.98,8.89,9.11,8.45,8.84,11.94,9.63,10.57,9.79,8.51,8.75,9.25,9.73,10.37,9.43,8.61,10.88,8.77,9.65,9.49,11.23,8.85,9.35,10.16,9.13,8.92,9.7,10.36,9.05,11.59,9.38,8.36,9.41,9.94,9.75,8.48,9.16,10.5,10.28,10.29,9.4,9.84,11.02,9.39,8.07,9.98,9.7,11.54,9.13,8.84,9.95,11.88,7.17,8.68,9.28,10.57,7.96,9.51,10.09,9.32,9.86,9.47,10.62,8.07,9.69,7.8,10.16,10.3,8.1,7.91,8.63,8.59,8.92,7.91,10.07,8.29,10.07,8.98,9.75,8.26,9.6,8.64,9.99,9.5,10.05,6.71,9.3,8.35,11.12,9.23,10.7,10.52,9,5.74,7.43,8.41,8.57,8.81,7.35,9.46,9.52,8.12,9.54,9.09,6.43,8.18,8.72,]

VariableVideoDuration = [14,12.85,12.21,10.23,13.1,9.88,12.25,8.86,11.99,9.91,11.62,8,11.97,9.33,10.54,7.81,10.12,8.69,9.37,9.72,10.57]



pictureDir = "pictures"
realLength = 0 ## length of actual list size instead of default 300
durationPerImage = 6
#need to program this
#audioMinutes = 4
#audioSeconds = 54
#audioDuration = (audioMinutes * 60) + audioSeconds + durationPerImage #seconds (2 minutes 5 seconds)
audioDuration = totalDuration + durationPerImage
videoDuration = 0
randomizeImages = True
verticalVideo = True
paddingColor = "004D33"
crossfade = False
variableDuration = False

print("actual length = ",sum(VariableVideoDuration))
print("added artificial length = ",audioDuration)

#Crossfade will use the default dimension of the images - it will not rescale
#if want vertical video with crossfade, all the images will have to be vertical

allFiles = os.listdir(pictureDir)
if(len(allFiles) == 0):
    print("Directory has no files")
    emptyDirectory = True
else:
    print("Directory is not empty")
    emptyDirectory = False

#print(images)


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
    
    if (randomizeImages == True):
        random.shuffle(filteredFiles)

    return filteredFiles

def keepAudioFilesOnly(files):
    filteredFiles = [0] * 30
    j = 0
    for i in range(len(files)):
        #print(files)
        if files[i].find("mp3") > 1:
            filteredFiles[j] = files[i]
            j+=1
    

    return filteredFiles

#print("imageFile length == ",len(imageFiles))

if (emptyDirectory == False):
    imageFiles = keepImageFilesOnly(allFiles)
    audioFiles = keepAudioFilesOnly(allFiles)
    ffmpegCommand = "C:\\ffmpeg\\ffmpeg.exe "
    while videoDuration < audioDuration:
        for i in range(len(imageFiles)):
            if imageFiles[i] != 0:
                print(imageFiles[i])
                if variableDuration == True:
                    durationPerImage = VariableVideoDuration[i]+2
                ffmpegCommand = ffmpegCommand + "-loop 1 -t " + str(durationPerImage) + " -i \"" + pictureDir + "\\" + imageFiles[i] + "\" "
                realLength += 1
                videoDuration += durationPerImage
                if videoDuration > audioDuration:
                    break
    
    
    print(realLength)

    # Testing image fill with blur
    img = pictureDir + "\\" + imageFiles[0]
    print(img)
    imgToBlur = cv2.imread(img)
    imgBlur = cv2.blur(imgToBlur,(10,10))
    cv2.imshow("Blurred Image",imgBlur)

    
    ffmpegCommand = ffmpegCommand + "-filter_complex \""
    
    #for i in range(len(imageFiles)):
    for i in range(0,realLength-1):
        #if imageFiles[i] != 0:
        if verticalVideo == False:
            if crossfade == False:
                ffmpegCommand = ffmpegCommand + "[" + str(i) + ":v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:#" + paddingColor + "@1,format=rgb24,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st=" + str(durationPerImage) + ":d=1[v" + str(i) + "]; "
            else:
                ffmpegCommand = ffmpegCommand + "[" + str(i+1) + "]format=rgb24,fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+" + str((i+1)*(durationPerImage-1)) + "/TB[f" + str(i) + "]; "
        if verticalVideo == True:
            if crossfade == False:
                ffmpegCommand = ffmpegCommand + "[" + str(i) + ":v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:#" + paddingColor + "@1,format=rgb24,setsar=1,fade=t=in:st=0:d=1,fade=t=out:st=" + str(durationPerImage) + ":d=1[v" + str(i) + "]; "
            else:
                if variableDuration == True:
                    durationPerImage = VariableVideoDuration[i]
                ffmpegCommand = ffmpegCommand + "[" + str(i+1) + "]format=rgb24,fade=d=1:t=in:alpha=1,setpts=PTS-STARTPTS+" + str((i+1)*(durationPerImage-1)) + "/TB[f" + str(i) + "]; "



    #for i in range(len(imageFiles)):
    if crossfade == True:
        rl = 2
    else:
        rl = 1
        
    for i in range(0,realLength-rl): #Cross fade is realLenth-2 while fade to black as a realLength-1 (1 and 2 represented by rl)
        if crossfade == False:
            ffmpegCommand = ffmpegCommand + "[v" + str(i) + "]"
        else:
            if (i==0):
                ffmpegCommand = ffmpegCommand + "[" + str(i) + "][f" + str(i) + "]overlay[bg" + str(i+1) + "];"
            else:
                ffmpegCommand = ffmpegCommand + "[bg" + str(i) + "][f" + str(i) + "]overlay[bg" + str(i+1) + "];"

    if crossfade == True:
        ffmpegCommand = ffmpegCommand + "[bg" + str(realLength-2) + "][f" + str(realLength-2) + "]overlay,format=yuv420p[v]\" -map \"[v]\" -movflags +faststart " + pictureDir + "\out.mp4"
    else:
        ffmpegCommand = ffmpegCommand + "concat=n=" + str(realLength-1) + ":v=1:a=0,format=yuv420p[v]\" -map \"[v]\" \"" + pictureDir + "\\" + "out.mp4\""
        
    #outputBATfile = pictureDir + "\\" + "slideshow.bat"
    outputBATfile = "slideshow.bat"
    
    outputFile = open(outputBATfile,"w")
    outputFile.write(ffmpegCommand)
    outputFile.close() 
    

"""
    # includes command for encoding video with audio
    ffmpegCommand = ffmpegCommand + "\n\n"
    ffmpegCommand = ffmpegCommand + "C:\\ffmpeg\\ffmpeg.exe -i \"" + pictureDir + "\\" + "out.mp4\" -i \"" + pictureDir + "\\" + audioFiles[0] + "\" \"" + pictureDir + "\\" + "slideshow_final.mp4\""
    ffmpegCommand = ffmpegCommand + "\n\n" + "del \"" + pictureDir + "\\" + "out.mp4\""

"""