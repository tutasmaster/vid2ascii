# Video To Ascii

 This is a project that turns any huge sequence of pictures into a watchable video in the form of an HTML file.

## Features

  - Batch conversion of images into ASCII art based on brightness;
  - Automatically adding a player for that sequence at a designated framerate;
  - Pause/Play and video controls;
  - Audio player for said video.

## Requirements

- [ffmpeg](https://www.ffmpeg.org/)
- [Python 3](https://www.python.org/download/releases/3.0/)
- [PILLOW for Python 3](https://pillow.readthedocs.io/en/5.1.x/)

## Using
After getting all the requirements up and running you need to execute ffmpeg in order to take out the frames out of the video. 
The frames should be in .jpg format and they should have the format VID%1d.jpg. 
The file type is just for convinience and can be easily changed inside the python script.

    ffmpeg  -i vid.mp4 -ss 00:00:00 -t 00:00:10 -r 10 VID%1d.jpg

That would extract all the frames of a file named "vid.mp4", starting from the point "00:00:00", ending 10 seconds later at a rate of 10 frames per second.

Now we extract the audio to an mp3 file with the name "output.mp3" using:

    ffmpeg -i vid.mp4 -ss 00:00:00 -t 00:00:10 -codec:a libmp3lame -qscale:a 2 output.mp3.

This would extract audio on the same timeframe to the correct file.

Now that you have a folder with all you need it's time to run the script.
The script will generate the HTML required.
To run the script you execute it like so:

    py vidToASCII.py videoname.mp4 <fps> <seconds> <outputName> <font-size in pixels> <scale>
    
- videoname is the "vid.mp4" file;
- fps is the framerate you set on ffmpeg when extracting the frames;
- seconds is the -t parameter in ffmpeg when extracting the frames;
- outputName should be called "VID" as in "VID%1d.jpg"
- font-size is the size of each character on the html page
- scale is a way so that you don't have to downsize your videos in order to run nice, a 7 scale is a video scaled by 1/7

The rest is handled by the script like the video playback and the file will be generated as "outputname.html".