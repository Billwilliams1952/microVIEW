#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#  microVIEW.py
#
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

appTitle = "microVIEW"

from Buttons		import *
from Globals		import *
from ConfigFile		import *
from Languages		import *
from AllDialogs		import *
from WebStream		import *

import netifaces as ni
import time
import datetime as dt
import os
import sys
from	platform	import *

try:
	import 	picamera
	from 	picamera import *
	import 	picamera.array
except ImportError:
	raise ImportError("You do not seem to have picamera installed")

import PIL
from PIL import Image, ExifTags

if sys.version_info[0] == 3:
	from	tkinter import *	# Python 3.X
	import	tkinter.filedialog as FileDialog
	import	tkinter.messagebox as MessageBox
	from	tkinter import ttk
	from 	tkinter.ttk import *
	import	tkinter.font
	try:
		from PIL import ImageTk
	except ImportError:
		raise ("ImageTk not installed.\n" \
				"Install using: sudo apt-get install python3-pil.imagetk")
else:
	from	Tkinter import *	# Python 2.X
	import 	tkFileDialog as FileDialog
	import 	tkMessageBox as MessageBox
	import 	ttk
	from 	ttk import *
	import 	tkFont
	
NoRequire = False
try:
	from pkg_resources import require
except ImportError:
	print ( "Cannot import 'require' from 'pkg_resources'" )
	NoRequire = True


