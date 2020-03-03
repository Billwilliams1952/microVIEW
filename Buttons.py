#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#  Buttons.py
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

from Globals		import *

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
		raise ("\n\n**** ImageTk not installed. ****" \
				 "**** Use: sudo apt-get install python3-pil.imagetk ****")
else:
	from	Tkinter import *	# Python 2.X
	import 	tkFileDialog as FileDialog
	import 	tkMessageBox as MessageBox
	import 	ttk
	from 	ttk import *
	import 	tkFont
	from	PIL import ImageTk

class LangButton ( ttk.Button ):
	def __init__(self,parent,*args,**kargs):
		try:
			self.lang = kargs['language']
			del kargs['language']
		except: self.lang = None
		try:
			self._text = kargs['text']
		except: self._text = ''
		ttk.Button.__init__(self,parent,*args,**kargs)
		self.UpdateLang()
	def UpdateLang ( self ):
		if self.lang:
			self.config(text=self.lang.GetText(self._text))

class LangLabelFrame ( ttk.Frame ):
	def __init__(self,parent,*args,**kargs):
		try:
			self.lang = kargs['language']
			del kargs['language']
		except: self.lang = None
		try:
			self._text = kargs['text']
			del kargs['text']
		except:	self._text = ''
		ttk.Frame.__init__(self,parent,*args,**kargs)
		self.config(style='Shaded.TFrame')
		self.UpdateLang()
	def UpdateLang ( self ):
		#if self.lang:
			#self._text = self.lang.GetText(self['text'])
		pass

class LangNotebook ( ttk.Notebook ):
	def __init__(self,parent,*args,**kargs):
		try:
			self.lang = kargs['language']
			del kargs['language']
		except: self.lang = None
		ttk.Notebook.__init__(self,parent,*args,**kargs)
		self._init = True
	def UpdateTabs ( self ):	# in case we add/remove tabs
		self._init = True
		self.UpdateLang()
	def UpdateLang ( self ):
		if self._init:		# Save strings for each tab in local copy
			self._numTabs = self.index("end")
			self._text = []
			for index in range(self._numTabs):
				self._text.append(self.tab(index,option='text'))
		self._init = False
		if self.lang:
			for index in range(self._numTabs):
				self.tab(index, text=self.lang.GetText(self._text[index]))

class LangLabel ( ttk.Label ):
	def __init__(self,parent,*args,**kargs):
		try:
			self.lang = kargs['language']
			del kargs['language']
		except: self.lang = None
		try:
			self._text = kargs['text']
		except: self._text = ''
		super().__init__(parent,*args,**kargs)
		self.config(style='Label.TLabel')
		self.UpdateLang()
	def config ( self, **kargs ):
		super().config(**kargs)
		try:
			self._text = kargs['text']
			super().config(text=self.lang.GetText(self._text))
		except: pass
	def UpdateLang ( self ):
		if self.lang:
			super().config(text=self.lang.GetText(self._text))

class MultiTouchButton ( ttk.Frame ):
	def __init__(self,parent,*args,**kargs):
		ttk.Frame.__init__(self,parent)
		self.config(style='F.TFrame')
		self._parent = parent
		try:		self._callback = kargs['callback']
		except:	self._callback = None
		try:		self.lang = kargs['language']
		except:	self.lang = None
		self._text = kargs['text']
		if ( isinstance(self._text,list) and
			  isinstance(self._text[0],str) ):	# only string lists please
			self._maxVal = len(self._text) - 1
		else: raise ValueError("'text' must be a list of strings")
		try:		self._width = int(kargs['width'])
		except:	self._width = 50
		try:		self._height = int(kargs['height'])
		except:	self._height = Globals.defaultButtonHeight
		self._value = min(self._maxVal, max(0, int(kargs['value'])))
		self._canvas = Canvas(self,width=self._width,height=self._height,
			background=Globals.buttonbackcolor)
		self._canvas.grid(row=0,column=0)
		self._canvas.bind('<Button-1>',self.Pressed)
		self._canvas.bind('<ButtonRelease-1>',self.Released)
		self._textArea = self._canvas.create_text((int(self._width/2),
			int(self._height/2)),font=Globals.defaultFont,
			fill=Globals.buttontextcolor,text='')
		self.DrawText()
	def Pressed ( self, event ):
		self._canvas.config(background=Globals.buttonpressedcolor)
		self._canvas.itemconfig(self._textArea,fill=Globals.buttonpressedtextcolor)
	def Released ( self, event ):
		self._value = self._value + 1
		if self._value > self._maxVal: self._value = 0
		self._canvas.config(background=Globals.buttonbackcolor)
		self.DrawText()
		if self._callback:
			self._callback(self._value)
	@property
	def value ( self ):
		return self._value
	@value.setter
	def value ( self, val ):
		self._value = min(self._maxVal, max(0, int(val)))
		self.DrawText()
	def DrawText ( self ):
		if self.lang:	txt = self.lang.GetText(self._text[self._value])
		else:	txt = self._text[self._value]
		self._canvas.itemconfig(self._textArea,fill=Globals.buttontextcolor,
			text=txt)
	def UpdateLang ( self ):
		self.DrawText()

