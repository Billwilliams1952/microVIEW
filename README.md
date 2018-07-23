# microVIEW
PiCamera user interface optimized for a touchscreen display. 

## Motivation

This work is a result of a collaboration between myself and Michael Axelsson, Professor, University of Gothenburg, Department of Biological and Environmental Sciences (http://www.bioenv.gu.se/personal/Axelsson_Michael/). Professor Axelsson has been investigating using inexpensive hardware and 3-D printed parts in order to capture video/photos from various types of microscopes. The final hardware/software solution would be primarily targeted to a teaching environment. After research, Professor Axelsson had selected the Raspberry PI (RPI) Model 3 as the computer system. Coupled with an RPI camera (V2 model) with flex cable, an SD card (for the OS), a power cable, a touchscreen display (Sundfounder 10” screen (https://www.sunfounder.com/10-1-touch-screen.html) with a 3D printed enclosure, and 3-D printed parts used to mount the RPI camera to each microscope; he had an inexpensive system that offered high resolution video and photo capture capabilities. What was needed was software. Professor Axelsson contacted me about using my PiCamera software (https://github.com/Billwilliams1952/PiCameraApp) to control the system. However, after further discussions, I decided to develop a user interface from scratch targeting a touchscreen display.

Professor Axelsson has documented the R&D effort - see http://microsurgery.se/ under the R/D tab.

## Design

This version of **microVIEW** is optimized for a 1280x800 touchscreen display running in fullscreen mode. Where possible, all controls are simple pushbuttons or sliders that are created specifically for **microVIEW**. There are no text fields in the option panels. The buttons and sliders have been enlarged to minimize 'touch' errors. In general during normal opeation, a keyboard should not be needed.

When **microVIEW** is first started, it creates a default **microVIEW.INI** file if one does not already exist. The default values may be edited to change many aspects of the program interface, file storage locations, and default camera programming values. Key **microVIEW.INI** data that the user may want to initially edit include:

#### Under [Preferences]

| INI Field    | Default Value | Notes |
| :--------- | :-------------------------- | :------------------------------------------------------ |
| defaultphotodir | /home/pi/Pictures | Default location for photos captured by user. May also be selected under **Preferences \| Files**. This is also true for the remaining photo and video directories. |
| defaultvideodir | /home/pi/Videos | Default location for videos captured by user |
| defaulttimelapsephotodir | /home/pi/Pictures | Default location for photos captured by timelapse |
| defaulttimelapsevideodir | /home/pi/Videos | Default location for videos captured by timelapse |
| defaultfilesdir | /home/pi/Documents | Default location for any text data created by **microVIEW** |
  
#### Under [Network]

| INI Field    | Default Value | Notes |
| :--------- | :-------------------------- | :------------------------------------------------------ |
| headinglevel1 | microVIEW | The first line (larger font) displayed on the streaming website. Both headingLevel1 and headingLevel2 are available for annotations too. |
| headinglevel2 | Streaming Live Video from Station 1 | The second line (smaller font) displayed on the streaming website. headingLevel2 may be used to identify the station (or computer system) that is streaming. Both headingLevel1 and headingLevel2 are available for annotations too. |

## User Interface

#### Main Screen
When started, **microVIEW** displays a fullscreen preview of the video. Along the bottom are four buttons:

![Image1](https://github.com/Billwilliams1952/microVIEW/blob/master/Assets/close.png?raw=true)		![Image2](https://github.com/Billwilliams1952/microVIEW/blob/master/Assets/options.png?raw=true)	![Image3](https://github.com/Billwilliams1952/microVIEW/blob/master/Assets/camera.png?raw=true)      ![Image4](https://github.com/Billwilliams1952/microVIEW/blob/master/Assets/video.png?raw=true)

* The first button closes **microVIEW**.
* The second button displays the options screen.
* The third button takes a picture and saves the photo under the directory specified by defaultphotodir.
* The fourth button starts video capture. While video capture is in progress, the video button will flash red. To stop the video capture, press the video capture button again. The video will be saved under the directory specified by defaultvideodir.

#### Options Screen

Basic camera programming functions are provided. In order to simplify the user interface, many of the advanced options for programming the camera are not provided. However, should the need arise, additional functionality can be readily added.

If running under Python 3.X, a simple HTTP web server is provided, allowing the user to stream the video over a local network. Both Ethernet and WiFi are supported. The controls are located under **Preferences \| Network**. Once the HTTP Server is turned ON, it cannot be turned OFF. To enable / disable video streaming, toggle the Video Stream ON or OFF.

Both Video and Photo timelapse capture are provided under **Timelapse \| Photos** and **Timelapse \| Videos**. For photos, the rate of photo capture (e.g. every 10 seconds), and either the stop count (e.g. stop after 10 pictures) or delta time (e.g. stop after 2 hours) may be specified. Photo timelapse may occur even during a video capture or video timelapse. For videos, the rate of video capture (e.g. capture every 30 seconds), the video length (e.g. 10 seconds) and either the stop count (e.g. stop after 10 videos) or delta time (e.g. stop after 2 hours) may be specified. During Video Timelapse, the Video capture button on the main screen is disabled.

Multiple languages are supported via the **microVIEW.language** file. This file contains many (not all - yet) of the labels, button/control text and messages used by **microVIEW** interface, ordered by [Language] sections. Currently there are entries for English, Svenska (Swedish), Deutsche (German), Italiano (Italian), Español (Spanish), Nederlands (Dutch), and Français (French). Please note that many translations may not be accurate usage (since I was just using Google Translate). Also note that not all text has translations (yet). Please feel free to update the file and send me the updates as they are completed.  If the **microVIEW.language** file is missing at startup, a default **microVIEW.language** file is created with just English translations. When editing the **microVIEW.language** file, the user may insert a newline character (\n) to force a line break in the text. This is useful when trying to fit text within a control or label. For example:

```
    dynamicrangecompression = Dynamisk\nOmfångskompression:
```

## Version History

Refer to **Preferences \| About \| About** for the version number of **microVIEW**.

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

**microVIEW** has been developed using Python ver 2.7.13 and Python ver 3.5.3. In addition, it uses the following additonal Python libraries. Refer to **Preferences \| About \| About** for the exact versions used.

| Library    | Usage                                               |
| :--------- | :-------------------------------------------------- |
| picamera   | The python interface to the PiCamera hardware. See https://picamera.readthedocs.io/en/release-1.13/install.html |
| PIL / Pillow | The Pillow fork of the Python Image Library. One issue is with PIL ImageTk under Python 3.x. It was not installed on my RPI. If you have similar PIL Import Errors use:  **sudo apt-get install python3-pil.imagetk**. |
| netifaces | Library to help discover IP addresses. Install using **sudo pip3 install netifaces** for Python3 or **sudo pip install netifaces** for Python2 |

## Installation

Download the zip file and extract to a directory of your choosing. To run, open a terminal, change to the directory containing the source files, and enter **sudo python microVIEW.py** or **sudo python3 microVIEW.py**.  Note:, if you run under a Python version lower than 3.0, then the Webserver interface will not be available.

### Installation on a Fresh Image

On a fresh install of Raspbian

(1) Update software sources. Open the terminal and enter:

	sudo apt-get update

(2) Once the update is complete, update everything to the latest version by entering:

	sudo apt-get upgrade

(3) Once the software is upgraded, install ImageTk for python2 by entering:

	sudo apt-get install python-imaging-tk

(4) Then install ImageTk for python3 by entering:

	sudo apt-get install python3-pil.imagetk

(5) Finally, install netifaces by entering:

	sudo pip3 install netifaces		for Python3 or
	sudo pip install netifaces		for Python2

(6) If there is a black border of unused pixels around the screen display, you’ll need to disable overscan, otherwise the button overlays won’t line up with the actual buttons underneath the preview. Edit the /boot/config.txt file by opening up a terminal and entering the following command:

	sudo nano /boot/config.txt

(6.1) Find and uncomment the disable_overscan=1 line by deleting the ‘#’ character:

	disable_overscan=1

(6.2) Save then exit by entering Ctrl+X and then pressing Y to save the file.

(7) Make sure you enable the camera. On the main menu, select Preferences, then ‘Raspberry Pi Configuration’. Once the configuration screen is up, select Interfaces, and Enable the Camera.

(8) Reboot your RPI. The black border should be gone, the Camera should work. After changing to the directory containing **microVIEW**, it should start up using the command:

	sudo python3 microVIEW.py or sudo python microVIEW.py

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
