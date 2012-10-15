'''
# Author: shawn.carrillo+log4j@gmail.com
# Source: https://github.com/scarrillo/Log4j-Sublime
# Version 1.0
# Date: 2012.09.23
#
# Credit for tail.py: 
# Author - Kasun Herath <kasunh01 at gmail.com>
# Source - https://github.com/kasun/python-tail
''' 
import sublime, sublime_plugin, os, subprocess, thread, time, tail, threading

class Log4jCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		sublime_plugin.WindowCommand.__init__(self, window) # super!
		self.LEVELS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
		self.loadSettings()

	def loadSettings(self):
		self.settings = sublime.load_settings("Log4j.sublime-settings")
		self.custom_syntax = self.settings.get("syntax")
		self.custom_scheme = self.settings.get("color_scheme")
		self.log_file = self.settings.get("log_file")

	def run(self):
		sublime.active_window().show_input_panel('Log4j Filter: ', '', lambda s: self.doInput(s), None, None)

	def doInput(self, filter):
		panel_name = 'log4j'
		logFile = sublime.active_window().folders()[0] + "/" + self.log_file

		self.init_view(panel_name, self.custom_syntax, self.custom_scheme)
		self.initFilter(filter)
		self.initTail(logFile)

	def initFilter(self, filter):
		self.level = ""
		self.filter = ""

		if len(filter) != 0:
			if filter.upper() in self.LEVELS:
				self.level = "["+filter.upper()+"]"
				self.appendInfo("Filter Level: "+ self.level)
				sublime.status_message("Log4j: Filter Level: "+ self.level)
			else:
				self.level = ""
				self.filter = filter
				self.appendInfo("Filter String: "+ self.filter)
				sublime.status_message("Log4j: Filter String: "+ self.level)
		else:
			self.appendInfo("No Filter")
			sublime.status_message("Log4j: No Filter")

	def doMessage(self, message):
		if ( len(self.level) != 0 and message.startswith(self.level) ) or \
			(len(self.filter) != 0 and message.find(self.filter) >= 0) or \
			(len(self.level) == 0 and len(self.filter) == 0):

			self.append(message.rstrip()+"\n")
		#else:
			#self.append("squeltched!\n")

	def doTailOut(self, message):
		sublime.set_timeout(lambda: self.doMessage(message), 0)

	def initTail(self, logFile):
		self.stopTail()

		threadId = threading.activeCount() + 1

		try:
			tailThread = TailThread(logFile, self.doTailOut, threadId) #file, callback
			tailThread.start()
		except:
			self.appendError("Log4j: unable to tail file: "+ logFile)

	def stopTail(self):
		#print "Log4j: stopTail: Active Threads:"+str(threading.activeCount())

		for t in threading.enumerate():
			#print "> Closing: "+str(t)
			if isinstance(t, TailThread):
				#print "\tClosed: instance: "+str(t)
				t.stop()
			elif t.__class__.__name__ == "TailThread":
				# isinstance seems to fail when the plugin is restarted without releasing resources. This works.
				#print "\tClosed: type?: "+str(t)
				t.stop()
			#else:
				#print "\t!Closed: "+str(t)+" | "+str(isinstance(t, TailThread))+" | "+t.__class__.__name__

	def appendError(self, data):
		self.append("[ERROR][Log4j]: "+ data +"\n")
		print "Log4j: "+data

	def appendInfo(self, data):
		self.append("[INFO][Log4j]: "+ data +"\n")

	def append(self, data):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.insert(edit, self.output_view.size(), data)
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)
		#self.output_view.show_at_center(self.output_view.size())
		self.output_view.show(self.output_view.size())

	def edit_clear(self):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)

	def init_view(self, name, syntax=None, scheme=None):
		# only use "get_output_panel" once, otherwise sublime will
		# recreate a new one and you will lose any existing text
		if not hasattr(self, 'output_view'):
			self.output_view = self.window.get_output_panel(name)
			self.output_view.set_syntax_file(syntax)
			#Seems to be automatically pulling this
			#self.output_view.settings().set("color_scheme", scheme)
		
		self.edit_clear()
		sublime.active_window().run_command("show_panel", {"panel": "output."+name})

	#""" Sublime sometimes invokes this when reloading the plugin """
	#def __del__(self):
	#	print ">>> Log4jCommand: release"

class TailThread(threading.Thread):
	def __init__(self, logFile, callback, threadId):
		self.logFile = logFile
		self.tail = tail.Tail(self.logFile)
		self.threadId = threadId
		print "\tTail: init ID #"+ str(self.threadId)
		self.tail.register_callback(callback)
		threading.Thread.__init__(self)

	def run(self):
		print "\tTail: Start ID #" + str(self.threadId)
		self.tail.follow(s=.02)

	def stop(self):
		print "\tTail: Stop #" + str(self.threadId)
		self.tail.end()
