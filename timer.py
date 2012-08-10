#!/usr/bin/env python
_VERSION = "0.9.1"

# USERCONFIG 
_TIMERS_TO_SPAWN = 3      # How many timers you need? (values between 1-9)
_DEFAULT_NAME_OF_TIMERS = "noName" # the default name of the timers (can change it later)
_DEFAULT_DUMP_FILE_NAME = "/tmp/dump" # the default file for dumping each timer
_VERTICAL = False # False/True if this is True the timers are shown vertical istead of horizontal
_REFRESH_RATE = 0.5 # Seconds to sleep between the refresh could also eg. 0.5, 0.25, 0.1, ...

def help():
    print """timer.py
Version: %s
by David Krause
baradock@gmx.de

eg usage:

q {enter} : quit/exits the timer program
h {enter} : this help 
fit {enter} : will try to fit console window to size, windows/linux !EXPERIMENTAL!

d {enter} : dump timer to a file; will append a timestamp!
l  {enter} : Load last dump from given or defaul file

v  {enter} : Toggle vertical, horizontal view

# feel free to replace 1 with the timer you like to change.
1 {enter} : toggle timer 1
1s {enter} : set minutes for timer 1
1n {enter} : set name for timer 1
1r {enter} : reset timer 1

# the prefix "a" will operate on all timers eg:
a {enter} : toggle all timers
as {enter} : set minutes for all timers
an {enter} : set name for all timers
ar {enter} : reset all timers

ss {enter} : aka super stop stops all timers

""" % _VERSION
# PROGRAM BEGINS!
import time
import threading
import sys
import os
import getpass

shutdown = False # All threads will check this global variable and shuts down when it's set to True

# Printer is the Thread that prints out all the information nicely for you
class Printer(threading.Thread):
    running = True
    vertical = _VERTICAL

    def __init__(self,t=[]):
        threading.Thread.__init__(self)
        self.t=t

    def run(self):
        while True:        
            while self.running:        
                txt=""
                for each in self.t:
                    if self.vertical == True:
                        txt+= "%s \n" % each.getText()                
                    else:
                        txt+= "%s " % each.getText()
                clear()
                sys.stdout.write("%s\r" % txt)
                sys.stdout.flush()
                time.sleep(_REFRESH_RATE)
        if self.running == False:
            time.sleep(1)            

    def suspend(self):
        self.running = False

    def resume(self):
        self.running = True

    def toggleVertical(self):
        self.vertical = 1 - self.vertical


class Timer(threading.Thread):
    name = ""
    id = 0
    
    running = False # Timers not running on startup, should run manually
    seconds = 0

    def suspend(self):
        self.running = False

    def resume(self):
        self.running = True

    def toggle(self):
        self.running= 1 - self.running # this swaps the running variable 

    def reset(self):
        self.seconds = 0    
    
    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def __init__(self,name,id):
        threading.Thread.__init__(self)
        try:
            self.name = name
            self.id   = int(id)
        except:
            print "name oder id nicht angegeben!"

    def run(self):
        while True:
            if self.running == True:
                self.seconds = self.seconds + 1
                #self.text()
                time.sleep(1)
            else:
                time.sleep(1)

    def text(self):
        sys.stdout.write( '%d:%s %s \r\n' % (self.id,self.name,self.seconds ) )
        sys.stdout.flush()

    def getText(self):
        return '#%d:%s %02d:%02d' % (self.id,self.name,(self.seconds/60.0),(self.seconds % 60))

    def setMinutes(self,minutesStr): # sets minutes as you think: 1.30 -> 1Minute 30Seconds
        if minutesStr:        
            try:
                min, sec = minutesStr.split(":")

            except ValueError:
                printer.suspend()
                clear()
                sys.stdout.write('illegal format:"%s" should be eg: 10:43\r')
                sys.stdout.flush()
                time.sleep(3.5)
                printer.resume()
                return False
            self.seconds = int(float(min)*60)+int(sec) # sets the clock
            

    def getMinutes(self):
        return '%d:%d' % ((self.seconds/60.0),(self.seconds % 60))


def dump(t,filename): # dumps all data to given file
    try:
        f = open(filename,"a")
        txt=""
        for each in t:
            txt+= "%s " % each.getText()
        f.writelines("%s -> %s\n" % (time.ctime(),txt))
        f.close()
    except all as e:
        print e
    

