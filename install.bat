@echo off

mkdir .\bin

echo Downloading 7za...
mkdir .\bin\7za
curl.exe -o .\bin\7za\7za920.zip https://newcontinuum.dl.sourceforge.net/project/sevenzip/7-Zip/9.20/7za920.zip
echo Extracting 7a...
tar -xf .\bin\7za\7za920.zip -C .\bin\7za
del .\bin\7za\7za920.zip

echo Downloading 7zip...
mkdir .\bin\7zip
curl.exe -o .\bin\7zip\7z2103-x64.exe https://www.7-zip.org/a/7z2103-x64.exe
echo Extracting 7zip...
.\bin\7za\7za.exe e .\bin\7zip\7z2103-x64.exe -o".\bin\7zip" -y

echo Downloading python...
mkdir .\bin\python
curl.exe -o .\bin\python\Winpython64-3.9.5.0dot.exe https://phoenixnap.dl.sourceforge.net/project/winpython/WinPython_3.9/3.9.5.0/Winpython64-3.9.5.0dot.exe
echo Extracting python...
.\bin\python\Winpython64-3.9.5.0dot.exe -o".\bin\python" -y
del .\bin\python\Winpython64-3.9.5.0dot.exe

echo Downloading ffmpeg...
mkdir .\bin\ffmpeg
curl.exe -o .\bin\ffmpeg\ffmpeg-4.4-full_build.7z https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-4.4-full_build.7z
echo Extracting ffmpeg...
.\bin\7zip\7z.exe e .\bin\ffmpeg\ffmpeg-4.4-full_build.7z -o".\bin\ffmpeg" -y
del .\bin\ffmpeg\ffmpeg-4.4-full_build.7z

echo Downloading mpv...
mkdir .\bin\mpv
curl.exe -o .\bin\mpv\mpv-x86_64-20210919-git-560e6c8.7z https://phoenixnap.dl.sourceforge.net/project/mpv-player-windows/64bit/mpv-x86_64-20210919-git-560e6c8.7z
echo Extracting mpv...
.\bin\7zip\7z.exe e .\bin\mpv\mpv-x86_64-20210919-git-560e6c8.7z -o".\bin\mpv" -y
del .\bin\mpv\mpv-x86_64-20210919-git-560e6c8.7z

echo Installing dependencies..
.\bin\python\WPy64-3950\python-3.9.5.amd64\python.exe -m pip install -r .\requirements.txt

echo Completed.
pause