'''
The main microVIEW window.
'''
class microVIEW ( Frame ):
	def __init__(self, root, camera, language, title, width, height):
		Frame.__init__(self, root)

		#self.grid(padx=5,pady=5)
		self.root = root
		self.root.rowconfigure(0,weight=1)		# size frames to window
		self.root.columnconfigure(1,weight=1)	# size frames to window
		self.width = width
		self.height = height

		self.PhotoImg = self.GetImage('Assets/camera.png')
		self.TakePhotoImg = self.GetImage('Assets/takePhoto.png')
		self.StartVideoImg = self.GetImage('Assets/video.png')
		self.StopVideoImg = self.GetImage('Assets/videoStop.png')
		self.OptionsImg = self.GetImage('Assets/options.png')
		self.CloseImg = self.GetImage('Assets/close.png')

		Style().configure('F.TFrame',background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultBackgroundColor)
		self.config(style='F.TFrame')
		Style().configure('FA.TFrame',background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultBackgroundColor,
			bordercolor=Globals.defaultBackgroundColor,borderwidth=0,
			lightcolor=Globals.defaultBackgroundColor,
			darkcolor=Globals.defaultBackgroundColor)
		Style().configure('Button.TButton',background=Globals.buttonbackcolor,
			foreground=Globals.buttontextcolor,font=Globals.defaultFont)
		Style().configure('Black.TButton',background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultBackgroundColor,
			highlightcolor=Globals.defaultBackgroundColor,
			focuscolor=Globals.defaultBackgroundColor,
			activebackground=Globals.defaultBackgroundColor,
			activeforeground=Globals.defaultBackgroundColor,borderwidth=0,
			highlightbackground=Globals.defaultBackgroundColor)
		Style().configure('Label.TLabel',font=Globals.labelFont,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor,sticky='W')
		Style().configure('Shaded.TFrame',background='#303030',
			foreground='#303030',bordercolor='#303030',borderwidth=0,
			lightcolor='#303030',darkcolor='#303030')
		Style().configure('Shaded.TLabel',font=Globals.labelFont,
			foreground=Globals.defaultForegroundColor,
			background='#303030',sticky='W')

		self.camera = camera
		self.camera.framerate = Globals.defaultFrameRate	# Allow changing?
		self.preview = self.camera.start_preview(fullscreen=True,
			alpha=Globals.defaultAlpha)

		self.stream = None

		self.language = language

		self.VideoInProgress = False
		self.VideoTimelapse = False
		self.PhotoTimelapse = False
		self.InOptions = False

		self.back = Label(background=Globals.defaultBackgroundColor)
		self.back.place(x=0,y=0,width=width,height=height)

		self.mainFrame = Frame(self.root,style='F.TFrame')
		self.mainFrame.grid(row=0,column=0,sticky='nsew')
		self.mainFrame.rowconfigure(0,weight=1)
		self.mainFrame.columnconfigure(0,weight=1)

		self.MainNotebook = LangNotebook(self.mainFrame,language=self.language)
		self.MainNotebook.grid(row=0,column=0,sticky='nsew')
		self.MainNotebook.rowconfigure(0,weight=1)

		BasicNotebookTab = Frame(style='F.TFrame')
		BasicNotebookTab.columnconfigure(0,weight=1)
		BasicNotebookTab.rowconfigure(0,weight=1)
		self.MainNotebook.add(BasicNotebookTab,text='Basic')

		AdvancedNotebookTab = Frame(style='F.TFrame')
		AdvancedNotebookTab.columnconfigure(0,weight=1)
		AdvancedNotebookTab.rowconfigure(0,weight=1)
		self.MainNotebook.add(AdvancedNotebookTab ,text='Advanced')

		TimelapseNotebookTab = Frame(style='F.TFrame')
		TimelapseNotebookTab.columnconfigure(0,weight=1)
		TimelapseNotebookTab.rowconfigure(0,weight=1)
		self.MainNotebook.add(TimelapseNotebookTab ,text='Timelapse')

		PreferenceNotebookTab = Frame(style='F.TFrame')
		PreferenceNotebookTab.columnconfigure(0,weight=1)
		PreferenceNotebookTab.rowconfigure(0,weight=1)
		self.MainNotebook.add(PreferenceNotebookTab ,text='Preferences')

		self.MainNotebook.UpdateLang()		# Initial update....

		#--------- Now add the DONE button --------
		fa = Frame(self.mainFrame,style='F.TFrame')
		fa.grid(row=0,column=1,sticky='nsew')
		self.doneOptions = MyButton(fa,text='Done with options',
			height=50,width=220,language=self.language,
			callback=self.DoneOptions,anchor='bottom')
		self.doneOptions.grid(row=0,column=0,sticky='w',pady=15,padx=50)
		#--------- Text display --------
		l = Label(fa,text=appTitle,background='black',
			font="Arial 30 bold",foreground='yellow')
		l.grid(row=0,column=2,padx=15,pady=0)

		# -------------- Now the Basic page layout ----------------
		BasicPage = Frame(BasicNotebookTab,style='F.TFrame')
		BasicPage.grid(row=0,column=0,sticky='nsew')
		BasicPage.columnconfigure(0,weight=1)

		self.brightness = Slider(BasicPage,text='Brightness',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.BrightnessChanged,_from=0,_to=100,
			value=Globals.defaultBrightness)
		self.brightness.grid(row=0,column=0,sticky='ew',padx=20,pady=20)
		self.BrightnessChanged(Globals.defaultBrightness)

		self.contrast = Slider(BasicPage,text='Contrast',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.ContrastChanged,_from=-100,_to=100,
			value=Globals.defaultContrast)
		self.contrast.grid(row=1,column=0,sticky='ew',padx=20,pady=(0,20))
		self.ContrastChanged(Globals.defaultContrast)

		self.saturation = Slider(BasicPage,text='Saturation',
			padding=(25,25,25,25),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.SaturationChanged,_from=-100,_to=100,
			value=Globals.defaultSaturation)
		self.saturation.grid(row=2,column=0,sticky='ew',padx=20,pady=(0,20))
		self.SaturationChanged(Globals.defaultSaturation)

		self.sharpness = Slider(BasicPage,text='Sharpness',
			padding=(25,25,25,25),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.SharpnessChanged,_from=-100,_to=100,
			value=Globals.defaultSharpness)
		self.sharpness.grid(row=3,column=0,sticky='ew',padx=20,pady=(0,20))
		self.SharpnessChanged(Globals.defaultSharpness)

		self.alpha = Slider(BasicPage,text='Transparancy',
			padding=(25,25,25,25),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.AlphaChanged,_from=0,_to=255,
			value=Globals.defaultAlpha)
		self.alpha.grid(row=4,column=0,sticky='ew',padx=20,pady=(0,20))
		self.AlphaChanged(Globals.defaultAlpha)

		self.setResolutionLabel = LangLabel(BasicPage,text='setresolution',
			language=self.language)
		self.setResolutionLabel.grid(row=5,column=0,sticky='W',padx=(20,20))

		res = ['CGA: (320x200)','QVGA: (320x240)','VGA: (640x480)','PAL: (768x576)',
				 '480p: (720x480)','576p: (720x576)', 'WVGA: (800x480)',
				 'SVGA: (800x600)', 'FWVGA: (854x480)', 'WSVGA: (1024x600)',
				 'XGA: (1024x768)', 'HD 720: (1280x720)', 'WXGA_1: (1280x768)',
				 'WXGA_2: (1280x800)', 'SXGA: (1280x1024)', 'SXGA+: (1400x1050)',
				 'UXGA: (1600x1200)', 'WSXGA+: (1680x1050)', 'HD 1080: (1920x1080)',
				 'WUXGA: (1920x1200)', '2K: (2048x1080)', 'QXGA: (2048x1536)',
				 'WQXGA: (2560x1600)', 'WQXGA: (2592x1944)' ]
		self.resolution = Slider(BasicPage,text=res,padding=(25,25,25,25),
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.ResolutionChanged,
			value=Globals.defaultResolution)
		self.resolution.grid(row=6,column=0,sticky='ew',padx=20,pady=(0,20))
		self.ResolutionChanged(res[Globals.defaultResolution])

		'''
		Build the Advanced notebook page for Camera, Annotate
		'''
		AdvancedNotebook = LangNotebook(AdvancedNotebookTab,
			padding=(15,15,15,15),language=self.language)
		AdvancedNotebook.grid(row=0,column=0,sticky='nsew')
		AdvancedNotebook.rowconfigure(0,weight=1)

		#------------- Camera page -------------
		CameraTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		CameraTab.grid(row=0,column=0,sticky='nsew')
		CameraTab.columnconfigure(0,weight=1)
		AdvancedNotebook.add(CameraTab ,text='Camera')

		f10 = Frame(CameraTab,style='F.TFrame')
		f10.grid(row=0,column=0,sticky='nsew')

		LangLabel(f10,text='Use Video Port',
			language=self.language).grid(row=0,column=1,sticky='W')
		self.UseVideoPort = PushButton(f10,width=50,
			value=Globals.useVideoPort,text=['OFF','ON'],
			callback=self.ToggleUseStillPort,language=self.language)
		self.UseVideoPort.grid(row=0,column=0,sticky='W')

		LangLabel(f10,text='Video Stabilization',
			language=self.language).grid(row=0,column=3,sticky='W')
		self.VideoStab = PushButton(f10,width=50,
			value=Globals.videoStabilization,text=['OFF','ON'],
			callback=self.ToggleVideoStabilization,language=self.language)
		self.VideoStab.grid(row=0,column=2,sticky='W',padx=(35,0))

		LangLabel(f10,text='Image Denoise',
			language=self.language).grid(row=1,column=1,sticky='W',pady=(15,0))
		self.ImageDenoise = PushButton(f10,width=50,
			value=Globals.imageDenoise,text=['OFF','ON'],
			callback=self.ToggleImageDenoise,language=self.language)
		self.ImageDenoise.grid(row=1,column=0,sticky='W',pady=(15,0))

		LangLabel(f10,text='Video Denoise',
			language=self.language).grid(row=1,column=3,sticky='W',pady=(15,0))
		self.VideoDenoise = PushButton(f10,width=50,
			value=Globals.videoDenoise,text=['OFF','ON'],
			callback=self.ToggleVideoDenoise,language=self.language)
		self.VideoDenoise.grid(row=1,column=2,sticky='W',padx=(35,0),pady=(15,0))

		f10 = Frame(CameraTab,style='F.TFrame')
		f10.grid(row=1,column=0,sticky='nsew')
		f10.columnconfigure(2,weight=1)

		l = LangLabel(f10,text='Metering Mode:',language=self.language)
		l.grid(row=0,column=0,sticky='E',pady=(15,0))
		self.meterMode = MultiTouchButton(f10,value=Globals.meteringMode,
			text=['average','spot','backlit','matrix'],
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.MeterModeChanged,width=200)
		self.meterMode.grid(row=0,column=1,padx=(15,0),pady=(15,0))

		l = LangLabel(f10,text='Exposure:',language=self.language)
		l.grid(row=1,column=0,sticky='E',pady=(15,0))
		self.exposureComp = Slider(f10,#fcamera,
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.ExposureCompChanged,_from=-25,_to=25,width=50,
			value=Globals.exposureCompensation,addValue=False)
		self.exposureComp.grid(row=1,column=1,columnspan=2,sticky='ew',
			padx=(15,0),pady=(15,0))

		LangLabel(f10,text='Dynamic Range Compression:',
			language=self.language).grid(row=2,column=0,sticky='E',pady=(15,0))
		self.meterMode = MultiTouchButton(f10,text=['None','Low','Medium','High'],
			value=Globals.drcStrength,language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.DRCStrengthChanged,width=200)
		self.meterMode.grid(row=2,column=1,padx=(15,0),pady=(15,0))

		self.ToggleUseStillPort(Globals.useVideoPort)
		self.ToggleVideoStabilization(Globals.videoStabilization)
		self.ToggleImageDenoise(Globals.imageDenoise)
		self.ToggleVideoDenoise(Globals.videoDenoise)
		self.MeterModeChanged(Globals.meteringMode)
		self.ExposureCompChanged(Globals.exposureCompensation)
		self.DRCStrengthChanged(Globals.drcStrength)

		#------------- Annotate page -------------
		AnnotateTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		AnnotateTab.grid(row=0,column=0,sticky='nsew')
		AnnotateTab.columnconfigure(0,weight=1)
		AdvancedNotebook.add(AnnotateTab ,text='Annotate')

		f10 = Frame(AnnotateTab,style='F.TFrame')
		f10.grid(row=0,column=0,sticky='nsew')

		LangLabel(f10,text='Time-Stamp',
			language=self.language).grid(row=0,column=1,sticky='W')
		self.enableTimestamp = PushButton(f10,width=50,
			value=Globals.timestampEnabled,text=['OFF','ON'],
			callback=self.ToggleTimestamp,language=self.language)
		self.enableTimestamp.grid(row=0,column=0,sticky='W')

		LangLabel(f10,text='Frame Number',
			language=self.language).grid(row=0,column=3,sticky='W')
		self.AnnotateFrameNum = PushButton(f10,width=50,
			value=Globals.framerateEnabled,text=['OFF','ON'],
			callback=self.ToggleAnnotateFrameNum,language=self.language)
		self.AnnotateFrameNum.grid(row=0,column=2,sticky='W',padx=(35,0))

		f10 = Frame(AnnotateTab,style='F.TFrame')
		f10.grid(row=1,column=0,sticky='nsew',pady=(15,0))
		f10.columnconfigure(1,weight=1)

		LangLabel(f10,text='Identify Text:',
			language=self.language).grid(row=0,column=0,sticky='W')

		self.identify = ''
		self.identifyText = MultiTouchButton(f10,
			text=['None',Globals.headingLevel1,Globals.headingLevel2],language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.IdentifyTextChanged,
			value=0,width=450)
		self.identifyText.grid(row=0,column=1,sticky='ew',padx=(20,0))

		self.annotateSize = Slider(AnnotateTab,text='Annotate Text Size',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.AnnotateSizeChanged,_from=6,_to=160,width=300,
			value=Globals.defaultAnnotateTextsize)
		self.annotateSize.grid(row=2,column=0,columnspan=2,sticky='EW',
			pady=(15,0))

		f10 = Frame(AnnotateTab,style='F.TFrame')
		f10.grid(row=3,column=0,sticky='nsew',pady=(15,0))
		f10.columnconfigure(2,weight=1)

		self.enableTransparentBackgroundColor = PushButton(f10,width=50,
			value=Globals.transparantBackgroundEnabled,text=['OFF','ON'],
			callback=self.EnableTransparentBackgroundColor,language=self.language)
		self.enableTransparentBackgroundColor.grid(row=0,column=0,sticky='W')
		LangLabel(f10,text='Transparant background',
			language=self.language).grid(row=0,column=1,sticky='E')

		self.annotateBackgroundColor = Slider(f10,text='Background Color',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.AnnotateBackgroundColorChanged,_from=0,_to=100,width=250,
			value=Globals.annotateBackgroundColor)
		self.annotateBackgroundColor.grid(row=0,column=2,columnspan=2,sticky='EW',
			padx=(40,0))
		self.AnnotateBackgroundColorChanged(Globals.annotateBackgroundColor)

		self.annotateForegroundColor = Slider(AnnotateTab,text='Foreground Color',
			background=Globals.defaultBackgroundColor,language=self.language,
			callback=self.AnnotateForegroundColorChanged,_from=0,_to=100,width=200,
			value=Globals.annotateForegroundColor)
		self.annotateForegroundColor.grid(row=4,column=0,columnspan=2,sticky='EW',
			pady=(15,0))

		self.ToggleTimestamp(Globals.timestampEnabled)
		self.ToggleAnnotateFrameNum(Globals.framerateEnabled)
		self.EnableTransparentBackgroundColor(Globals.transparantBackgroundEnabled)
		AdvancedNotebook.UpdateLang()

		'''
		-------------------- Preferences Notebook ----------------------
		'''
		self.PreferencesNotebook = LangNotebook(PreferenceNotebookTab,
			padding=(15,15,15,15),language=self.language)
		self.PreferencesNotebook.grid(row=0,column=0,rowspan=2,sticky='nsew')
		self.PreferencesNotebook.rowconfigure(0,weight=1)
		self.PreferencesNotebook.columnconfigure(0,weight=1)

		#GeneralTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		#self.PreferencesNotebook.add(GeneralTab ,text='General')
		FilesTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		self.PreferencesNotebook.add(FilesTab,text='Files')
		NetworkTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		NetworkTab.columnconfigure(0,weight=1)
		self.PreferencesNotebook.add(NetworkTab,text='Network')
		InterfaceTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		self.PreferencesNotebook.add(InterfaceTab ,text='Interface')
		AboutTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		AboutTab.grid(sticky='nsew')
		AboutTab.columnconfigure(0,weight=1)
		AboutTab.rowconfigure(0,weight=1)
		self.PreferencesNotebook.add(AboutTab,text='About')

		self.PreferencesNotebook.UpdateLang()

		#---------------------- General --------------------
		#l = LangLabel(GeneralTab,text='What controls or information would go here?\n' +
			#'Consider Raspberry PI ID or name that would be used on streaming page.\n' +
			#'General information on RPI (like an About Page?).\n' +
			#'Other information.....',
			#language=self.language,style='Label.TLabel',wraplength=500)
		#l.grid(row=0,column=0,pady=(20,0),columnspan=2)

		#---------------------- Interface --------------------
		l = LangLabel(InterfaceTab,text='Select language:',language=self.language,
			style='Label.TLabel')
		l.grid(row=0,column=0)

		for index, lan in enumerate(self.language.sections):
			if lan == Globals.defaultLanguage:
				break;
		self.textLanguage = MultiTouchButton(InterfaceTab,
			text=self.language.sections,language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.LanguageChanged,
			value=index,width=130)
		self.textLanguage.grid(row=0,column=1,sticky='ew',padx=(20,0))

		l = LangLabel(InterfaceTab,text='Add additional controls to size text and controls',
			language=self.language,style='Label.TLabel',wraplength=500)
		l.grid(row=1,column=0,pady=(20,0),columnspan=2)

		#---------------------- Files --------------------
		l = LangLabel(FilesTab,style='Label.TLabel',language=self.language,
			text='Directories for Photos and Videos:')
		l.grid(row=0,column=0,sticky='W',columnspan=2)
		self.selectPhotoDirectory = MyButton(FilesTab,text='Photos',
			width=200,language=self.language,
			callback=self.SelectPhotoDirectory)
		self.selectPhotoDirectory.grid(row=1,column=0,sticky='w',pady=(20,0))
		self.photoDirLabel = Label(FilesTab,style='Label.TLabel',text=Globals.defaultphotodir)
		self.photoDirLabel.grid(row=1,column=1,sticky='W',padx=(20,0),pady=(20,0))

		self.selectVideoDirectory = MyButton(FilesTab,text='Videos',
			width=200,language=self.language,
			callback=self.SelectVideoDirectory)
		self.selectVideoDirectory.grid(row=2,column=0,sticky='w',pady=(20,0))
		self.videoDirLabel = Label(FilesTab,style='Label.TLabel',text=Globals.defaultvideodir)
		self.videoDirLabel.grid(row=2,column=1,sticky='W',padx=(20,0),pady=(20,0))

		self.selectTimelapsePhotoDirectory = MyButton(FilesTab,text='Timelapse Photos',
			width=200,language=self.language,
			callback=self.SelectTimelapsePhotoDirectory)
		self.selectTimelapsePhotoDirectory.grid(row=3,column=0,sticky='w',pady=(20,0))
		self.timelapsephotoDirLabel = Label(FilesTab,style='Label.TLabel',text=Globals.defaulttimelapsephotodir)
		self.timelapsephotoDirLabel.grid(row=3,column=1,sticky='W',padx=(20,0),pady=(20,0))

		self.selectTimelapseVideoDirectory = MyButton(FilesTab,text='Timelapse Videos',
			width=200,language=self.language,
			callback=self.SelectTimelapseVideoDirectory)
		self.selectTimelapseVideoDirectory.grid(row=4,column=0,sticky='w',pady=(20,0))
		self.timelapsevideoDirLabel = Label(FilesTab,style='Label.TLabel',text=Globals.defaulttimelapsevideodir)
		self.timelapsevideoDirLabel.grid(row=4,column=1,sticky='W',padx=(20,0),pady=(20,0))

		#---------------------- Network --------------------
		f10 = Frame(NetworkTab,style='F.TFrame')
		f10.grid(row=0,column=0,sticky='nsew')
		f10.columnconfigure(0,weight=1)

		l = LangLabel(f10,text='Connection',wraplength=500,language=self.language)
		l.grid(row=0,column=0,sticky='NSEW')

		f10 = Frame(NetworkTab,style='Shaded.TFrame')
		f10.grid(row=1,column=0,sticky='NSEW',pady=(20,0))
		self.wlan0Label = LangLabel(f10,text='',
			language=self.language)
		self.wlan0Label.config(style='Shaded.TLabel')
		self.wlan0Label.grid(row=1,column=0,sticky='W',padx=15,pady=(15,0))
		self.eth0Label = LangLabel(f10,text='',
			language=self.language)
		self.eth0Label.config(style='Shaded.TLabel')
		self.eth0Label.grid(row=2,column=0,padx=15,pady=(15,15),sticky='W')
		self.UpdateInternetConnections()

		f10 = Frame(NetworkTab,style='F.TFrame')
		f10.grid(row=3,column=0,sticky='nsew',pady=(15,0))

		self.HttpServerEnabled = PushButton(f10,width=50,
			value=False,	# ALWAYS START OFF
			text=['OFF','ON'],language=self.language,
			callback=self.HTTPServerEnabled)
		self.HttpServerEnabled.grid(row=0,column=0,sticky='W')
		LangLabel(f10,text='HTTP server enabled',language=self.language,
			style='Label.TLabel').grid(row=0,column=1,sticky='W')
		self.videoStreamingEnabled = PushButton(f10,width=50,
			value=Globals.enableVideoStreaming,text=['OFF','ON'],
			callback=self.VideoStreamingEnabled,language=self.language)
		self.videoStreamingEnabled.grid(row=0,column=2,sticky='W',padx=(40,0))
		LangLabel(f10,text='Video stream',
			language=self.language).grid(row=0,column=3,sticky='W')

		self.HTTPServerEnabled(False)
		self.videoStreamingEnabled.enable = False
		self.VideoStreamingEnabled(Globals.enableVideoStreaming)
		
		#---------------------- About Notebook --------------------
		self.AboutNotebook = LangNotebook(AboutTab,language=self.language)
		self.AboutNotebook.grid(row=0,column=0,sticky='nsew')
		self.AboutNotebook.rowconfigure(0,weight=1)
		self.AboutNotebook.columnconfigure(0,weight=1)
		AboutMeTab = Frame(style='F.TFrame')
		AboutMeTab.grid(row=0,column=0,sticky='NSEW')
		#AboutMeTab.rowconfigure(0,weight=1)
		AboutMeTab.columnconfigure(0,weight=1)
		self.AboutNotebook.add(AboutMeTab ,text='About')
		CreditsTab = Frame(style='F.TFrame')
		CreditsTab.grid(row=0,column=0,sticky='NSEW')
		#CreditsTab.rowconfigure(0,weight=1)
		CreditsTab.columnconfigure(0,weight=1)
		self.AboutNotebook.add(CreditsTab ,text='Credits')
		LicenseTab = Frame(style='F.TFrame')
		LicenseTab.grid(row=0,column=0,sticky='NSEW')
		#LicenseTab.rowconfigure(0,weight=1)
		LicenseTab.columnconfigure(0,weight=1)
		self.AboutNotebook.add(LicenseTab,text='License')
		
		#--------------- About page ---------------------
		Label(AboutMeTab,text='microVIEW Application',
			anchor='center',font=('Helvetica',20,'bold'),
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor) \
			.grid(row=0,column=0,sticky='ew',pady=(20,20))

		f = ('Helvetica',16)
		Label(AboutMeTab,text='Copyright (C) 2018',
			anchor='center',font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=1,column=0,sticky='ew')
		Label(AboutMeTab,text='Bill Williams (github.com/Billwilliams1952/)',
			anchor='center',font=f,
			background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultForegroundColor).grid(row=2,column=0,sticky='ew',pady=(5,0))

		rev = self.camera.revision
		if rev == "ov5647": camType = "V1"
		elif rev == "imx219" : camType = "V2"
		else: camType = "Unknown"
		f = ('Helvetica',14)
		Label(AboutMeTab,text="Camera revision: " + rev + " (" + camType + \
			" module)",font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=3,column=0,sticky='EW',pady=(20,0),padx=(10,0))

		if NoRequire:
			PiVer = "Picamera library version unknown"
			PILVer = "Pillow (PIL) library version unknown"
			if sys.version_info[0] == 3:
				NetifaceVer = "netifaces library version unknown"
		else:
			PiVer = "PiCamera library version %s" % require('picamera')[0].version
			PILVer = "Pillow (PIL) library version %s" % require('Pillow')[0].version
			if sys.version_info[0] == 3:
				NetifaceVer = "netifaces library version %s" % require('netifaces')[0].version

		Label(AboutMeTab,text=PiVer,font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=4,column=0,sticky='EW',padx=(10,0))
		Label(AboutMeTab,text=PILVer,font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=5,column=0,sticky='EW',padx=(10,0))
		row = 6
		if sys.version_info[0] == 3:
			Label(AboutMeTab,text=NetifaceVer,font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=6,column=0,sticky='EW',padx=(10,0))
			row = 7
		s = processor()
		if s:
			txt = 'Processor type: %s (%s)' % (processor(), machine())
		else:
			txt = 'Processor type: %s' % machine()
		Label(AboutMeTab,text=txt,font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=row,column=0,sticky='EW',padx=(10,0))
		Label(AboutMeTab,text='Platform: %s' % platform(),font=f,
			foreground=Globals.defaultForegroundColor,
			background=Globals.defaultBackgroundColor).grid(row=row+1,
				column=0,sticky='EW',padx=(10,0))


		#--------------- Credits page ---------------------
		#f = MyLabelFrame(self,'Thanks To',0,0)
		string = \
		"\n\n    Camera programming information courtesy of:\n" \
		"        picamera.readthedocs.io/en/release-1.13/api_camera.html\n\n" \
		"    Various free icons courtesy of:\n" \
		"        iconfinder.com/icons/ and icons8.com/icon/\n" \
		""
		Label(CreditsTab,text=string,font=Globals.labelFont,
			background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultForegroundColor).grid(row=0,column=0,sticky='NEW')
		
		#--------------- License page ---------------------
		self.sb = Scrollbar(LicenseTab,orient='vertical')
		self.sb.grid(row=0,column=1,sticky='NEWS')
		self.text = Text(LicenseTab,height=35,width=50,wrap='word',
			yscrollcommand=self.sb.set,font=Globals.labelFont,
			background=Globals.defaultBackgroundColor,
			foreground=Globals.defaultForegroundColor)
		self.text.grid(row=0,column=0,sticky='NEWS')
		self.text.bind("<Key>",lambda e : "break")	# ignore all keypress
		# Note: return "break" from event handler to ignore
		self.sb.config(command=self.text.yview)
		try:
			with open('gpl.txt') as f: self.text.insert(END,f.read())
		except IOError:
			self.text.insert(END,"\n\n\n\t\tError reading file 'gpl.txt'")
		'''
		------------------------------------------------------------------
		Build the timelapse notebook page. This consists of a notebook for
		containing the controls for photo timelapse and video timelapse.
		'''
		self.TimelapseNotebook = LangNotebook(TimelapseNotebookTab,
			padding=(15,15,15,15),language=self.language)
		self.TimelapseNotebook.grid(row=0,column=0,rowspan=2,sticky='nsew')
		PhotoTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		PhotoTab.columnconfigure(0,weight=1)
		self.TimelapseNotebook.add(PhotoTab ,text='Photos')

		self.photoCount = 1
		self.photoEnd = dt.datetime.now()
		self.delayBetweenPhoto = 0
		self.takePictureEvery = Slider(PhotoTab,text='Take Picture every',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.TakePictureEveryChanged,_from=1,_to=59,
			value=Globals.defaultTakePictureCount,width=200)
		self.takePictureEvery.grid(row=0,column=0,sticky='ew')

		self.whenToTakePicture = MultiTouchButton(PhotoTab,
			text=['seconds','minutes','hours','days'],language=self.language,
			value=Globals.defaultTakePictureCountType,
			background=Globals.defaultBackgroundColor,
			callback=self.WhenToTakePictureChanged,width=120)
		self.whenToTakePicture.grid(row=0,column=1,sticky='ew',padx=(20,0))

		self.stopPictureCount = Slider(PhotoTab,text='Stop after',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.StopPictureCountChanged,_from=1,_to=59,
			value=Globals.defaultStopPictureCount,width=200)
		self.stopPictureCount.grid(row=1,column=0,sticky='ew',pady=(20,0))

		self.whenToStopPicture = MultiTouchButton(PhotoTab,
			text=['pictures','seconds','minutes','hours','days'],
			language=self.language,
			value=Globals.defaultStopPictureCountType,
			background=Globals.defaultBackgroundColor,
			callback=self.WhenToStopPictureChanged,width=120)
		self.whenToStopPicture.grid(row=1,column=1,sticky='ew',padx=(20,0),pady=(20,0))

		f10 = Frame(PhotoTab,style='F.TFrame')
		f10.grid(row=2,column=0,columnspan=2,sticky='nsew',pady=(20,0))

		self.startPhotoTimelapse = PushButton(f10,width=50,
			value=False,text=['OFF','ON'],
			callback=self.StartPhotoTimelapse,language=self.language)
		self.startPhotoTimelapse.grid(row=0,column=0,sticky='W')
		LangLabel(f10,text='Time-Lapse',
			language=self.language).grid(row=0,column=1,sticky='W')
		self.photoLabel = Label(f10,style='Label.TLabel')
		self.photoLabel.grid(row=0,column=2,sticky='W',padx=(40,0))

		self.TakePictureEveryChanged(Globals.defaultTakePictureCount)
		self.WhenToTakePictureChanged(Globals.defaultTakePictureCountType)
		self.StopPictureCountChanged(Globals.defaultStopPictureCount)
		self.WhenToStopPictureChanged(Globals.defaultStopPictureCountType)

		#----------------- Video Timelapse ------------------------------
		VideoTab = Frame(style='F.TFrame',padding=(15,15,15,15))
		VideoTab.columnconfigure(0,weight=1)
		self.TimelapseNotebook.add(VideoTab ,text='Videos')

		self.videoCount = 1
		self.videoLength = 0
		self.videoEnd = dt.datetime.now()
		self.delayBetweenVideo = 0

		self.takeVideoEvery = Slider(VideoTab,text='Capture Video every',
			language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.TakeVideoEveryChanged,_from=1,_to=59,
			value=Globals.defaultTakeVideoCount,width=200)
		self.takeVideoEvery.grid(row=0,column=0,sticky='ew')

		self.whenToTakeVideo = MultiTouchButton(VideoTab,
			text=['seconds','minutes','hours','days'],
			language=self.language,
			padding=(10,10,10,10),value=Globals.defaultTakeVideoCountType,
			background=Globals.defaultBackgroundColor,
			callback=self.WhenToTakeVideoChanged,width=120)
		self.whenToTakeVideo.grid(row=0,column=1,sticky='ew',padx=(20,0))

		self.videoLength = Slider(VideoTab,text='Video length',
			padding=(10,10,10,10),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.VideoLengthChanged,_from=1,_to=59,
			value=Globals.defaultVideoLength,width=200)	# Use Global here....
		self.videoLength.grid(row=1,column=0,sticky='ew',pady=(20,0))

		self.videoLengthType = MultiTouchButton(VideoTab,text=['seconds','minutes'],
			padding=(10,10,10,10),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.VideoLengthTypeChanged,width=120,value=Globals.defaultVideoLengthType)
		self.videoLengthType.grid(row=1,column=1,sticky='ew',padx=(20,0),pady=(20,0))

		self.stopVideoCount = Slider(VideoTab,text='Stop after',
			padding=(10,10,10,10),language=self.language,
			background=Globals.defaultBackgroundColor,
			callback=self.StopVideoCountChanged,_from=1,_to=59,
			value=Globals.defaultStopVideoCount,width=200)	# Use Global here....
		self.stopVideoCount.grid(row=2,column=0,sticky='ew',pady=(20,0))

		self.whenToStopVideo = MultiTouchButton(VideoTab,
			text=['videos','seconds','minutes','hours','days'],
			language=self.language,
			padding=(10,10,10,10),value=Globals.defaultStopVideoCountType,
			background=Globals.defaultBackgroundColor,
			callback=self.WhenToStopVideoChanged,width=120)
		self.whenToStopVideo.grid(row=2,column=1,sticky='ew',padx=(20,0),pady=(20,0))

		f10 = Frame(VideoTab,style='F.TFrame')
		f10.grid(row=3,column=0,columnspan=2,sticky='nsew',pady=(20,0))

		self.startVideoTimelapse = PushButton(f10,width=50,
			value=False,text=['OFF','ON'],
			callback=self.StartVideoTimelapse,language=self.language)
		self.startVideoTimelapse.grid(row=0,column=0,sticky='w')
		LangLabel(f10,text='Time-Lapse',
			language=self.language).grid(row=0,column=1,sticky='W')

		self.videoLabel = Label(f10,style='Label.TLabel')
		self.videoLabel.grid(row=0,column=2,sticky='W',padx=(40,0))

		self.TakeVideoEveryChanged(Globals.defaultTakeVideoCount)
		self.WhenToTakeVideoChanged(Globals.defaultTakeVideoCountType)
		self.VideoLengthChanged(Globals.defaultVideoLength)
		self.VideoLengthTypeChanged(Globals.defaultVideoLengthType)
		self.StopVideoCountChanged(Globals.defaultStopVideoCount)
		self.WhenToStopVideoChanged(Globals.defaultStopVideoCountType)

		self.TimelapseNotebook.UpdateLang()

		# --------------- Done Timelapse page -----------------
		'''
		This is kind of a hack since I'm using fixed locations for the
		images, and then using the 'place' method to locate the actual
		buttons behind the overlay images. This needs to change to use
		the 'grid' method for all controls. I can hand tune the placement
		of the controls in the grid using padx and pady.
		'''
		self.xList = []
		self.w = self.imageSize[0]
		self.h = self.imageSize[1]
		self.padding = int((self.width - 10 * self.w) / 2)	# padding from right / left
		self.dx = self.imageSize[0] * 3		# next one....
		x = self.padding
		self.xList.append(x)
		self.close = ttk.Button(text='DONE',command=self.Close,style='Black.TButton')
		self.close.place(x=x,y=int(height-120),width=self.w,height=self.h)
		x += self.dx
		self.xList.append(x)
		self.options = ttk.Button(text='',command=self.Options,style='Black.TButton')
		self.options.place(x=x,y=int(height-120),width=self.w,height=self.h)
		x += self.dx
		self.xList.append(x)
		self.photo = ttk.Button(text='',command=self.TakePhoto,style='Black.TButton')
		self.photo.place(x=x,y=int(height-120),width=self.w,height=self.h)
		x += self.dx
		self.xList.append(x)
		self.video = ttk.Button(text='',command=self.Video,style='Black.TButton')
		self.video.place(x=x,y=int(height-120),width=self.w,height=self.h)

		self.ShowHideButtons(True)

		self.AddOverlays()

		root.bind('Control-c',self.Close)	# NOT WORKING
	'''
	Simple web server functions
	'''
	def UpdateInternetConnections ( self ):
		try:
			ip = ( 'Address for wlan0 (WiFi): http://' +
					  ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'] +
					 ':8000' )
			self.wlan0 = True
		except:
			ip = "Wifi is not connected"
			self.wlan0 = False
		self.wlan0Label.config(text=ip)
		try:
			ip = ( 'Address for eth0 (Ethernet): http://' +
					  ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] +
					 ':8000' )
			self.eth0 = True
		except:
			ip = "Ethernet is not connected"
			self.eth0 = False
		self.eth0Label.config(text=ip)
		self.after(5000,self.UpdateInternetConnections)
	def HTTPServerEnabled ( self, val ):
		if val:
			self.stream = StreamingVideo(self.camera, 1, None )
			self.stream.StartStream()
			self.videoStreamingEnabled.enable = True
			self.HttpServerEnabled.enable = False
			self.VideoStreamingEnabled(Globals.enableVideoStreaming)
	def VideoStreamingEnabled ( self, val ):
		if self.HttpServerEnabled.value and (self.wlan0 or self.eth0):
			self.stream.recording = val
			Globals.enableVideoStreaming = val
	def StreamingEnabled ( self, val ):
		# NOT WORKING!  A thread issue
		#if self.eth0 or self.wlan0:
			#self.stream.enable = val
		pass
	'''
	Basic tab - Camera programming functions
	'''
	def BrightnessChanged ( self, val ):
		self.camera.brightness = int(float(val))
		Globals.defaultBrightness = int(float(val))
	def ContrastChanged ( self, val ):
		self.camera.contrast = int(float(val))
		Globals.defaultContrast = int(float(val))
	def SaturationChanged ( self, val ):
		self.camera.saturation = int(float(val))
		Globals.defaultSaturation = int(float(val))
	def SharpnessChanged ( self, val ):
		self.camera.sharpness = int(float(val))
		Globals.defaultSharpness = int(float(val))
	def AlphaChanged ( self, val ):
		self.camera.preview.alpha = int(float(val))
		Globals.defaultAlpha = int(float(val))
	def ResolutionChanged ( self, val ):
		recording = True
		try:
			recording = self.stream.recording
			self.stream.recording = False
		except:	pass
		s = val.split(':') # text string like --> 'CGA: (320x200)'
		s1 = s[1].replace('(','').replace(')','').strip().split('x')
		self.camera.resolution = (int(s1[0]),int(s1[1]))
		Globals.defaultResolution = self.resolution.value
		try:	self.stream.recording = recording
		except:	pass
	'''
	Advanced options tab
	'''
	def ToggleUseStillPort ( self, val ):
		Globals.useVideoPort = val
	def ToggleImageDenoise ( self, val ):
		self.camera.image_denoise = val
		Globals.imageDenoise = val
	def ToggleVideoDenoise ( self, val ):
		self.camera.video_denoise = val
		Globals.videoDenoise = val
	def ToggleVideoStabilization ( self, val ):
		self.camera.video_stabilization = val
		Globals.videoStabilization = val
	def MeterModeChanged ( self, val ):
		Globals.meteringMode = val
		self.camera.meter_mode = ['average','spot','backlit','matrix'][val]
	def ExposureCompChanged ( self, val ):
		self.camera.exposure_compensation = val
		Globals.exposureCompensation = val
		if val == 0: t = self.language.GetText('None')
		else: t = '%.1f fstops' % (float(val) / 6.0)
		self.exposureComp.text = '%s' % t
	def DRCStrengthChanged ( self, val ):
		Globals.drcStrength = val
		self.camera.drc_strength = ['off','low','medium','high'][val]

		#revision (of camera)
		#sensor_mode
		#shutter_speed
		#exposure_speed
		#exposure_mode			PiCamera.EXPOSURE_MODES
		#iso
		#framerate
		#digital_gain
		#analog_gain
		#awb_mode				PiCamera.AWB_MODES
		#awb_gains				(red,blue as fractions)
	'''
	Start of Photo timelapse functions
	'''
	def PhotoParamSanityCheck ( self ):
		self.StoppedPhotoTimelapse()
		self.UpdatePhotoParams()
	def UpdatePhotoParams ( self ):
		self.photoCount = 0
		i = Globals.defaultStopPictureCountType
		if i != 0: 	 # end time
			delta = [1,60,3600,3600*24][i-1] * Globals.defaultStopPictureCount
			self.photoEnd = dt.datetime.now() + dt.timedelta(seconds=delta)
		self.delayBetweenPhoto = (
			[1,60,3600,3600*24][Globals.defaultTakePictureCountType] *
			Globals.defaultTakePictureCount * 1000 )
		self.phototimedelta = dt.timedelta(milliseconds=self.delayBetweenPhoto)
		self.PhotoStatusUpdate()
	def PhotoStatusUpdate ( self ):
		text = '%s: %d ' % (self.language.GetText('Photos').replace('s',''),self.photoCount)
		if Globals.defaultStopPictureCountType == 0:
			text = text + '%s %d' % (self.language.GetText('of'),Globals.defaultStopPictureCount)
		else:
			try:
				t = self.photoEnd.strftime('%m/%e/%y %I:%M:%S %p')
				text = text + '\n%s %s' % ( self.language.GetText('Ending on'), t )
			except:	text = self.language.GetText('Bad Format!')
		self.photoLabel.config(text = text)
	def TakePictureEveryChanged ( self, val ):
		Globals.defaultTakePictureCount = int(float(val))
		self.PhotoParamSanityCheck()
	def WhenToTakePictureChanged ( self, val ):
		Globals.defaultTakePictureCountType = int(float(val))
		self.PhotoParamSanityCheck()
	def StopPictureCountChanged ( self, val ):
		Globals.defaultStopPictureCount = int(float(val))
		self.PhotoParamSanityCheck()
	def WhenToStopPictureChanged ( self, val ):
		Globals.defaultStopPictureCountType = int(float(val))
		self.PhotoParamSanityCheck()
	def StartPhotoTimelapse ( self, val ):
		if not self.startPhotoTimelapse.value: 
			self.startPhotoTimelapse.enable = False
			self.StoppedPhotoTimelapse()
			self.after(1000,self.EnablePhotoTimelapseButton)
		else:
			# Determine self.photoEnd based on whether it's a picture count
			# or a delta time
			self.UpdatePhotoParams()
			self.after(10,self.TakeTimelapsePhoto)
	def EnablePhotoTimelapseButton ( self ):
		self.startPhotoTimelapse.enable = True
	def TakeTimelapsePhoto ( self ):
		# Time this so we know how much to subtract from the
		if not self.startPhotoTimelapse.value: 
			self.StoppedPhotoTimelapse()
			return
		self.photoCount = self.photoCount + 1
		now = dt.datetime.now()
		filename = ( Globals.defaulttimelapsephotodir + '/' +
						 Globals.defaultphotoname +
						 str(self.photoCount) + '_' +
						 now.strftime(Globals.defaulttimestampformat) +
						 '.' + Globals.defaultphotoformat )
		self.CapturePhoto(filename)
		self.PhotoStatusUpdate()
		self.nextPhoto = now + dt.timedelta(milliseconds=self.delayBetweenPhoto)
		if Globals.defaultStopPictureCountType == 0:	# picture count
			if self.photoCount > Globals.defaultStopPictureCount:
				self.StoppedPhotoTimelapse()
				return
		elif self.nextPhoto > self.photoEnd:
			self.StoppedPhotoTimelapse()
			return
		self.after(1000,self.CheckIfPhotoTimelapseIsStillEnabled)
	def CheckIfPhotoTimelapseIsStillEnabled ( self ):
		if not self.startPhotoTimelapse.value: return
		if dt.datetime.now() >= self.nextPhoto:
			self.after(10,self.TakeTimelapsePhoto)
		else: self.after(1000,self.CheckIfPhotoTimelapseIsStillEnabled)
	def StoppedPhotoTimelapse ( self ):
		self.startPhotoTimelapse.value = False
		self.photoLabel.config(text = "Stopped/Finished\n%d photos taken"%self.photoCount)
	'''
	Start of Video timelapse functions
	'''
	def VideoParamSanityCheck ( self ):
		self.StoppedVideoTimelapse()
		self.UpdateVideoParams()
	def UpdateVideoParams ( self ):
		self.videoCount = 0
		i = Globals.defaultStopVideoCountType
		if i != 0: 	 # end time
			delta = [1,60,3600,3600*24][i-1] * Globals.defaultStopVideoCount
			self.videoEnd = dt.datetime.now() + dt.timedelta(seconds=delta)
		self.delayBetweenVideo = (
			[1,60,3600,3600*24][Globals.defaultTakeVideoCountType] *
			Globals.defaultTakeVideoCount )
		self.videoRunLength = (
			[1,60][Globals.defaultVideoLengthType] * Globals.defaultVideoLength)
		self.VideoStatusUpdate()
	def VideoStatusUpdate ( self ):
		text = '%s: %d ' % (self.language.GetText('Videos').replace('s',''),
					self.videoCount)
		if Globals.defaultStopVideoCountType == 0:
			text = text + '%s %d' % (self.language.GetText('of'),
				Globals.defaultStopVideoCount)
		else:
			try:
				t = self.videoEnd.strftime('%m/%e/%y %I:%M:%S %p')
				text = text + '\n%s %s' % ( self.language.GetText('Ending on'), t )
			except:	text = self.language.GetText('Bad Format!')
		self.videoLabel.config(text = text)
	def StartVideoTimelapse ( self, val ):
		if self.VideoInProgress: return		# High level
		if not self.startVideoTimelapse.value:
			self.StoppedVideoTimelapse()
			return
		self.UpdateVideoParams()
		self.after(10,self.TakeTimelapseVideo) 	# Start video
	def TakeTimelapseVideo ( self ):
		if not self.startVideoTimelapse.value:
			self.StoppedVideoTimelapse()
			return
		self.videoCount = self.videoCount + 1
		now = dt.datetime.now()
		filename = ( Globals.defaulttimelapsevideodir + '/' +
						 Globals.defaultvideoname +
						 str(self.videoCount) + '_' +
						 now.strftime(Globals.defaulttimestampformat) +
						 '.' + Globals.defaultvideoformat )
		self.camera.start_recording(filename)
		self.resolution.grid_remove()		# Hide resolution - could disable instead?
		self.setResolutionLabel.grid_remove()
		self.endVideoRecording = now + dt.timedelta(seconds=self.videoRunLength)
		self.after(1000,self.CheckDuringVideoRecording)
		self.blinkVideo = True
		self.after(1000,self.BlinkVideoNew)
	def CheckDuringVideoRecording ( self ):
		if not self.startVideoTimelapse.value:
			self.StoppedVideoTimelapse()
		else:
			now = dt.datetime.now() 
			if now >= self.endVideoRecording:
				if self.camera.recording:
					self.camera.stop_recording()
				self.VideoStatusUpdate()
				self.blinkVideo = False
				self.nextVideo = now + dt.timedelta(seconds=self.delayBetweenVideo)
				# Now setup to delay until next recording should start
				if Globals.defaultStopVideoCountType == 0:
					if self.videoCount > Globals.defaultStopVideoCount:
						self.StoppedVideoTimelapse()
						return;
				elif self.nextVideo > self.videoEnd:
					self.StoppedVideoTimelapse()
					return;
				self.after(1000,self.CheckIfVideoTimelapseIsStillEnabled)
			else:
				self.after(1000,self.CheckDuringVideoRecording)
	def CheckIfVideoTimelapseIsStillEnabled ( self ):
		if not self.startVideoTimelapse.value: 
			self.StoppedVideoTimelapse()
			return
		if dt.datetime.now() >= self.nextVideo:
			self.after(10,self.TakeTimelapseVideo)
		else: self.after(1000,self.CheckIfVideoTimelapseIsStillEnabled)
	def StoppedVideoTimelapse ( self ):
		if self.camera.recording:
			self.camera.stop_recording()
		self.startVideoTimelapse.value = False
		self.blinkVideo = False
		self.BlinkVideoNew()
		self.videoLabel.config(text = "Stopped/Finished\n%d videos taken"%self.videoCount)
		self.resolution.grid()
		self.setResolutionLabel.grid()
	def BlinkVideoNew ( self ):
		try:
			if self.blinkVideo:
				if not self.InOptions:
					if self.VideoStartOverlay.layer == 5:
						self.VideoStartOverlay.layer = 3
						self.VideoOverlay.layer = 5
					else:	# default
						self.VideoStartOverlay.layer = 5
						self.VideoOverlay.layer = 3
				self.after(1000,self.BlinkVideoNew)
			elif not self.InOptions:
				self.VideoStartOverlay.layer = 3
				self.VideoOverlay.layer = 5
		except: pass
	def TakeVideoEveryChanged ( self, val ):
		Globals.defaultTakeVideoCount = int(float(val))
		self.VideoParamSanityCheck()
	def WhenToTakeVideoChanged ( self, val ):
		Globals.defaultTakeVideoCountType = int(float(val))
		self.VideoParamSanityCheck()
	def VideoLengthChanged ( self, val ):
		Globals.defaultVideoLength = int(float(val))
		self.VideoParamSanityCheck()
	def VideoLengthTypeChanged ( self, val ):
		Globals.defaultVideoLengthType = int(float(val))
		self.VideoParamSanityCheck()
	def StopVideoCountChanged ( self, val ):
		Globals.defaultStopVideoCount = int(float(val))
		self.VideoParamSanityCheck()
	def WhenToStopVideoChanged ( self, val ):
		Globals.defaultStopVideoCountType = int(float(val))
		self.VideoParamSanityCheck()
	'''
	Select save directories for photos and videos
	'''
	def GetDirectory ( self ):
		self.camera.stop_preview()
		directory = FileDialog.askdirectory()
		self.preview = self.camera.start_preview(alpha=self.alpha.value,
			fullscreen=False,
			window=(int(self.width/2 + 25),0,int(self.width/2-25),self.height))
		return directory
	def SelectPhotoDirectory ( self ):
		directory = self.GetDirectory()
		if directory:
			Globals.defaultphotodir = directory
			self.photoDirLabel.config(text=directory)
	def SelectVideoDirectory ( self ):
		directory = self.GetDirectory()
		if directory:
			Globals.defaultvideodir = directory
			self.videoDirLabel.config(text=directory)
	def SelectTimelapsePhotoDirectory ( self ):
		directory = self.GetDirectory()
		if directory:
			Globals.defaulttimelapsephotodir = directory
			self.timelapsephotoDirLabel.config(text=directory)
	def SelectTimelapseVideoDirectory ( self ):
		directory = self.GetDirectory()
		if directory:
			Globals.defaulttimelapsevideodir = directory
			self.timelapsevideoDirLabel.config(text=directory)
	'''
	These functions deal with annotation overlays. Frame, Timestamp, and
	and background colors. These colors are variable between black through
	all gray levels, to white.
	TODO - add text annotation.
	'''
	def AnnotateForegroundColorChanged ( self, val ):	# val ranges from 0 to 100
		self.camera.annotate_foreground = picamera.Color(y=float(val)/100.0, u=0, v=0)
		Globals.annotateForegroundColor = val
	def EnableTransparentBackgroundColor ( self, val ):
		if val:	self.camera.annotate_background = None
		else:	self.camera.annotate_background = (
			picamera.Color(y=float(self.annotateBackgroundColor.value)/100.0, u=0, v=0) )
		Globals.transparantBackgroundEnabled = val
	def AnnotateBackgroundColorChanged ( self, val ):	# Change white to black only
		if not Globals.transparantBackgroundEnabled:
			self.camera.annotate_background = picamera.Color(y=float(val)/100.0, u=0, v=0)
		Globals.annotateBackgroundColor = val
	def AnnotateSizeChanged ( self, val ):
		Globals.defaultAnnotateTextsize = val
		self.camera.annotate_text_size = val
	def ToggleAnnotateFrameNum ( self, val ):
		if not Globals.timestampEnabled:	self.camera.annotate_text = ''
		self.camera.annotate_frame_num = val
		Globals.framerateEnabled = val
	def ToggleTimestamp ( self, val ):
		Globals.timestampEnabled = val
		self.after(10,self.UpdateTimestamp())
	def UpdateTimestamp ( self ):
		if Globals.timestampEnabled or len(self.identify) > 0:
			t = self.identify
			if Globals.timestampEnabled:
				try:	t = t + dt.datetime.now().strftime(Globals.defaulttimestampformat)
				except:	t = t + self.language.GetText('Bad Format!') # Should never get here...
			self.camera.annotate_text = t
			self.after(1000,self.UpdateTimestamp)
		else:	self.camera.annotate_text = ''
	def IdentifyTextChanged ( self, value ):
		if value == 0:
			self.identify = ""
		else:
			if value == 1:
				self.identify = Globals.headingLevel1
			else: 
				self.identify = Globals.headingLevel2
			self.after(10,self.UpdateTimestamp())
		print(value,'Identify text=',self.identify)
	'''
	Generic helper function to pad image to the correct boundary
	'''
	def GetImage ( self, image ):
		img = PIL.Image.open(image)
		self.imageSize = img.size
		image = PIL.Image.new('RGBA', (
			((img.size[0] + 31) // 32) * 32,
			((img.size[1] + 15) // 16) * 16,
			))
		image.paste(img, (0, 0),img)
		return image
	'''
	Bring up the options screen. Called by main button on screen
	'''
	def Options ( self ):
		self.InOptions = True
		self.RemoveOverlays()
		self.ShowHideButtons(False)
		self.preview.fullscreen = False;
		self.after(100,self.UpdatePreview)	# wait for things to settle
	'''
	User pressed the Done button on the options screen. Return to full screen
	'''
	def DoneOptions ( self ):
		self.InOptions = False
		self.ShowHideButtons(True)
		self.preview.fullscreen = True;
		self.AddOverlays()
	'''
	Direct capture of an image to a file. Called by main button on screen
	'''
	def TakePhoto ( self ):
		filename = ( Globals.defaultphotodir + '/' + Globals.defaultphotoname +
						 dt.datetime.now().
						 strftime(Globals.defaulttimestampformat) +
						 '.' + Globals.defaultphotoformat )
		self.CapturePhoto(filename)
	'''
	Direct capture of an image to a file.
	Called by Timelapse and TakePhoto
	'''
	def CapturePhoto ( self, filename ):
		if not self.InOptions:
			self.TakePhotoOverlay.layer = 5
			self.PhotoOverlay.layer = 0
		self.camera.capture(filename,use_video_port=Globals.useVideoPort)
		if not self.InOptions:
			self.TakePhotoOverlay.layer = 0
			self.PhotoOverlay.layer = 5
	'''
	Start/stop video capture to a file. While capture is in progress,
	blink the video image. Note that video capture is ignored if
	the resoltuion is greater than 1920x1080. If Timelapse video capture
	in progress, then we need to ignore any user presses?
	'''
	def Video ( self ):
		if self.startVideoTimelapse.value: return	# Timelapse is ON!!
		if self.VideoInProgress:	# Now stop video
			if self.camera.recording:
				try:	self.camera.stop_recording()		# and save to filename
				except:	pass
			self.VideoStartOverlay.layer = 3
			self.VideoOverlay.layer = 5
			self.resolution.grid() # Restore it
			self.setResolutionLabel.grid()
		else:	# Start video
			# Check to make sure we're <= 1920 x 1080
			if self.resolution.value > 18:	return
			self.start = time.time()
			filename = ( Globals.defaultvideodir + '/' + Globals.defaultvideoname +
							 dt.datetime.now().
							 strftime(Globals.defaulttimestampformat) +
							 '.' + Globals.defaultvideoformat )
			self.camera.start_recording(filename)
			self.resolution.grid_remove()	# Hide resolution - could disable instead?
			self.setResolutionLabel.grid_remove()
			self.after(10,self.BlinkVideo)	# Call AFTER setting videoInProgress
		self.VideoInProgress = not self.VideoInProgress
	def BlinkVideo ( self ):
		if self.VideoInProgress:
			if ( Globals.defaultVideoTimeout != 0 and
				  time.time() - self.start >= Globals.defaultVideoTimeout ):
				self.Video()	# Halt this run
				return
			if not self.InOptions:
				if self.VideoStartOverlay.layer == 5:
					self.VideoStartOverlay.layer = 3
					self.VideoOverlay.layer = 5
				else:
					self.VideoStartOverlay.layer = 5
					self.VideoOverlay.layer = 3
			self.after(1000,self.BlinkVideo)
	'''
	Place the overlay images on the screen. Everything is based off
	the size of the overlay images and the locations of the buttons
	that reside underneath.
	'''
	def AddOverlays ( self ):
		w = self.imageSize[0]
		h = self.imageSize[1]
		locy = int(self.height-120)
		self.CloseOverlay = self.camera.add_overlay(self.CloseImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=5,
			fullscreen=False,window=(self.xList[0],locy,w,h))
		self.OptionsOverlay = self.camera.add_overlay(self.OptionsImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=5,
			fullscreen=False,window=(self.xList[1],locy,w,h))
		self.PhotoOverlay = self.camera.add_overlay(self.PhotoImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=5,
			fullscreen=False,window=(self.xList[2],locy,w,h))
		self.TakePhotoOverlay = self.camera.add_overlay(self.TakePhotoImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=3,
			fullscreen=False,window=(self.xList[2],locy,w,h))
		self.VideoOverlay = self.camera.add_overlay(self.StartVideoImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=5,
			fullscreen=False,window=(self.xList[3],locy,w,h))
		self.VideoStartOverlay = self.camera.add_overlay(self.StopVideoImg.tobytes(),
			size=self.CloseImg.size,format='rgba',layer=3,
			fullscreen=False,window=(self.xList[3],locy,w,h))
	def RemoveOverlays ( self ):
		for i in range(len(self.camera.overlays)-1,-1,-1):
			self.camera.remove_overlay(self.camera.overlays[i])
	'''
	Generic procedure to show/hide all of the controls under the
	preview window.
	'''
	def ShowHideButtons (self, hide ):
		if hide:
			self.mainFrame.grid_remove()
			self.close.lift(self.back)
			self.options.lift(self.back)
			self.photo.lift(self.back)
			self.video.lift(self.back)
		else:
			self.mainFrame.grid()
			self.close.lower(self.back)
			self.options.lower(self.back)
			self.photo.lower(self.back)
			self.video.lower(self.back)

	def LanguageChanged ( self, val ):
		self.language.LanguageChanged(self.root,val)
		self.after(100,self.UpdatePreview)	# wait for things to settle
	'''
	Adjust the size of the preview window based on the size of the
	main options notebook self.MainNotebook
	'''
	def UpdatePreview ( self ):
		width = self.MainNotebook.winfo_width()
		self.camera.preview.window = (width+5,0,self.width-width-5,self.height)
	'''
	User pressed the 'X' close button on the screen. Exit the program.
	'''
	def Close ( self ):
		self.camera.stop_preview()
		#QuitDialog(self,title="Quit "+appTitle,okonly=False)
		if MessageBox.askyesno("Quit %s"%appTitle,"Exit the %s program?"%appTitle):
			if self.stream:	self.stream.StopStream()
			self.master.destroy()
		else:
			self.preview = self.camera.start_preview(alpha=self.alpha.value,
								fullscreen=True)

'''
The main function.  Load preferrences and the language dictionary,
start the camera, setup Tk and the main window, then enter the mainloop
until the program terminates. At that point save preferences.
'''
def Run_microVIEW():
	INIfile = "%s.INI" % appTitle
	LoadPreferences(INIfile)	# First thing to do!

	language = LanguageSupport("%s.language" % appTitle)	# Second thing to do!

	microVIEWApp = Tk()

	'''
	Change the theme for microView. Use larger buttons and text
	and change the foreground and background colors.
	TODO: Add TButton, TLabel, TFrame - but this changes ALL dialogs
	when this program is running.
	'''
	style = ttk.Style()
	style.theme_create( appTitle, parent="clam", settings= {
		#"TFrame" : {	# ALL Frames are affected!
			#"configure" : {
				#"background" : Globals.defaultBackgroundColor,
				#"foreground" : Globals.defaultBackgroundColor }, },
		#"TButton" : {	# ALL Buttons are affected!
			#"configure" : {
				#"background" : Globals.defaultBackgroundColor,
				#"font" : Globals.defaultFont,
				#"foreground" : Globals.buttontextcolor }, },
		#"TLabelframe" : {
			#"configure" : {
				#"foreground" : "white",
				#"font" : Globals.defaultFont,
				#"background" : '#303030' }, }, #Globals.defaultBackgroundColor }, },
		#"TLabelframe.label" : {
			#"configure" : {
				#"background" : Globals.defaultBackgroundColor,
				#"foreground" : "white",
				#"font" : Globals.defaultFont }, },
		"TNotebook" : {
			"configure": {
				"tabmargins": [2, 5, 2, 0],
				"background" : Globals.defaultBackgroundColor }, },
		"TNotebook.Tab" : {
			"configure": {
				"padding": [20, 15],	# bigger tabs
				"background" : Globals.buttonbackcolor,
				"foreground" : Globals.buttontextcolor,
				"font" : Globals.defaultFont }, }, } )
	style.theme_use(appTitle)

	try:
		camera = picamera.PiCamera(sensor_mode=1)	# leftover bug(?) fix
		camera.sensor_mode = 0	# go back to auto mode

		width = microVIEWApp.winfo_screenwidth()
		height = microVIEWApp.winfo_screenheight()
		microVIEWApp.attributes("-fullscreen", True)	# FIXED!
		microVIEWApp.configure(background = Globals.defaultBackgroundColor)
		microVIEW(microVIEWApp,camera,language,appTitle,width,height)
		microVIEWApp.mainloop()
	finally:
		camera.close()

	SavePreferences(INIfile,False)		# Last thing to do!

'''
Python will look for __main__ to start execution. If not here, then the
first non-function code is executed.

TODO
	Add capability to read arguments:
		e.g. INI filename, Language filename, Default language (overrides
				the INI file, full screen or not... etc
'''
if __name__ == '__main__':
	Run_microVIEW()
