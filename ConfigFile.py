#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ConfigFile.py
#  Copyright 2018 Bill Williams <github.com/Billwilliams1952>

Read/Write the PiCamera INI file

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''
import os
import subprocess
import sys

Python2 = True

# Big changes between the two
if sys.version_info[0] == 3:
	Python2 = False
	import configparser as ConfigParser		# Python 3.x
else:
	import ConfigParser as ConfigParser		# Python 2.X

from Globals import *

def ReadConfigValue ( config, section, item, typeVal ):
	if typeVal is int:
		if Python2:	val = config.getint(section,item)
		else:			val = config[section].getint(item)
	elif typeVal is float:
		if Python2:	val = config.getfloat(section,item)
		else:			val = config[section].getfloat(item)
	elif typeVal is bool:
		if Python2:	val = config.getboolean(section,item)
		else:			val = config[section].getboolean(item)
	else:	# string
		if Python2:	val = config.get(section,item)
		else:			val = config[section][item]
		# Now check if the string is of the form 'file=path\filename'
		# if so, then read the given file for the string text.
		# Replace newlines with spaces and replace the '\n' string
		# with a newline. Return the string.
	return val

def UpdateConfigValue ( config, section, item, val ):
	try:
		if type(val) is not str:	val = str(val)
		if Python2:	config.set(section,item,val)
		else:			config[section][item] = val
	except: pass

