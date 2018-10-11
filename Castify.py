#usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter, tkFileDialog
from subprocess import call
from subprocess import Popen, PIPE
from getpass import getpass
import multiprocessing
from time import sleep
import pdb
import threading
#####################################################################################################
class RadioApp(Tkinter.Tk):

	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.protocol('WM_DELETE_WINDOW', self.cleanExit)
		self.initialize()
#####################################################################################################
	def initialize(self):
		self.grid()
		
		
		#frequency text box
		self.text = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable = self.text)
		self.entry.grid(column=0,row=1,columnspan=2,sticky='EW')
		self.entry.bind("<Return>",self.onPressEnter)
		self.text.set(u"frequency")

		# start stop button
		self.buttonName = Tkinter.StringVar()
		self.button = Tkinter.Button(self,textvariable = self.buttonName,
								command = self.onStartButtonClick)
		self.button.grid(column=2,row=1)
		self.buttonName.set(u"Start")

		#Now playing
		self.labelvar = Tkinter.StringVar()
		label = Tkinter.Label(self,textvariable = self.labelvar,
							fg="white",bg="blue")
		label.grid(column=0,row=2,columnspan=3,sticky='EW')
		self.labelvar.set("Not Broadcasting")

		# song selector file browser

		#toggle song/mic button

		# this adds resizability
		self.grid_columnconfigure(0,weight=1)
		#self.grid_rowconfigure(0,weigh=1)

		#file Label
		self.browserText = Tkinter.StringVar()
		self.browserEntry = Tkinter.Entry(self,
										textvariable = self.browserText)
		self.browserEntry.grid(column = 0, row = 0,columnspan=2
								,sticky = 'EW')
		self.browserText.set(u"Click Browse")

		#filebrowser button
		self.bbn = Tkinter.StringVar()
		self.browseButton = Tkinter.Button(self, textvariable = self.bbn,
											command = self.onBrowseButtonClick)
		self.browseButton.grid(column = 2, row = 0)
		self.bbn.set(u"Browse")

		#broadcast live button

		#this controls resizability, keep it off
		self.resizable(False,True)
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

#####################################################################################################
	def onStartButtonClick(self):

		self.gupdate = True
		if self.buttonName.get() == "Start":
			print self.gupdate
			def changeButton(self):
				print self.gupdate
				self.labelvar.set("Broadcasting on "+self.text.get()+"!")
				self.buttonName.set("Stop")

				#sox **FILE** -t wav -b 16 -r 22050 -c 1 - | ssh pi@raspberrypi.local 'sudo ./pifm - 100.1 22050'
				#sox -d -t wav -b 16 -r 22050 -c 1 - | ssh pi@raspberrypi.local 'sudo ./pifm - 100.1 22050'
				call("sox " + '"' + self.browserText.get() + '"' + " -t wav -b 16 -r 22050 -c 1 - | ssh pi@raspberrypi.local 'sudo ./pifm - " + self.text.get() + " 22050'",shell = True)
				self.gupdate = False
				self.labelvar.set("Not Broadcasting :(")
				self.buttonName.set("Start")

			def updateGUI(self):
				while self.gupdate:
					self.update()
					sleep(.1)

			t1 = threading.Thread(target=changeButton, args=(self,))
			t2 = threading.Thread(target=updateGUI, args=(self,))

			t1.start()
			t2.start()
#####################################################################################################
		elif self.buttonName.get() == "Stop":
			self.labelvar.set("Not Broadcasting :(")
			self.buttonName.set("Start")
			#stop the broadcast
			def exit(self):
				call('ssh pi@raspberrypi.local "sudo killall pifm"' ,shell = True)
				call('killall sox', shell = True)
				self.gupdate = False
			def updateGUI(self):
				while self.gupdate:
					self.update()
					sleep(.1)
			Bstop = threading.Thread(target=exit, args=(self,))
			GUI = threading.Thread(target = updateGUI, args=(self,))
			Bstop.start()
			GUI.start()

		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

#####################################################################################################
	def onPressEnter(self,event):
		if self.buttonName.get() == "Start":
			self.labelvar.set( "Frequency set to " + self.text.get() + "!")
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

	def onBrowseButtonClick(self):
		#filebrowser
		self.file_opt = options = {}
		options['filetypes'] = [('all files', '.*'), ('mp3 audio', '.mp3'),
								('wave File','.wav'), ('m4a audio','.m4a')]
		options['initialdir'] = '~:/'
		options['initialfile'] = 'sound.wav'
		options['parent'] = None
		options['title'] = 'Pick a sound file'
		self.audioFile = tkFileDialog.askopenfilename(**self.file_opt)
		self.browserText.set(self.audioFile)

#####################################################################################################
	def cleanExit(self):
		self.gupdate = True
		self.labelvar.set("Not Broadcasting :(")
		self.buttonName.set("Start")
		#stop the broadcast
		def exit(self):
			print "closing application"
			call('killall sox', shell = True)
			call('ssh pi@raspberrypi.local "sudo killall pifm"' ,shell = True)
			print self.gupdate
			self.gupdate = False
		def updateGUIandExit(self):
			while self.gupdate:
				self.update()
				sleep(.1)
			self.destroy()
			self.quit()
		Bstop = threading.Thread(target=exit, args=(self,))
		GUI = threading.Thread(target = updateGUIandExit, args=(self,))
		Bstop.start()
		GUI.start()

#####################################################################################################
if __name__ == "__main__":
    app = RadioApp(None)
    app.title('Castify ')
    app.mainloop()