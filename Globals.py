#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Globals.py
#  Copyright 2018 Bill Williams <github.com/Billwilliams1952>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
'''

class Globals:
	# [Preferences]
	defaultphotodir = '/media/pi/USB_BACKUP/Pictures'
	defaultvideodir = '/media/pi/USB_BACKUP/Videos'
	defaulttimelapsephotodir = '/media/pi/USB_BACKUP/Pictures'
	defaulttimelapsevideodir = '/media/pi/USB_BACKUP/Videos'
	defaultfilesdir = '/home/pi/Documents'
	defaultphotoname = 'Image_'
	defaultphotoformat = 'jpg'
	defaultvideoname = 'Video_'
	defaultvideoformat = 'h264'
	# In the INI file replace % with @, then replace back when reading
	defaulttimestampformat = '%m%d%y-%H%M%S'
	phototimestamp = False
	videotimestamp = False
	defaultLanguage = 'English'

	# [Camera]
	cameraPresent = True			# Not sure if this will be used
	defaultBrightness = 50
	defaultContrast = 0
	defaultSaturation = 0
	defaultSharpness = 0
	defaultResolution = 18		# 1920 x 1080 (HD)
	# Newly added
	useVideoPort = False
	imageDenoise = True
	videoDenoise = True
	videoStabilization = True
	exposureCompensation = 0	# -25 to 25
	meteringMode = 0				# 'average' = 0
	drcStrength = 0				#

	# [Video]
	defaultVideoTimeout = 30	# a value of 0 is NO timeout
	defaultFrameRate = 30

	# [Annotation]
	defaultAnnotateTextsize = 40
	timestampEnabled = False
	framerateEnabled = False
	transparantBackgroundEnabled = True
	annotateBackgroundColor = 50
	annotateForegroundColor = 100

	# [Preview]
	defaultAlpha = 240

	# [Network]
	enableHTTPServer = False			# ALWAYS START AS FALSE
	enableVideoStreaming = False
	headingLevel1 = 'microVIEW Test Header 1'
	headingLevel2 = 'Streaming live video from station 1'

	# [Timelapse]
	defaultTakePictureCount = 5
	defaultTakePictureCountType = 0	# 0=seconds, 1=minutes, 2=hours
	defaultStopPictureCount = 5
	defaultStopPictureCountType = 0	# 0=pictures, 1=seconds, 2=minutes, 3=hours, 4=days
	defaultTakeVideoCount = 5
	defaultTakeVideoCountType = 0		# 0=seconds, 1=minutes, 2=hours
	defaultVideoLength = 5
	defaultVideoLengthType = 0			# 0=seconds, 1=minutes, 2=hours
	defaultStopVideoCount = 5
	defaultStopVideoCountType = 0		# 0=videos, 1=seconds, 2=minutes, 3=hours, 4=days

	# [Colors]
	defaultBackgroundColor = 'black'
	defaultForegroundColor = 'white'
	buttonbackcolor = 'blue'
	buttontextcolor = 'white'
	buttonpressedcolor = '#9899FF'
	buttonpressedtextcolor = 'black'
	sliderbackcolor = 'blue'
	slidercolor = '#9899FF'
	slidertextcolor = 'white'

	# [Fonts]
	defaultFont = 'Arial 14 bold'
	labelFont = 'Arial 12 bold'

	# [Layout]
	defaultButtonHeight = 50
	defaultButtonPadX = 10
	defaultButtonPadY	= 10
	defaultSliderHeight = 50
	defaultSliderPadX = 10
	defaultSliderPadY	= 10

	# [JPEG]

	# [H264]


