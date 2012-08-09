#!/usr/bin/env kross
# -*- coding: utf-8 -*-
import KTorrent
import KTScriptingPlugin
import Kross
from subprocess import call
#from PyQt4 import QtCore

t = Kross.module("kdetranslation")

class AutoExecute:
	def __init__(self):
		self.command = ""
		KTorrent.connect("torrentAdded(const QString &)",self.torrentAdded)
		tors = KTorrent.torrents()
		# bind to signals for each torrent
		for t in tors:
			self.torrentAdded(t)
		
		
	def torrentFinished(self,tor):
		KTorrent.log("Torrent finished %s" % tor.name())
		if self.command != "":
			KTorrent.log("Executing command: %s" % self.command)
			KTorrent.log("For torrent: %s" % tor.name() )
			call([self.command,tor.infoHash(),tor.name(),tor.pathOnDisk()])
			
	
	def torrentAdded(self,ih):
		tor = KTorrent.torrent(ih)
		KTorrent.log("Torrent added %s" % tor.name())
		tor.connect("finished(QObject* )",self.torrentFinished)

	def save(self):
		KTScriptingPlugin.writeConfigEntry("AutoExecuteScript","command",self.command)
		KTScriptingPlugin.syncConfig("AutoExecuteScript")
	
	def load(self):
		self.command = KTScriptingPlugin.readConfigEntry("AutoExecuteScript","command","")
		
	def configure(self):
		forms = Kross.module("forms")
		dialog = forms.createDialog(t.i18n("Auto Execute Settings"))
		dialog.setButtons("Ok|Cancel")
		page = dialog.addPage(t.i18n("Auto Execute"),t.i18n("Auto Execute"),"system-run")
		widget = forms.createWidgetFromUIFile(page,KTScriptingPlugin.scriptDir("auto_execute") + "auto_execute.ui")
		widget["command_line"].setText(self.command) 
		if dialog.exec_loop():
			self.command = widget["command_line"].text 
			self.save()


ar = AutoExecute()
ar.load()

def configure():
	global ar
	ar.configure()

def unload():
	global ar
	del ar