class PushButton ( ttk.Frame ):
	def __init__(self,parent,*args,**kargs):
		'''
		Add list of tuples - [('text',value),('text',value),...]
		list[i][0] = text list[i][1] = value
		immutable values....
		'''
		ttk.Frame.__init__(self,parent)
		self.config(style='FA.TFrame')
		self._parent = parent
		try:		self._callback = kargs['callback']
		except:	self._callback = None
		try:		self.lang = kargs['language']
		except:	self.lang = None
		self._text = kargs['text']		# a list with two values for OFF/ON
		try:		self._state = bool(kargs['value'])
		except:	self._state = False
		try:		self._width = int(kargs['width'])
		except:	self._width = 50
		try:		self._height = int(kargs['height'])
		except:	self._height = Globals.defaultButtonHeight

		self._enabled = True
		self._canvas = Canvas(self,width=self._width,height=self._height,
			background=Globals.defaultBackgroundColor,
			highlightbackground=Globals.defaultBackgroundColor,
			borderwidth=0)
		self._canvas.grid(row=0,column=0)
		self._canvas.bind('<Button-1>',self.Pressed)
		self._canvas.bind('<ButtonRelease-1>',self.Released)
		self._circle = self._canvas.create_oval(0, 0, self._width, self._height)
		self._textArea = self._canvas.create_text((int(self._width/2),
			int(self._height/2)),font=Globals.defaultFont)
		self._buttonText = ''	# Hack to allow other text for buttons
		self.DrawText()
		#if self._callback:
			#self._callback(self._state)	# True is Pressed ON, else False
	@property
	def value ( self ):
		return self._state
	@value.setter
	def value ( self, val ):
		self._state = bool(val)
		self.DrawText()
	@property
	def enable ( self ):
		return self._enabled
	@enable.setter
	def enable ( self, val ):
		self._enabled = bool(val)
		self.DrawText()
	@property
	def text ( self ):
		if self._text != None:
			return self.lang.GetText(self._text[self._state])
		return self._buttonText
	@text.setter
	def text ( self, txt ):
		self._buttonText = txt
		self.DrawText()
	def DrawText ( self ):
		if self._enabled:
			if self._state:
				fillc = Globals.buttonpressedcolor
				fillt = Globals.buttonpressedtextcolor
			else:
				fillc = Globals.buttonbackcolor
				fillt = Globals.buttontextcolor
		else:
			fillc = '#303030'
			fillt = Globals.defaultBackgroundColor
		self._canvas.itemconfig(self._circle,fill=fillc)
		if self._text != None:
			if self.lang:	txt = self.lang.GetText(self._text[self._state])
			else:	txt = self._text[self._state]
		else:
			txt = self.lang.GetText(self._buttonText)
		self._canvas.itemconfig(self._textArea,fill=fillt,text=txt)
	def Pressed ( self, event ):
		if not self._enabled: return
		state = self._state
		self._state = True
		self.DrawText()
		self._state = state
	def Released ( self, event ):
		if not self._enabled: return
		self._state = not self._state
		self.DrawText()
		if self._callback:
			self._callback(self._state)	# True is Pressed ON, else False
	def UpdateLang ( self ):
		self.DrawText()

class MyButton ( ttk.Frame ):
	def __init__(self,parent,*args,**kargs):
		ttk.Frame.__init__(self,parent)
		self.config(style='F.TFrame')
		self._parent = parent
		try:		self._callback = kargs['callback']
		except:	self._callback = None
		try:		self.lang = kargs['language']
		except:	self.lang = None
		try:		self._text = kargs['text']
		except:	self._text = ''
		try:		self._width = int(kargs['width'])
		except:	self._width = 50
		try:		self._height = int(kargs['height'])
		except:	self._height = Globals.defaultButtonHeight
		self._canvas = Canvas(self,width=self._width,height=self._height,
			background=Globals.buttonbackcolor)
		self._canvas.grid(row=0,column=0)
		self._canvas.bind('<Button-1>',self.Pressed)
		self._canvas.bind('<ButtonRelease-1>',self.Released)
		if self.lang:	txt = self.lang.GetText(self._text)
		else:	txt = self._text
		self._textArea = self._canvas.create_text((int(self._width/2),
			int(self._height/2)),font=Globals.defaultFont,
			fill=Globals.buttontextcolor,text=txt)
	def Pressed ( self, event ):
		self._canvas.config(background=Globals.buttonpressedcolor)
		self._canvas.itemconfig(self._textArea,fill=Globals.buttonpressedtextcolor)
	def Released ( self, event ):
		self._canvas.config(background=Globals.buttonbackcolor)
		self._canvas.itemconfig(self._textArea,fill=Globals.buttontextcolor)
		if self._callback:
			self._callback()	# no parameters
	def UpdateLang ( self ):
		if self.lang:	txt = self.lang.GetText(self._text)
		else:	txt = self._text
		self._canvas.itemconfig(self._textArea,text=txt)

