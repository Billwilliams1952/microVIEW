#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  Languages.py
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
import sys
import os
import subprocess

# Big changes between the two
if sys.version_info[0] == 3:
	import configparser as ConfigParser		# Python 3.x
else:
	import ConfigParser as ConfigParser		# Python 2.X

from ConfigFile	import UpdateConfigValue, SaveConfigFile
from Globals	import *

'''
	TODO:
	Support getting a series of strings.
	Pass "The value is".
			Split into words, lookup each one and return a concatentated string.
			Not sure if this will work across all languages, (The word may change
			depending on context).
'''

class LanguageSupport:
	def __init__ ( self, languageFilename ):
		self.filename = languageFilename
		self.config = ConfigParser.SafeConfigParser()
		self.config.read(self.filename)

		if not self.config.sections():
			# Create a microVIEW.language file with just the English.
			default = 'English'
			print (self.filename + " does not exist - creating file")
			if Python2:	self.config.add_section(default)
			else:		self.config[default] = {}

			section = default

			UpdateConfigValue ( self.config, section, 'basic', 'Basic' )
			UpdateConfigValue ( self.config, section, 'brightness', 'Brightness' )
			UpdateConfigValue ( self.config, section, 'contrast', 'Constrast' )
			UpdateConfigValue ( self.config, section, 'saturation', 'Saturation' )
			UpdateConfigValue ( self.config, section, 'sharpness', 'Sharpness' )
			UpdateConfigValue ( self.config, section, 'transparancy', 'Transparancy' )
			UpdateConfigValue ( self.config, section, 'setresolution', 'Set resolution for images and videos' )
			UpdateConfigValue ( self.config, section, 'advanced', 'Advanced' )
			UpdateConfigValue ( self.config, section, 'timelapse', 'Time-lapse' )
			UpdateConfigValue ( self.config, section, 'preferences', 'Preferences' )
			UpdateConfigValue ( self.config, section, 'camera', 'Camera' )
			UpdateConfigValue ( self.config, section, 'annotate', 'Annotate' )
			UpdateConfigValue ( self.config, section, 'photos', 'Photos' )
			UpdateConfigValue ( self.config, section, 'videos', 'Videos' )
			UpdateConfigValue ( self.config, section, 'general', 'General' )
			UpdateConfigValue ( self.config, section, 'interface', 'Interface' )
			UpdateConfigValue ( self.config, section, 'files', 'Files' )
			UpdateConfigValue ( self.config, section, 'network', 'Network' )
			UpdateConfigValue ( self.config, section, 'selectlanguage', 'Select language:' )
			UpdateConfigValue ( self.config, section, 'on', 'ON' )
			UpdateConfigValue ( self.config, section, 'off', 'OFF' )
			UpdateConfigValue ( self.config, section, 'donewithoptions', 'Done with options' )
			UpdateConfigValue ( self.config, section, 'badformat', 'Bad format!' )
			UpdateConfigValue ( self.config, section, 'photodirectory', 'Photo directory' )
			UpdateConfigValue ( self.config, section, 'videodirectory', 'Video directory' )
			UpdateConfigValue ( self.config, section, 'usevideoport', 'Use Video port' )
			UpdateConfigValue ( self.config, section, 'videostabilization', 'Video Stabilization' )
			UpdateConfigValue ( self.config, section, 'imagedenoise', 'Image Denoise' )
			UpdateConfigValue ( self.config, section, 'videodenoise', 'Video Denoise' )
			UpdateConfigValue ( self.config, section, 'meteringmode', 'Metering Mode:' )
			UpdateConfigValue ( self.config, section, 'matrix', 'matrix' )
			UpdateConfigValue ( self.config, section, 'average', 'average' )
			UpdateConfigValue ( self.config, section, 'spot', 'spot' )
			UpdateConfigValue ( self.config, section, 'backlit', 'backlit' )
			UpdateConfigValue ( self.config, section, 'dynamicrangecompression', 'Dynamic Range\nCompression:' )
			UpdateConfigValue ( self.config, section, 'none', 'None (Off)' )
			UpdateConfigValue ( self.config, section, 'low', 'Low' )
			UpdateConfigValue ( self.config, section, 'medium', 'Medium' )
			UpdateConfigValue ( self.config, section, 'high', 'High' )
			UpdateConfigValue ( self.config, section, 'exposure', 'Exposure\nCompensation:' )
			UpdateConfigValue ( self.config, section, 'timestamp', 'Time-Stamp' )
			UpdateConfigValue ( self.config, section, 'framenumber', 'Frame Number' )
			UpdateConfigValue ( self.config, section, 'annotatetextsize', 'Annotate Text Size' )
			UpdateConfigValue ( self.config, section, 'transparantbackground', 'Transparant background' )
			UpdateConfigValue ( self.config, section, 'backgroundcolor', 'Background Color' )
			UpdateConfigValue ( self.config, section, 'foregroundcolor', 'Foreground Color' )
			UpdateConfigValue ( self.config, section, 'takepictureevery', 'Take Picture every' )
			UpdateConfigValue ( self.config, section, 'stopafter', 'Stop after' )
			UpdateConfigValue ( self.config, section, 'seconds', 'seconds' )
			UpdateConfigValue ( self.config, section, 'minutes', 'minutes' )
			UpdateConfigValue ( self.config, section, 'hours', 'hours' )
			UpdateConfigValue ( self.config, section, 'days', 'days' )
			UpdateConfigValue ( self.config, section, 'pictures', 'pictures' )
			UpdateConfigValue ( self.config, section, 'capturevideoevery', 'Capture Video every' )
			UpdateConfigValue ( self.config, section, 'videoLength', 'Video length' )
			UpdateConfigValue ( self.config, section, 'httpserverenabled', 'HTTP server enabled' )
			UpdateConfigValue ( self.config, section, 'videostream', 'Video stream' )
			UpdateConfigValue ( self.config, section, 'of', 'of' )
			UpdateConfigValue ( self.config, section, 'endingon', 'Ending on' )

			SaveConfigFile(self.filename, self.config )

	def GetText ( self, item ):
		Python2 = sys.version_info[0] == 2
		# This seems to work ok. Do I need the fake 'a', 'a' translate table?
		# Consider a regex instead.
		litem = ( item.lower().translate(
			str.maketrans('a','a',' \n\t:;,.\'"[]{}()%$#@!?><|\\/*+=-')) )
		try:
			if Python2:	val = self.config.get(Globals.defaultLanguage,litem)
			else:		val = self.config[Globals.defaultLanguage][litem]
		except:	# An error - return the default English word/phrase
			try:
				if Python2:	val = self.config.get('English',litem)
				else:		val = self.config['English'][litem]
			except:		# The phrase is not in any dictionary. return the 'item'
				val = item
		# Now see if the text is of the form 'file=\pathname\textfilename'
		# If yes, attempt to open the file, read the text, format as one
		# string, and return it.
		strs = val.split('=',1)
		if len(strs) == 2 and strs[0].strip().lower() == 'file':
			text = ''
			try:
				with open(strs[1].strip(),'r') as f: 
					text = f.read().replace('\n','')
			except IOError: text = item
			return text.replace('\\n','\n')
		else: 
			return val.replace('\\n','\n')
	'''
	The user specified a new language. Update all of the text strings
	throughout the program. This could get REALLY long. Perhaps we need
	to think this out a bit:
		Each of my controls 'knows' to use the text returned by GetText. So
		just pass text='Text' as before. Internally, each control will
		actually use self.language.GetText(text). Add a UpdateLang method
		that when called, forces the control to repaint with new text. Need
		to pass language=self.language also.

		For other widgets, we can subclass them to add the LangChanged
		method. We would also need to capture the text='text' and replace
		it with text=self.language.GetText('text'). Need to pass
		language=self.language also.

		Then just loop through all widgets and call LangChanged. If an
		exception, just ignore it (a control I didn't subclass)

		What about strings? They would all just GetText to get the actual
		string anyway.  May have to call some methods to force an update
		to the display.
	'''
	def RecurseChildren ( self, currentControl ):
		try:		currentControl.UpdateLang()
		except:	pass
		childList = currentControl.winfo_children()
		if not childList: return
		for child in childList:
			self.RecurseChildren(child)
	def LanguageChanged ( self, root, val ):
		Globals.defaultLanguage = self.config.sections()[val]
		self.RecurseChildren(root)
		root.update_idletasks()
	@property
	def sections ( self ):
		return self.config.sections()