def load(t,filename): # loads the las dump from spezified file
    try:
        f = open(filename,"r")
        lastline = f.readlines()[-1] # this will get only the last line
        data = lastline.split("->")[1].strip().split(" ") # skip the cdate format and get only the data (in form '#1:noName','00:11',...,...

        i = 0
        for each in t:
            each.setName(data[i].split(":")[1]) # get name from string and set it for each timer
            i += 1
            each.setMinutes(data[i]) # get value from string and set it
            i += 1
    except IndexError:
        pass # when this except is thrown you have more timers than the file has saved.

    except all as e:
        print e
        
def fit(): # try to set geometry
    if os.name == "nt":
        os.system("mode con cols=180 lines=1")
    elif os.name == "posix":
        #pass        
        os.system("clear")
        
def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        #pass        
        os.system("clear")       


# COMMAND LINE PARSING
# At first look if help is aquired on startup
if ('-h' in sys.argv) or ('--help' in sys.argv) or ('/?' in sys.argv):
    help()
    exit()

if ('-v' in sys.argv) or ('--version' in sys.argv) or ('/v' in sys.argv):
    print _VERSION
    exit()


# Tries to change terminal window size
fit()

# SPAWN ALL THE TIMERS
t = [] # t holds all the timers for the user!
for each in range(_TIMERS_TO_SPAWN): # going to create the timers
    _timer = Timer(_DEFAULT_NAME_OF_TIMERS ,int(each + 1)) # each+1; for easy access via keyboard
    _timer.setDaemon(True) # This will shut down the threads on keyboard interrupt
    _timer.start()
    t.append(_timer)

# START PRINTING THREAD
printer = Printer(t)
printer.setDaemon(True) # This will shut down the threads on keyboard interrupt
printer.start()


# Parsing loop in MAIN THREAD
while True:
    cmd = getpass.getpass("") # use getpass for no response

    if cmd.startswith("q"):
        exit()

    if cmd.startswith("h"):
        printer.suspend()
        help()
        getpass.getpass("press enter for exit help")
        printer.resume()

    if cmd.startswith("d"):
        printer.suspend()
        new_filename = raw_input("dump to [%s]: " % _DEFAULT_DUMP_FILE_NAME )
        if len(new_filename) == 0:
            dump(t,_DEFAULT_DUMP_FILE_NAME)
        else:
            dump(t,new_filename)
        printer.resume()

    if cmd.startswith("l"):
        printer.suspend()
        new_filename = raw_input("load last line from [%s]: " % _DEFAULT_DUMP_FILE_NAME )
        if len(new_filename) == 0:
            load(t,_DEFAULT_DUMP_FILE_NAME)
        else:
            load(t,new_filename)
        printer.resume()

    if cmd.startswith("v"): # toggle vertical
        printer.toggleVertical()

    if cmd.startswith("ss"):
        for each in t:
            each.suspend()

    if cmd.startswith("a"): # operate on all timers
        if cmd.startswith("ar"): # reset all timers
            for each in t:
                each.reset()
        elif cmd.startswith("an"):
            printer.suspend()
            newName=raw_input("Set new name for all: ")
            if len(newName) != 0:
                for each in t:
                    each.setName(newName)
            printer.resume()
        elif cmd.startswith("as"):
            printer.suspend()
            newVal=raw_input("Set new Value for all: ")
            if len(newVal) != 0:
                for each in t:
                    sucess = each.setMinutes(newVal)
                    if sucess == False:
                        break
                    
            printer.resume()      
        elif cmd.startswith("a"):
            for each in t:
                each.toggle() # this swaps the running variable 
        
    for each in t:
        if cmd.startswith("%sr" % each.id): #reset 1r, 2r ... + enter
            each.reset()

        elif cmd.startswith("%sn" % each.id): #set name 1n, 2n ... + enter
            printer.suspend()
            newName=raw_input("Set new Name for #%d %s: " % (each.id,each.getName()))
            if len(newName) != 0:
                each.setName(newName)
            printer.resume()

        elif cmd.startswith("%ss" % each.id): #set timer 1s, 2s ... + enter
            printer.suspend()
            newVal=raw_input("Set new Value for #%d %s(%s): " % (each.id,each.getName(),each.getMinutes()))
            if len(newVal) != 0:
                each.setMinutes(newVal)
            printer.resume()            

        elif cmd.startswith(str(each.id)): # set running 1,2,3... + enter
            each.toggle() # this swaps the running variable 

    time.sleep(0.5)
