#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#  WebStream.py
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
#  GNU Genera192.168.1.16:800l Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
'''
import	sys
import	io
import	picamera
import	logging
import	threading
from	threading import Condition

Python3 = True
if sys.version_info[0] == 3:
	from http import server
	import socketserver
else:
	raise ImportError ("\n\n**** This program currently runs under Python3 only. ****")
	Python3 = False
	from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
	from SimpleHTTPServer import SimpleHTTPRequestHandler
	
from Globals	import *

PAGE_DISPLAY = ""

'''
The HTML description for the web page.
TODO: Make this an external file that the user can specify at startup or
in the Network tab.
'''
PAGE_SETUP = \
"""\
<html>
<head>
<style>
body {
	background-color: rgb(255,255,255);
}
h1 {
	background-color: rgb(255,255,255);
	color: rgb(0,0,0);
}
h3 {
	color: rgb(0,0,0);
}
</style>
<title>microVIEW Video</title>
</head>
<body>
<h1><center>#1</center></h1>
<h3><center>#2</center></h3>
<p style="text-align:center;"><img src="stream.mjpg" width="800" height="600" /></p>
</body>
</html>
"""

output = None	# 	Need a global variable here

class StreamingOutput(object):
	def __init__(self):
		self.frame = None
		self.buffer = io.BytesIO()
		self.condition = Condition()

	def write(self, buf):
		if buf.startswith(b'\xff\xd8'):
			# New frame, copy the existing buffer's content and notify all
			# clients it's available
			self.buffer.truncate()
			with self.condition:
				 self.frame = self.buffer.getvalue()
				 self.condition.notify_all()
			self.buffer.seek(0)
		return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.send_response(301)
			self.send_header('Location', '/index.html')
			self.end_headers()
		elif self.path == '/index.html':
			# Update the HTML with the Heading levels identified in the INI file.
			PAGE_DISPLAY = PAGE_SETUP.replace("#1",Globals.headingLevel1).replace("#2",Globals.headingLevel2)
			content = PAGE_DISPLAY.encode('utf-8')
			self.send_response(200)
			self.send_header('Content-Type', 'text/html')
			self.send_header('Content-Length', len(content))
			self.end_headers()
			self.wfile.write(content)
		elif self.path == '/stream.mjpg':
			self.send_response(200)
			self.send_header('Age', 0)
			self.send_header('Cache-Control', 'no-cache, private')
			self.send_header('Pragma', 'no-cache')
			self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
			self.end_headers()
			try:
				while True:
					with output.condition:
						output.condition.wait()
						frame = output.frame
					self.wfile.write(b'--FRAME\r\n')
					self.send_header('Content-Type', 'image/jpeg')
					self.send_header('Content-Length', len(frame))
					self.end_headers()
					self.wfile.write(frame)
					self.wfile.write(b'\r\n')
			except Exception as e:
				logging.warning(
					'Removed streaming client %s: %s',
					self.client_address, str(e))
		else:
			self.send_error(404)
			self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True

class StreamingVideo:
	def __init__ ( self, camera, resolution, language ):
		self.camera = camera
		self.resolution = resolution
		self.lang = language
		self._recording = False
		self._streaming = False
	@property
	def recording ( self ):
		return self._recording
	@recording.setter
	def recording ( self, val ):
		if self._streaming:
			if val:
				if not self._recording:
					self.camera.start_recording(self.output, format='mjpeg',
						splitter_port=2)
			elif self._recording:
				self.camera.stop_recording(splitter_port=2)
		self._recording = val
	@property
	def enable ( self ):
		return self._streaming
	@enable.setter
	def enable ( self, val ):
		if val:	self.StartStream()
		else:		self.StopStream()
		self._recording = val
	'''
	This function can only be called once.
	TODO: How can we start/stop the server under program control?
	'''
	def StartStream ( self ):
		if not self._streaming:
			global output
			self.output = StreamingOutput()
			output = self.output
			if self._recording:
				self.camera.start_recording(self.output, format='mjpeg',splitter_port=2)
			self.address = ('', 8000)
			# Python2 equivalent
			#def run(server_class=BaseHTTPServer.HTTPServer,
					#handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
				#server_address = ('', 8000)
				#httpd = server_class(server_address, handler_class)
				#httpd.serve_forever()
			self.server = StreamingServer(self.address, StreamingHandler)
			self.server_thread = threading.Thread(target=self.server.serve_forever)
			self.server_thread.daemon = True
			self.server_thread.start()
			self._streaming = True
	'''
	This function can only be called at program termination.
	TODO: How can we start/stop the server under program control?
	'''
	def StopStream ( self ):
		if self._streaming:
			print("Shutdown server")
			if self._recording:
				self.camera.stop_recording(splitter_port=2)
				self._recording = False
			self.server.shutdown()
			self._streaming = False


