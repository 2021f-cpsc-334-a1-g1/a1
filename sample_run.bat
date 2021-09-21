@echo off

echo Running process-video.py...
.\bin\python\WPy64-3950\python-3.9.5.amd64\python.exe .\process_video.py .\reports\leeds\display-config.json .\demo_content\johnny-bubble.mp4 .\out.mp4 -v -r 270
echo Running process-video.py...Complete
pause

echo Viewing output...
.\bin\mpv\mpv.exe .\out.mp4 --no-border
echo Viewing output...Complete
pause
