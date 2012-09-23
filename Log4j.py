import sublime, sublime_plugin, os, subprocess, thread, time, tail, threading

class Log4jCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		sublime_plugin.WindowCommand.__init__(self, window) # super!
		self.LEVELS = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]

	def run(self):
		sublime.active_window().show_input_panel('Filter: ', '', lambda s: self.doInput(s), None, None)

	def doInput(self, filter):
		# some unique name for your output panel
		panel_name = 'log4j'
		# relative path to your custom syntax
		custom_syntax = 'Packages/Log4j/Log4j.tmLanguage'
		logFile = sublime.active_window().folders()[0] + "/log4j.log"

		self.init_view(panel_name, custom_syntax)
		self.initFilter(filter)
		self.initTail(logFile)
		#self.end_view(custom_syntax) # Need to leave open for threaded use

	def initFilter(self, filter):
		self.level = ""
		self.filter = ""

		if len(filter) != 0:
			if filter.upper() in self.LEVELS:
				self.level = "["+filter.upper()+"]"
				self.append("[INFO][sublime]: Filter Level: "+ self.level +"\n")
			else:
				self.level = ""
				self.filter = filter
				self.append("[INFO][sublime]: Filter String: "+ self.filter +"\n")
		else:
			self.append("[INFO][sublime]: No Filter\n")

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
		self.initThreads()
		tailThread = TailThread(logFile, self.doTailOut) #file, callback
		tailThread.start()

	def initThreads(self):
		print "initThreads: "+str(threading.activeCount())
		main = threading.currentThread()
		for t in threading.enumerate():
			if t is main:
				#print "Main Thread: ignore"
				continue
			#print "Stop: "+t.logFile
			t.stop()

	def append(self, data):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.insert(edit, self.output_view.size(), data)
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)
		self.output_view.show_at_center(self.output_view.size())

	def edit_clear(self):
		self.output_view.set_read_only(False)
		edit = self.output_view.begin_edit()
		self.output_view.erase(edit, sublime.Region(0, self.output_view.size()))
		self.output_view.end_edit(edit)
		self.output_view.set_read_only(True)

	def init_view(self, name, syn):
		# only use "get_output_panel" once, otherwise sublime will
		# recreate a new one and you will lose any existing text
		if not hasattr(self, 'output_view'):
			self.output_view = self.window.get_output_panel(name)
			self.output_view.set_syntax_file(syn)
		
		#self.output_view.set_read_only(False)
		self.edit_clear()
		sublime.active_window().run_command("show_panel", {"panel": "output."+name})

	#def end_view(self, syn):
		#self.output_view.set_read_only(True)
		#self.output_view.show_at_center(self.output_view.size())
		#self.output_view.set_syntax_file(syn)

class TailThread (threading.Thread):
	def __init__(self, logFile, callback):
		print "TailThread: init"
		self.logFile = logFile
		self.tail = tail.Tail(self.logFile)
		self.tail.register_callback(callback)
		threading.Thread.__init__(self)

	def run(self):
		print "TailThread: Start: " + self.logFile
		self.tail.follow(s=0)

	def stop(self):
		print "TailThread: Stop"
		self.tail.end()
