# microVIEW
PiCamera user interface optimized for a touchscreen display. 

## Motivation

This work is a result of a collaboration between myself and Michael Axelsson, Professor, University of Gothenburg, Department of Biological and Environmental Sciences. Professor Axelsson has been investigating using inexpensive hardware and 3-D printed parts in order to capture video/photos from various types of microscopes. The final hardware/software solution would be primarily targeted to a teaching environment. After research, Professor Axelsson had selected the Raspberry PI Model 3 as the basic computer system. Coupled with the RPI camera; an SD card; a power cable; a touchscreen tablet; and 3-D printed parts used to mount the RPI camera to the microscope; he had an inexpensive system that offered high resolution video and photo capture capabilities. What was needed was software. Professor Axelsson contacted me about using my PiCamera software <INSERT LINK> to control the system. However, after further discussions, I decided to develop a user interface from scratch targeting a 1280x800 touchscreen display.

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
