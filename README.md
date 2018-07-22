# microVIEW
PiCamera user interface optimized for a touchscreen display. 

## Motivation

This work is a result of a collaboration between myself and Michael Axelsson, Professor, University of Gothenburg, Department of Biological and Environmental Sciences (http://www.bioenv.gu.se/personal/Axelsson_Michael/). Professor Axelsson has been investigating using inexpensive hardware and 3-D printed parts in order to capture video/photos from various types of microscopes. The final hardware/software solution would be primarily targeted to a teaching environment. After research, Professor Axelsson had selected the Raspberry PI (RPI) Model 3 as the computer system. Coupled with the RPI camera; an SD card; a power cable; a touchscreen display; and 3-D printed parts used to mount the RPI camera to each microscope; he had an inexpensive system that offered high resolution video and photo capture capabilities. What was needed was software. Professor Axelsson contacted me about using my PiCamera software (https://github.com/Billwilliams1952/PiCameraApp) to control the system. However, after further discussions, I decided to develop a user interface from scratch targeting a touchscreen display.

## Design

This version of **microVIEW** is optimized for a 1280x800 touchscreen display. Where possible, all controls are simple pushbuttons or sliders that are created specifically for **microVIEW**. There are no text fields in the option panels. The buttons and sliders have been enlarged to minimize 'touch' errors. In general during normal opeation, a keyboard should not be needed.

When **microVIEW** is first started, it creates a default **microVIEW.INI** file if one does not already exist. The default values may be edited to change many aspects of the program interface, file storage locations, and default camera programming values. Key **microVIEW.INI** data that the user may want to initially edit include:

**Under [Preferences]**

| INI Field    | Default Value | Notes |
| :--------- | :-------------------------- | :------------------------------------------------------ |
| defaultphotodir | /home/pi/Pictures | Default location for photos captured by user |
| defaultvideodir | /home/pi/Videos | Default location for videos captured by user |
| defaultfilesdir | /home/pi/Documents | Default location for any text data created by **microVIEW** |
| defaulttimelapsephotodir | /home/pi/Pictures | Default location for photos captured by timelapse |
| defaulttimelapsevideodir | /home/pi/Videos | Default location for videos captured by timelapse |
  
**Under [Network]**

| INI Field    | Default Value | Notes |
| :--------- | :-------------------------- | :------------------------------------------------------ |
| headinglevel1 | microVIEW | The first line (larger font) displayed on the streaming website. Both headingLevel1 and headingLevel2 are available for annotations too. |
| headinglevel2 | Streaming Live Video from Station 1 | The second line (smaller font) displayed on the streaming website. headingLevel2 may be used to identify the station (or computer system) that is streaming. Both headingLevel1 and headingLevel2 are available for annotations too. |

Basic camera programming functions are provided. In order to simplify the user interface, many of the advanced options for programming the camera are not provided. However, should the need arise, additional functionality can be readily added.

If running under Python 3.X, a simple web server is provided, allowing the user to stream the video over a local network. Both Ethernet and WiFi are supported.

Both Video and Photo timelapse capture are provided.


## Installation

Download the zip file and extract to a directory of your choosing. To run, open a terminal, change to the directory containing the source files, and enter **sudo python microVIEW.py** or **sudo python3 microVIEW.py**.  Note:, if you run under a Python version lower than 3.0, then the Webserver interface will not be available.

## Version History

| Version    | Notes                               |
| :--------- | :----------------------------------------------------- |
| 0.1 | <ul><li>Initial release. Tested under Python 2.7X and 3.5.3</li><li>Tested using the RPI V2 camera module </li></ul> |

## Known Issues

| Issue      | Description / Workaround                               |
| :--------- | :----------------------------------------------------- |
| Language Support | The language support is not complete for all controls and text messages throughout **microVIEW**. Also, I have not verified the accuracy/suitability of the translations. I have just used Google translate. I really need the translations reviewed by native speakers. |

## TODO List (future enhancements)

| TODO       | Description                               |
| :--------- | :----------------------------------------------------- |
| Language Support | Continue to update translations as reviews are completed and suggestions are offered.|
| Screen Size | **microVIEW** has been designed assuming a 1280 x 800 touch screen tablet. Provide support for other touchscreen sizes. |
| Web Server | **microVIEW** uses a very simple web server to stream the video. Only Python 3.x is supported. Provide support for Python 2.x. Provide the ability to start / stop the web server. |

## API Reference

**microVIEW** has been developed using Python ver 2.7.13 and Python ver 3.5.3. In addition, it uses the following additonal Python libraries. See the **microVIEW** About tab for exact versions used.

| Library    | Usage                                               |
| :--------- | :-------------------------------------------------- |
| picamera   | The python interface to the PiCamera hardware. See https://picamera.readthedocs.io/en/release-1.13/install.html |
| PIL / Pillow | The Pillow fork of the Python Image Library. One issue is with PIL ImageTk under Python 3.x. It was not installed on my RPI. If you have similar PIL Import Errors use:  **sudo apt-get install python3-pil.imagetk**. |

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