def LoadPreferences ( filename ):
	config = ConfigParser.SafeConfigParser()
	config.read(filename)

	if not config.sections():
		print (filename+" does not exist - creating file")
		SavePreferences(filename,True)	# Create default values
		return

	section = 'Preferences'
	Globals.defaultphotodir = ReadConfigValue ( config, section, 'DefaultPhotoDir', str )
	Globals.defaultvideodir = ReadConfigValue ( config, section, 'DefaultVideoDir', str )
	Globals.defaultfilesdir = ReadConfigValue ( config, section, 'DefaultFilesDir', str )
	Globals.defaulttimelapsephotodir = ReadConfigValue ( config, section, 'DefaultTimelapsePhotoDir', str )
	Globals.defaulttimelapsevideodir = ReadConfigValue ( config, section, 'DefaultTimelapseVideoDir', str )
	Globals.defaultphotoname = ReadConfigValue ( config, section, 'DefaultPhotoName', str )
	Globals.defaultphotoformat = ReadConfigValue ( config, section, 'DefaultPhotoFormat', str )
	Globals.defaultvideoname = ReadConfigValue ( config, section, 'DefaultVideoName', str )
	Globals.defaultvideoformat = ReadConfigValue ( config, section, 'DefaultVideoFormat', str )
	formatstr = ReadConfigValue ( config, section, 'DefaultTimestampFormat', str)
	Globals.defaulttimestampformat = formatstr.replace('@','%')
	Globals.phototimestamp = ReadConfigValue ( config, section, 'PhotoTimestamp', bool )
	Globals.videotimestamp = ReadConfigValue ( config, section, 'VideoTimestamp', bool )
	Globals.defaultLanguage = ReadConfigValue ( config, section, 'Language', str )

	section = 'Camera'
	Globals.cameraPresent = ReadConfigValue ( config, section, 'CameraPresent', bool )
	Globals.defaultBrightness = ReadConfigValue ( config, section, 'DefaultBrightness', int )
	Globals.defaultContrast = ReadConfigValue ( config, section, 'DefaultContrast', int )
	Globals.defaultSaturation = ReadConfigValue ( config, section, 'DefaultSaturation', int )
	Globals.defaultSharpness = ReadConfigValue ( config, section, 'DefaultSharpness', int )
	Globals.defaultResolution = ReadConfigValue ( config, section, 'DefaultResolution', int )
	Globals.useVideoPort = ReadConfigValue ( config, section, 'UseVideoPort', bool )
	Globals.imageDenoise = ReadConfigValue ( config, section, 'ImageDenoise', bool )
	Globals.videoDenoise = ReadConfigValue ( config, section, 'VideoDenoise', bool )
	Globals.videoStabilization = ReadConfigValue ( config, section, 'VideoStabilization', bool )
	Globals.exposureCompensation = ReadConfigValue ( config, section, 'ExposureCompensation', int )
	Globals.meteringMode = ReadConfigValue ( config, section, 'MeteringMode', int )
	Globals.drcStrength = ReadConfigValue ( config, section, 'DrcStrength', int )

	section = 'Video'
	Globals.defaultVideoTimeout = ReadConfigValue ( config, section, 'DefaultVideoTimeout', int )
	Globals.defaultFrameRate = ReadConfigValue ( config, section, 'DefaultFrameRate', int )

	section = 'Annotation'
	Globals.timestampEnabled = ReadConfigValue ( config, section, 'TimestampEnabled', bool )
	Globals.framerateEnabled = ReadConfigValue ( config, section, 'FramerateEnabled', bool )
	Globals.transparantBackgroundEnabled = ReadConfigValue ( config, section, 'TransparantBackgroundEnabled', bool )
	Globals.annotateBackgroundColor = ReadConfigValue ( config, section, 'AnnotateBackgroundColor', int )
	Globals.annotateForegroundColor = ReadConfigValue ( config, section, 'AnnotateForegroundColor', int )
	Globals.defaultAnnotateTextsize = ReadConfigValue ( config, section, 'DefaultAnnotateTextsize', int )

	section = 'Preview'
	Globals.defaultAlpha = ReadConfigValue ( config, section, 'DefaultAlpha', int )

	section = 'Network'
	Globals.enableHTTPServer = ReadConfigValue ( config, section, 'EnableHTTPServer', bool )
	Globals.enableVideoStreaming = ReadConfigValue ( config, section, 'EnableVideoStreaming', bool )
	Globals.headingLevel1 = ReadConfigValue ( config, section, 'HeadingLevel1', str )
	Globals.headingLevel2 = ReadConfigValue ( config, section, 'HeadingLevel2', str )

	section = 'Timelapse'
	Globals.defaultTakePictureCount = ReadConfigValue ( config, section, 'DefaultTakePictureCount', int )
	Globals.defaultTakePictureCountType = ReadConfigValue ( config, section, 'DefaultTakePictureCountType', int )
	Globals.defaultStopPictureCount = ReadConfigValue ( config, section, 'DefaultStopPictureCount', int )
	Globals.defaultStopPictureCountType = ReadConfigValue ( config, section, 'DefaultStopPictureCountType', int )
	Globals.defaultTakeVideoCount = ReadConfigValue ( config, section, 'DefaultTakeVideoCount', int )
	Globals.defaultTakeVideoCountType = ReadConfigValue ( config, section, 'DefaultTakeVideoCountType', int )
	Globals.defaultVideoLength = ReadConfigValue ( config, section, 'DefaultVideoLength', int )
	Globals.defaultVideoLengthType = ReadConfigValue ( config, section, 'DefaultVideoLengthType', int )
	Globals.defaultStopVideoCount = ReadConfigValue ( config, section, 'DefaultStopVideoCount', int )
	Globals.defaultStopVideoCountType = ReadConfigValue ( config, section, 'DefaultStopVideoCountType', int )

	section = 'Colors'
	Globals.defaultBackgroundColor = ReadConfigValue ( config, section, 'DefaultBackgroundColor', str )
	Globals.defaultForegroundColor = ReadConfigValue ( config, section, 'DefaultForegroundColor', str )
	Globals.buttonbackcolor  = ReadConfigValue ( config, section, 'Buttonbackcolor', str )
	Globals.buttontextcolor = ReadConfigValue ( config, section, 'Buttontextcolor', str )
	Globals.buttonpressedcolor = ReadConfigValue ( config, section, 'Buttonpressedcolor', str )
	Globals.buttonpressedtextcolor = ReadConfigValue ( config, section, 'Buttonpressedtextcolor', str )
	Globals.sliderbackcolor = ReadConfigValue ( config, section, 'Sliderbackcolor', str )
	Globals.slidercolor = ReadConfigValue ( config, section, 'Slidercolor', str )
	Globals.slidertextcolor = ReadConfigValue ( config, section, 'Slidertextcolor', str )

	section = 'Fonts'
	ReadConfigValue ( config, section, 'DefaultFont', Globals.defaultFont )
	ReadConfigValue ( config, section, 'LabelFont', Globals.labelFont )

	section = 'Layout'
	Globals.defaultButtonHeight = ReadConfigValue ( config, section, 'DefaultButtonHeight', int )
	Globals.defaultButtonPadX = ReadConfigValue ( config, section, 'DefaultButtonPadX', int )
	Globals.defaultButtonPadY = ReadConfigValue ( config, section, 'DefaultButtonPadY', int )
	Globals.defaultSliderHeight = ReadConfigValue ( config, section, 'DefaultSliderHeight', int )
	Globals.defaultSliderPadX = ReadConfigValue ( config, section, 'DefaultSliderPadX', int )
	Globals.defaultSliderPadY = ReadConfigValue ( config, section, 'DefaultSliderPadY', int )

	section = 'JPEG'

	section = 'H264'

