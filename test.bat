@echo off
set /p video_name= Please enter video name:
set /p url= Please enter url:
mkdir %video_name%
cd %video_name%
mkdir images
mkdir audio
cd ..
python scraper.py %video_name% %url%
cd %video_name%
ffmpeg -f concat -i input.txt -vsync vfr -pix_fmt yuv420p output.mp4
ffmpeg -f concat -i audio.txt -c copy output.wav
ffmpeg -i output.mp4 -i output.wav -c:v copy -c:a aac -strict experimental final.mp4
