cd /d D:\Users\roman\potrace-1.16.win64
potrace.exe -i image.bmp -b svg -o image.svg
GCodeConverter.exe image.svg
java -cp UniversalGcodeSender.jar com.willwinder.ugs.cli.TerminalClient --controller GRBL --port COM3 --baud 115200 --print-progressbar --file image.tap