def SavePreferences ( filename, createNewFile ):
	config = ConfigParser.SafeConfigParser()
	config.read(filename)

	if createNewFile:
		if Python2:
			config.add_section('Preferences')
			config.add_section('Camera')
			config.add_section('Video')
			config.add_section('Annotation')
			config.add_section('Preview')
			config.add_section('Network')
			config.add_section('Timelapse')
			config.add_section('Colors')
			config.add_section('Fonts')
			config.add_section('Layout')
			config.add_section('JPEG')
			config.add_section('H264')
		else:
			config['Preferences'] = {}
			config['Camera'] = {}
			config['Video'] = {}
			config['Annotation'] = {}
			config['Preview'] = {}
			config['Network'] = {}
			config['Timelapse'] = {}
			config['Colors'] = {}
			config['Fonts'] = {}
			config['Layout'] = {}
			config['JPEG'] = {}
			config['H264'] = {}

	section = 'Preferences'
	UpdateConfigValue ( config, section, 'DefaultPhotoDir', Globals.defaultphotodir )
	UpdateConfigValue ( config, section, 'DefaultVideoDir', Globals.defaultvideodir )
	UpdateConfigValue ( config, section, 'DefaultFilesDir', Globals.defaultfilesdir )
	UpdateConfigValue ( config, section, 'DefaultTimelapsePhotoDir', Globals.defaulttimelapsephotodir )
	UpdateConfigValue ( config, section, 'DefaultTimelapseVideoDir', Globals.defaulttimelapsevideodir )

	UpdateConfigValue ( config, section, 'DefaultPhotoName', Globals.defaultphotoname )
	UpdateConfigValue ( config, section, 'DefaultPhotoFormat', Globals.defaultphotoformat )
	UpdateConfigValue ( config, section, 'DefaultVideoName', Globals.defaultvideoname )
	UpdateConfigValue ( config, section, 'DefaultVideoFormat', Globals.defaultvideoformat )
	formatStr = Globals.defaulttimestampformat.replace('%','@')
	UpdateConfigValue ( config, section, 'DefaultTimestampFormat', formatStr)
	UpdateConfigValue ( config, section, 'PhotoTimestamp', Globals.phototimestamp )
	UpdateConfigValue ( config, section, 'VideoTimestamp', Globals.videotimestamp )
	UpdateConfigValue ( config, section, 'Language', Globals.defaultLanguage )

	section = 'Camera'
	UpdateConfigValue ( config, section, 'CameraPresent', Globals.cameraPresent )
	UpdateConfigValue ( config, section, 'DefaultBrightness', Globals.defaultBrightness )
	UpdateConfigValue ( config, section, 'DefaultContrast', Globals.defaultContrast )
	UpdateConfigValue ( config, section, 'DefaultSaturation', Globals.defaultSaturation )
	UpdateConfigValue ( config, section, 'DefaultSharpness', Globals.defaultSharpness )
	UpdateConfigValue ( config, section, 'DefaultResolution', Globals.defaultResolution )
	UpdateConfigValue ( config, section, 'UseVideoPort', Globals.useVideoPort )
	UpdateConfigValue ( config, section, 'ImageDenoise', Globals.imageDenoise )
	UpdateConfigValue ( config, section, 'VideoDenoise', Globals.videoDenoise )
	UpdateConfigValue ( config, section, 'VideoStabilization', Globals.videoStabilization )
	UpdateConfigValue ( config, section, 'ExposureCompensation', Globals.exposureCompensation )
	UpdateConfigValue ( config, section, 'MeteringMode', Globals.meteringMode )
	UpdateConfigValue ( config, section, 'DrcStrength', Globals.drcStrength )

	section = 'Video'
	UpdateConfigValue ( config, section, 'DefaultVideoTimeout', Globals.defaultVideoTimeout )
	UpdateConfigValue ( config, section, 'DefaultFrameRate', Globals.defaultFrameRate )

	section = 'Annotation'
	UpdateConfigValue ( config, section, 'TimestampEnabled', Globals.timestampEnabled )
	UpdateConfigValue ( config, section, 'FramerateEnabled', Globals.framerateEnabled )
	UpdateConfigValue ( config, section, 'TransparantBackgroundEnabled', Globals.transparantBackgroundEnabled )
	UpdateConfigValue ( config, section, 'AnnotateBackgroundColor', Globals.annotateBackgroundColor )
	UpdateConfigValue ( config, section, 'AnnotateForegroundColor', Globals.annotateForegroundColor )
	UpdateConfigValue ( config, section, 'DefaultAnnotateTextsize', Globals.defaultAnnotateTextsize )

	section = 'Preview'
	UpdateConfigValue ( config, section, 'DefaultAlpha', Globals.defaultAlpha )

	section = 'Network'
	UpdateConfigValue ( config, section, 'EnableHTTPServer', Globals.enableHTTPServer )
	UpdateConfigValue ( config, section, 'EnableVideoStreaming', Globals.enableVideoStreaming )
	UpdateConfigValue ( config, section, 'HeadingLevel1', Globals.headingLevel1 )
	UpdateConfigValue ( config, section, 'HeadingLevel2', Globals.headingLevel2 )


	section = 'Timelapse'
	UpdateConfigValue ( config, section, 'DefaultTakePictureCount', Globals.defaultTakePictureCount )
	UpdateConfigValue ( config, section, 'DefaultTakePictureCountType', Globals.defaultTakePictureCountType )
	UpdateConfigValue ( config, section, 'DefaultStopPictureCount', Globals.defaultStopPictureCount )
	UpdateConfigValue ( config, section, 'DefaultStopPictureCountType', Globals.defaultStopPictureCountType )
	UpdateConfigValue ( config, section, 'DefaultTakeVideoCount', Globals.defaultTakeVideoCount )
	UpdateConfigValue ( config, section, 'DefaultTakeVideoCountType', Globals.defaultTakeVideoCountType )
	UpdateConfigValue ( config, section, 'DefaultVideoLength', Globals.defaultVideoLength )
	UpdateConfigValue ( config, section, 'DefaultVideoLengthType', Globals.defaultVideoLengthType )
	UpdateConfigValue ( config, section, 'DefaultStopVideoCount', Globals.defaultStopVideoCount )
	UpdateConfigValue ( config, section, 'DefaultStopVideoCountType', Globals.defaultStopVideoCountType )

	section = 'Colors'
	UpdateConfigValue ( config, section, 'DefaultBackgroundColor', Globals.defaultBackgroundColor )
	UpdateConfigValue ( config, section, 'DefaultForegroundColor', Globals.defaultForegroundColor )
	UpdateConfigValue ( config, section, 'Buttonbackcolor', Globals.buttonbackcolor )
	UpdateConfigValue ( config, section, 'Buttontextcolor', Globals.buttontextcolor )
	UpdateConfigValue ( config, section, 'Buttonpressedcolor', Globals.buttonpressedcolor )
	UpdateConfigValue ( config, section, 'Buttonpressedtextcolor', Globals.buttonpressedtextcolor )
	UpdateConfigValue ( config, section, 'Sliderbackcolor', Globals.sliderbackcolor )
	UpdateConfigValue ( config, section, 'Slidercolor', Globals.slidercolor )
	UpdateConfigValue ( config, section, 'Slidertextcolor', Globals.slidertextcolor )

	section = 'Fonts'
	UpdateConfigValue ( config, section, 'DefaultFont', Globals.defaultFont )
	UpdateConfigValue ( config, section, 'LabelFont', Globals.labelFont )

	section = 'Layout'
	UpdateConfigValue ( config, section, 'DefaultButtonHeight', Globals.defaultButtonHeight )
	UpdateConfigValue ( config, section, 'DefaultButtonPadX', Globals.defaultButtonPadX )
	UpdateConfigValue ( config, section, 'DefaultButtonPadY', Globals.defaultButtonPadY )
	UpdateConfigValue ( config, section, 'DefaultSliderHeight', Globals.defaultSliderHeight )
	UpdateConfigValue ( config, section, 'DefaultSliderPadX', Globals.defaultSliderPadX )
	UpdateConfigValue ( config, section, 'DefaultSliderPadY', Globals.defaultSliderPadY )

	section = 'JPEG'
	section = 'H264'

	SaveConfigFile(filename, config )

'''
Used here and in Languages.py
'''
def SaveConfigFile ( filename, config ):
	with open(filename, 'w+') as configfile:
		config.write(configfile)

	# now change its permissions so it can be edited by anyone
	# sudo chmod a+w microVIEW.INI
	path = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
	os.system('sudo chmod a+w %s' % (path))
