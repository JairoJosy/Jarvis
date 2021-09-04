#!/usr/bin/env python2.7
#coding=UTF-8

# Copyright (c) 2016 Angelo Moura
#
# This file is part of the program PytheM
#
# PytheM is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA


from brain import Jarvis
import serial.tools.list_ports
import os,sys
import webbrowser
import subprocess
import termcolor

def color(message,color):
        msg = termcolor.colored(str(message), str(color), attrs=["bold"])
        return msg

class Processor(object):

	name = "Jarvis-Processor"
	desc = "Console to process voice commands"
	version = "0.3"

	def __init__(self):
		self.Jarvis = Jarvis()

	def help(self,version):
		print
		print("[ Jarvis - Personal Assistence - v{} ]".format(version),"blue")
		print
		print
		print("[*] exit |or| quit : 			Terminate the program.","blue")
		print
		print
		print("[*] sleep |or| stop |or| wait:  	Sleep until you say 'Jarvis'.","blue")
		print
		print
		print("[*] newspaper |or| news: 		Read the top trending news from reddit.","blue")
		print
		print
		print("[*] say |or| speak [message]:      	Ask Jarvis to say something.","blue")
		print
		print(" examples(say):","green")
		print
  		print("  say I like donuts","green")
  		print("  speak my name is Jarvis","green")
		print
		print
		print("[*] run [script]:	 		Run .sh script that you place on the scripts folder with chmod +x","blue")
		print
		print(" example(say):","green")
		print
		print("  run firewall		 		| Place a firewall.sh on the scripts folder and give execution privilege first.","green")
		print
		print
		print("[*] browser:		 		Ask Jarvis to start your default browser.","blue")
		print
 		print(" example(say):","green")
		print
  		print("  browser","green")
		print
		print
		print("[*] terminal:		 		Ask Jarvis to open a gnome-terminal.","blue")
		print
 		print(" example(say):","green")
		print
  		print("  terminal","green")
		print
		print
		print("[*] search [query]	 		Ask Jarvis to search query via google.","blue")
		print
		print(" example(say):","green")
		print
		print("  search python programming.","green")
		print
		print
 		print("[*] input [keystroke]:   		Send a command to the Arduino Leonardo without entering editor mode.","blue")
		print
        	print("          * ARDUINO LEONARDO REQUIRED *","red")
		print
		print("voice commands: (Same as EDITOR MODE )","yellow")
		print
		print
		print("[*] editor: 				Start the editor mode.","blue")
		print
		print("          * ARDUINO LEONARDO REQUIRED *","red")
		print
		print("               [EDITOR MODE]","red")
		print
		print("voice commands: (anything else will be typed)","yellow")
		print
		print(" forward   = tab","green")
 		print(" back      = (shift+tab)","green")
 		print(" up        = up arrow","green")
		print(" down      = down arrow","green")
		print(" right     = right arrow","green")
		print(" left      = left arrow","green")
		print(" super     = super/windows","green")
		print(" slash     = slash(/)","green")
		print(" backspace = backspace(erase character)","green")
		print(" erase	  = press backspace 10 times","green")
		print(" space     = space(spacebar)","green")
		print(" enter     = enter(return)","green")
		print(" close	  = close(alt+f4)","green")
		print(" escape    = escape(esc)","green")
		print(" exit	  = leaves editor mode","green")
		print

	def start(self):
		try:
			self.Jarvis.ser.open()

		except Exception as e:
			print "[!] Arduino Leonardo not found, features that use keyboard will not work."

		try:
			self.Jarvis.Say(self.Jarvis.random('greetings'))
			while 1:
				try:
					self.command = self.Jarvis.Listen()
       		        		self.message = self.command.split()
        			        self.input_list = [str(a) for a in self.message]
					if self.input_list[0] == "exit" or self.input_list[0] == "quit":
						self.Jarvis.Say(self.Jarvis.random('salutes'))
						exit()

					elif self.input_list[0] == "sleep" or self.input_list[0] == "stop" or self.input_list[0] == "wait":
						self.Jarvis.Say("Call me if you need me sir.")
						while 1:
							self.wait = self.Jarvis.Listen()
							if self.wait == "Jarvis":
								self.Jarvis.Say(self.Jarvis.random('affirmative'))
								break

					elif self.input_list[0] == "newspaper" or self.input_list[0] == "news":
						self.Jarvis.Say("Here are the news sir.")
						self.titles = self.Jarvis.GetNews()
						self.Jarvis.SpeakNews(self.titles)

					elif self.input_list[0] == "browser":
						try:
							webbrowser.open("https://www.google.com")
							self.Jarvis.Say(self.Jarvis.random('affirmative'))
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass

					elif self.input_list[0] == "terminal":
						try:
							os.system("gnome-terminal")
							self.Jarvis.Say(self.Jarvis.random('affirmative'))
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass

					elif self.input_list[0] == "search":
						try:
							search = self.input_list[1:]
							real = "".join(search)
							url = "https://www.google.com/search?q={}".format(real)
							webbrowser.open(url)
							self.Jarvis.Say(self.Jarvis.random('affirmative'))
						except Exception as e:
							print "[!] Exception caught: {}".format(e)
							pass

					elif self.input_list[0] == "say" or self.input_list[0] == "speak":
						self.Jarvis.Say(self.input_list[1:])

					elif self.input_list[0] == "run":
						self.Jarvis.Say(self.Jarvis.random('affirmative'))
						os.system("./scripts/{}.sh".format(self.input_list[1]))

					elif self.input_list[0] == "input":
                                                try:
                                                        self.Jarvis.SerialWrite(self.input_list[1])
                                                        self.Jarvis.Say(self.Jarvis.random('affirmative'))
                                                except:
                                                        self.Jarvis.Say("Feature not working master, plug your Arduino Leonardo then restart the program.")
                                                        pass

					elif self.input_list[0] == "editor":
						self.Jarvis.Say("Starting edition mode sir.")
                                	        while 1:
                                     			self.editmode = self.Jarvis.Listen()
                                     	 		self.mesg = self.editmode
                                       	 	        #self.msg = "".join(self.mesg)

                                       	        	if self.mesg is not None:
								try:
									self.Jarvis.SerialWrite(self.mesg)
                                       	        			self.Jarvis.Say(self.Jarvis.random('affirmative'))
								except:
									self.Jarvis.Say("Feature not working, plug you Arduino Leonardo then restart the program.")
									break
                                                	else:
								pass
							if self.editmode == "exit":
                                                        	self.Jarvis.Say("Stoping edition mode sir.")
								break

					else:
                       				print '[!] Input a valid option, enter "help" to see valid commands.'
						self.Jarvis.Say("i heard, {}".format(self.command))
						self.Jarvis.Say(self.Jarvis.random('dntunderstand'))


				except IndexError:
					pass
				except AttributeError:
					pass


		except KeyboardInterrupt:
			print "\n[*] User requested shutdown"
			self.Jarvis.Say(self.Jarvis.random('salutes'))
			exit()
		except Exception as e:
			print "[!] Exception caught: {}".format(e)

	def backgroundstart(self,path):
		try:
			with open("{}/log/jarvis.log".format(path),"a+") as stdout:
				self.p = subprocess.Popen(["python {}/core/processor.py".format(path)], shell=True, stdout=stdout, stderr=stdout)
			return
		except Exception as e:
			print "[-] Problem starting Jarvis in background: {}".format(e)


if __name__ == '__main__':
	processor = Processor()
	processor.start()
