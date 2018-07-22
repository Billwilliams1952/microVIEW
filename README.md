# microVIEW
PiCamera user interface optimized for touchscreen. 

## Motivation

This work is a result of a collaboration between myself and Professor Michael Axelsson of 

Note: I am an old (old, old, old, ..., so very old) Windows programmer going back to the days of Windows 2.1 (Petzold). Both the Python language as well as Linux on the Raspberry Pi are new to me, so please forgive unintentional (or blatant) misuses of the API or Python coding 'standards'.


## Installation

Download the zip file and extract to a directory of your choosing. To run, open a terminal, change to the directory containing the source files, and enter **sudo python microVIEW.py** or **sudo python3 microVIEW.py**.  Note:, if you run under a Python version lower than 3.0, then the Webserver interface will not be available.

## Version History

| Version    | Notes                               |
| :--------- | :----------------------------------------------------- |
| 0.1 | <ul><li>Initial release. Tested under Python 2.7X and 3.5.3</li><li>Tested using the RPI V2 camera module </li></ul> |
| | |

## Known Issues

| Issue      | Description / Workaround                               |
| :--------- | :----------------------------------------------------- |
| Language Support | The language support is not complete for all controls and text messages throughout **microVIEW**. Also, I have not verified the accuracy/suitability of the translations. I have just used Google translate. I really need the translations reviewed by native speakers. |
| | |

## TODO List (future enhancements)

| TODO       | Description                               |
| :--------- | :----------------------------------------------------- |
| Language Support | Continue to update translations as reviews are completed and suggestions are offered.|
| Screen Size | **microVIEW** has been designed assuming a 1280 x 800 touch screen tablet. Provide support for other touchscreen sizes. |
| Web Server | **microVIEW** uses a very simple web server to stream the video. Only Python 3.x is supported. Provide support for Python 2.x. Provide the ability to start / stop the web server. |
| | |

## API Reference

**microVIEW** has been developed using Python ver 2.7.13 and Python ver 3.5.3. In addition, it uses the following additonal Python libraries. See the PiCameraApp About dialog for exact versions used.

| Library    | Usage                                               |
| :--------- | :-------------------------------------------------- |
| picamera   | The python interface to the PiCamera hardware. See https://picamera.readthedocs.io/en/release-1.13/install.html |
| PIL / Pillow | The Pillow fork of the Python Image Library. One issue is with PIL ImageTk under Python 3.x. It was not installed on my RPI. If you have similar PIL Import Errors use:  **sudo apt-get install python3-pil.imagetk**. |
|     |    | 

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
