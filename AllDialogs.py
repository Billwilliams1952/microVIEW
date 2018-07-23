#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#  AllDialogs.py
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

from Dialog import *

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
		raise ImportError ("\n\n#### ImageTk not installed.\n ####" \
				 "#### Use: sudo apt-get install python3-pil.imagetk ####")
else:
	from	Tkinter import *	# Python 2.X
	import 	tkFileDialog as FileDialog
	import 	tkMessageBox as MessageBox
	import 	ttk
	from 	ttk import *
	import 	tkFont
	from	PIL import ImageTk

class QuitDialog ( Dialog ):
	def BuildDialog ( self ):
		l4 = Label(self.MainFrame,text='PiCamera ver 0.2  ',
			font=('Helvetica',20,'bold italic'), \
			foreground='blue') #,anchor='center')
		l4.grid(row=0,column=0,sticky='W') #'EW')


