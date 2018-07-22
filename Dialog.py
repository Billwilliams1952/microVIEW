'''
Dialog.py for microVIEW
Copyright 2018 Bill Williams <github.com/Billwilliams1952>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''
import sys

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
		raise ("ImageTk not installed. If running Python 3.x\n" \
				 "Use: sudo apt-get install python3-pil.imagetk")
else:
	from	Tkinter import *	# Python 2.X
	import 	tkFileDialog as FileDialog
	import 	tkMessageBox as MessageBox
	import 	ttk
	from 	ttk import *
	import 	tkFont
	from PIL import ImageTk



#
# Generic Dialog CLass - All dialogs inherit from this one
#
class Dialog:
	def __init__ ( self, parent, modal=True, title='No title supplied',
				   showtitlebar=True, centerTo='default', okonly=True,
				   help=False, resizable=False, minwidth=None, minheight=None,
				   camera=None, data = None ):
		self._parent = parent
		self.modal = modal
		self._window = Toplevel()
		self._window.minsize(minwidth,minheight)
		self.CancelButton = None

		if resizable is False:
			self._window.resizable(width=False,height=False)

		self._window.rowconfigure(0,weight=1)
		self._window.columnconfigure(0,weight=1)
		self._window.title(title)
		self._centerTo = centerTo

		# Should be:			Need to fix.....
		# self._mainFrame
		#	self.LayoutFrame
		#		Supplied to User for Layout
		#	self._buttonFrame
		#		Help	Cancel	Ok
		self.MainFrame = ttk.Frame(self._window,padding=(5,5,5,5))
		self.MainFrame.grid(row=0,column=0,columnspan=3,sticky='NSEW')

		self._camera = camera
		self.data = data

		self.okimage = ImageTk.PhotoImage(file='Assets/ok_22x22.png')
		self.OkButton = ttk.Button(self._window,text='Close' if okonly else 'Ok',
			command=lambda:self._Ok(None),image=self.okimage,compound='left')
		self.OkButton.grid(row=1,column=2,padx=10,pady=5)
		self.OkButton.focus_set()
		self._window.bind( '<Return>', self._Ok )

		if okonly is False:
			self.cancelimage = ImageTk.PhotoImage(file='Assets/cancel_22x22.png')
			self.CancelButton = ttk.Button(self._window,text='Cancel',
				command=lambda:self._Cancel(None),image=self.cancelimage,
				compound='left',state='disabled')
			self.CancelButton.grid(row=1,column=1,pady=5)
			self._window.bind( '<Escape>', self._Cancel )

		if help is True:
			b = ttk.Button(self._window,text='Help',command=lambda:self._Help(None))
			b.grid(row=1,column=0,sticky='W',padx=10,pady=5)

		self.BuildDialog()	# Overriden function

		self._window.after(10,self._Position)	# better way found!
		self._window.overrideredirect(not showtitlebar)
		self._window.transient(self._parent)	# no icon

		if modal is True:	# must close this dialog to return to parent
			self._window.grab_set()
			self._parent.wait_window(self._window)

	def BuildDialog ( self ):				# Always Override
		pass #UnderConstruction ( self.MainFrame )
	def OkPressed ( self ): return True		# Optional Override
	def CancelPressed ( self ): return True	# Optional Override
	def HelpPressed ( self ):				# Optional Override
		MessageBox.showwarning("Help","No Help available!")

	# Remap these so the dialog doesn't have to worry about the
	# 'event' parameter
	def _Ok ( self, event ):
		if self.OkPressed(): self._window.destroy()
	def _Cancel ( self, event ):
		if self.CancelPressed() : self._window.destroy()
	def _Help ( self, event ):
		self.HelpPressed()

	def _Position ( self ):
		if self._centerTo == 'default': return
		# handle center window and center screen
		if self._centerTo == 'parent':
			parentwidth = self._parent.winfo_width()
			parentheight = self._parent.winfo_height()
			locX = self._parent.winfo_x()
			locY = self._parent.winfo_y()
		else:	# center to 'screen'
			parentwidth = self._parent.winfo_screenwidth()
			parentheight = self._parent.winfo_screenheight()
			locX = 0
			locY = 0
		width = self._window.winfo_width()
		height = self._window.winfo_height()
		x = locX + parentwidth/2 - width / 2
		y = locY + parentheight / 2 - height / 2
		self._window.geometry('%dx%d+%d+%d' % (width,height,x,y))



