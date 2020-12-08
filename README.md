# slideshow-movie-maker

Python writes FFmpeg commands for creating a slideshow movie maker. Python pulls images and audios from picture directory.

Audio (mp3) duration pulled using Mutagen.


imageWithBlurredBG.py

Resizes an image to a desired video dimension and orientation keeping the original aspect ratio of image with gaps filled with blur. This is for creating slideshows with a crossfade which requires the same image dimensions.

The slideshows with a black transition has a automatic padding in slideshow.py.

Crossfading timing is still off.