class Slider ( ttk.Frame ):
	def __init__(self,parent,*args,**kargs):
		ttk.Frame.__init__(self,parent)
		self.config(style='F.TFrame')
		self._parent = parent
		self.columnconfigure(0,weight=1)		# Allow autoresizing
		try:		self._callback = kargs['callback']
		except:	self._callback = None
		try:		self.lang = kargs['language']
		except:	self.lang = None
		self._list = False
		try:
			self._text = kargs['text']
			if isinstance(self._text,str):	pass
			elif ( isinstance(self._text,list) and
					 isinstance(self._text[0],str) ):	# only string lists please
				self._list = True
				self._minVal = 0
				self._maxVal = len(self._text) - 1
				self._lastValue = -99999
			else: raise ValueError("'text' must be a string or a list of strings")
		except:	self._text = ''
		if not self._list:
			self._minVal = int(kargs['_from'])
			self._maxVal = int(kargs['_to'])
			if self._minVal >= self._maxVal:
				raise ValueError("'_from' must be less than '_to'")
		# Constrain value to min and max values (or _from and _to)
		self._value = int(kargs['value'])
		if self._value < self._minVal: self._value = self._minVal
		if self._value > self._maxVal: self._value = self._maxVal
		try:		self._width = int(kargs['width'])
		except:	self._width = 10
		try:		self._height = int(kargs['height'])
		except:	self._height = Globals.defaultSliderHeight
		try:		self._addValue = kargs['addValue']
		except:	self._addValue = True
		self._canvas = Canvas(self,width=self._width,height=self._height,
			background=Globals.sliderbackcolor)
		self._canvas.grid(row=0,column=0,sticky='ew')
		self._canvas.bind('<Button-1>',self.Pressed)
		self._canvas.bind('<B1-Motion>',self.Moved)
		self._canvas.update_idletasks()
		x = ( int(float(self._value - self._minVal) * float(self._canvas.winfo_width()) /
				    float(self._maxVal - self._minVal)) )
		self._rect = self._canvas.create_rectangle(0, 0, x, self._height,
			fill=Globals.slidercolor)
		# Text is centered in rectangle.  Have 'align' option?
		self._textArea = self._canvas.create_text((10,self._height/2),
			anchor=W,font=Globals.defaultFont,fill=Globals.slidertextcolor)
		self.DrawText()
		self.after(10,self.Again)
	def Again ( self ):
		self.Update(None)
	@property
	def text ( self ):
		return self._text
	@text.setter
	def text ( self, val ):
		if isinstance(val,str):
			self._text = val
			self._list = False
		elif isinstance(val,list) and isinstance(val[0],str):
			self._text = val
			self._list = True
			self.DrawText()
	@property
	def value ( self ):
		return self._value
	@value.setter
	def value ( self, val ):
		self._value = min(self._maxVal, max(self._minVal, int(val)))
		self.DrawText()
	def Update ( self, event ):
		w = float(self._canvas.winfo_width())
		if event == None:
			x = int(float(self._value - self._minVal) / float(self._maxVal - self._minVal) * w)
		else:
			x = min(w, max(0, int(event.x)))
			self._value = ( int(self._minVal + float(x) / float(w) *
									float(self._maxVal - self._minVal)) )
		self._canvas.coords(self._rect,0,0,x,self._height)
		self.DrawText()
		if self._callback:
			if self._list:
				if self._value != self._lastValue:
					self._lastValue = self._value
					self._callback(self._text[self._value])
			else:	self._callback(self._value)
	def DrawText ( self ):
		if self._list:
			txt = self._text[self._value]
			if self.lang:	t = self.lang.GetText(txt)
			else:			t = txt
		else:
			if self.lang:	t = self.lang.GetText(self._text)
			else:			t = self._text
			if self._addValue:	txt = "%s: %d" % (t,self._value)
			else:	txt = t
		self._canvas.itemconfig(self._textArea,text=txt)
	def Pressed ( self, event ):
		self.Update(event)
	def Moved ( self, event ):
		self.Update(event)
	def UpdateLang ( self ):
		self.DrawText()
