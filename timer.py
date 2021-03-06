#!/usr/bin/env python
_VERSION = "0.9.8.1+config"

import time
import threading
import sys
import os
import getpass
import re
import ConfigParser

DEFAULTS ={
"TIMERS_TO_SPAWN" : 1 ,     # How many timers you need? (values between 1-9)
"DEFAULT_NAME_OF_TIMERS" : "noName" ,# the default name of the timers (can change it later)
"DEFAULT_DUMP_FILE_NAME" : {"posix":"/tmp/timer.dump","nt":"./timer.dump"}, # the default file for dumping each timer posix:linux,unix,etc nt:windows
"VERTICAL" : False, # False/True if this is True the timers are shown vertical istead of horizontal
"REFRESH_RATE" : 1 ,# Seconds to sleep between the refresh could also eg. 0.5, 0.25, 0.1, ...
"AUTO_RESIZE_WINDOW" : True, # this currently works only on NT / WINDOWS

# ativates the autodump on every aktion on the timers.
# HINT hit {enter} in the program will dump the current state of the timers
"AUTO_DUMP_ON_CHANGE" : True, # True aktivates the AUTO DUMP
"AUTO_DUMP_FILE" : {"posix":"/tmp/timer.autodump","nt":"./timer.autodump"}, # dump path

"ERROR_DUMP_FILE" : {"posix":"/tmp/timer.autodump","nt":"./timer.errordump"},

"DEFAULT_HEIGHT": 1, # WINDOWS ONLY ATM
"DEFAULT_WIDTH" :100, # also only M$ Win
"DEFAULT_COLOR" : "A", # and also only M$ Win (color "A" is a hackisch matrix green)

"ACTION_TIMER" : True, # when this is set to true the default action will be called, else the timer bells visually
"DEFAULT_BELL_TIME" : 5,    

}

config = ConfigParser.ConfigParser(DEFAULTS)

# USERCONFIG
_TIMERS_TO_SPAWN = 1      # How many timers you need? (values between 1-9)
_DEFAULT_NAME_OF_TIMERS = "noName" # the default name of the timers (can change it later)
_DEFAULT_DUMP_FILE_NAME = {"posix":"/tmp/timer.dump","nt":"./timer.dump"} # the default file for dumping each timer posix=linux,unix,etc nt=windows
_VERTICAL = False # False/True if this is True the timers are shown vertical istead of horizontal
_REFRESH_RATE = 1 # Seconds to sleep between the refresh could also eg. 0.5, 0.25, 0.1, ...
_AUTO_RESIZE_WINDOW = True # this currently works only on NT / WINDOWS

# ativates the autodump on every aktion on the timers.
# HINT hit {enter} in the program will dump the current state of the timers
_AUTO_DUMP_ON_CHANGE = True # True aktivates the AUTO DUMP
_AUTO_DUMP_FILE = {"posix":"/tmp/timer.autodump","nt":"./timer.autodump"} # dump path

_ERROR_DUMP_FILE = {"posix":"/tmp/timer.autodump","nt":"./timer.errordump"}

_DEFAULT_HEIGHT= 1 # WINDOWS ONLY ATM
_DEFAULT_WIDTH =100 # also only M$ Win
_DEFAULT_COLOR = "A" # and also only M$ Win (color "A" is a hackisch matrix green)

_ACTION_TIMER = True # when this is set to true the default action will be called, else the timer bells visually
_DEFAULT_BELL_TIME = 5

_SPACE_TO_WRITE = '#'*10

def _DEFAULT_ACTION_ON_TIMER_BELL(): #

    if os.name == "posix":
        os.system("mplayer /home/david/Musik/vadd1.wav > /dev/null 2> /dev/null &")
    elif os.name == "nt":
        os.system('"C:/Program Files/VideoLAN/VLC/vlc.exe"  ')

helpstr = """timer.py
Version: %s
by David Krause
kekschaot@gmail.com

timer.py is a small console based timer application.
Its able to spawn a "no limited" amounth of timers wich are all stoppable by its own.
Its supports autodump and it's able to count backwards and execute a abitrary command (pizza mode) when time is over

eg usage:

q {enter}   : quit/exits the timer program
h {enter}   : this help
fit {enter} : will try to fit console window to size, windows/linux !EXPERIMENTAL!

d {enter}   : dump timer to a file; will append a timestamp!
l  {enter}  : Load last dump from given or defaul file

p  {enter}  : Toggle printing / refreshing (usefull for copy'n pasteing from terminal)
v  {enter}  : Toggle vertical, horizontal view

# feel free to replace 1 with the timer you like to change. eg "6s {enter}" or "57s {enter}"
1 {enter}   : toggle timer 1
1s {enter}  : set minutes for timer 1
1n {enter}  : set name for timer 1
1r {enter}  : reset timer 1

1i {enter}  : reverse timer 1 # if _ACTION_TIMER = True, execute _DEFAULT_ACTION_ON_TIMER_BELL()

# the prefix "a" will operate on all timers eg:
a {enter}   : toggle all timers
as {enter}  : set minutes for all timers
an {enter}  : set name for all timers
ar {enter}  : reset all timers

ss {enter}  : aka super stop stops all timers
sss {enter} : aka super stop stops all timers and also set default name

n {enter}   : span new timer
b {enter}   : remove the last timer 


""" % _VERSION

# PROGRAM BEGINS!
def raw_input_fit(prompt):
    fit(prompt+_SPACE_TO_WRITE)
    newName=raw_input(prompt)
    return newName


def setColor(color):
    if os.name == "nt":
        os.system("color "+color)

def help(): # dummy fuction prints the help, and also tries to fit the terminal
    fit(helpstr)
    print helpstr

def copyToClipboard(cstr):
    from Tkinter import Tk
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(cstr)
    r.destroy()    

class Printer(threading.Thread):
    """  Printer is the Thread that prints out all the information nicely for you """
    running = True
    vertical = _VERTICAL

    def __init__(self,timers=[]): # timers are the timer threads
        threading.Thread.__init__(self) # needed for threading
        self.timers=timers

    def run(self): # main printing thread
        while True:
            oldtxt="" # used to suppress unecessary prints
            while self.running:
                txt=""
                for each in self.timers:
                    if self.vertical == True:
                        txt+= "%s \n" % each.getText()
                    else:
                        txt+= "%s " % each.getText()
                if txt != oldtxt:
                    if _AUTO_RESIZE_WINDOW == True:
                        fit(txt)
                    sys.stdout.write("%s\r" % txt)
                    sys.stdout.flush()
                oldtxt = txt
                if self.once == True:
                    self.once = False # to the next run will be a normal run
                    self.running = False # stop afterwards
                    break
                else:
                    time.sleep(_REFRESH_RATE)
        if self.running == False:
            time.sleep(1)

    def once(self):
        """ prints only once, timer will be stopped afterwards """
        self.once = True
        self.resume()


    def suspend(self):
        self.running = False

    def resume(self):
        self.running = True

    def toggleSuspend(self):
        if self.running == False:
            self.running = True
        else:
            self.running = False

    def toggleVertical(self):
        self.vertical = 1 - self.vertical


class Timer(threading.Thread):
    name = ""
    id = 0 

    global printer

    running = True # Timers threads "run" all the time BUT timers counting;this is set to false when the stop() function is called
    counting = False #Timers not counting&running on startup, should run manually
    reverse = False # Timers should not run backwards as default
    seconds = 0

    def suspend(self):
        autoDump()
        self.counting = False

    def resume(self):
        self.counting = True

    def toggle(self):
        self.counting= 1 - self.counting # this swaps the running variable

    def toggleReverse(self):
        self.reverse= 1 - self.reverse

    def setReverse(self,reverse):
        self.reverse= reverse

    def getReverse(self): # dirty hack to display the reverse everywhere in the program
        if self.reverse == True:
            return "R"
        else:
            return ""

    def reset(self):
        self.seconds = 0

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = re.sub('\s+',"_",name)



    def __init__(self,name,id):
        threading.Thread.__init__(self)
        try:
            self.name = name
            self.id   = int(id)
        except:
            print "name oder id nicht angegeben!"
    def stop(self):
        self.running = False
        return 0

    def run(self):
        while self.running:
            if self.counting == True:
                if self.reverse == True:
                    self.seconds = self.seconds - 1
                    if self.seconds  <= 0:
                        self.counting = False
                        self.seconds = 0
                        self.reverse = False
                        try:
                            if _ACTION_TIMER == True:
                                _DEFAULT_ACTION_ON_TIMER_BELL()
                            self.visualBell("BELL from [%s] BELL" % self.getText())
                        except all as e:
                            print e
                            printer.suspend()
                else:
                    self.seconds = self.seconds + 1
                time.sleep(1)
            else:
                time.sleep(1)

    def visualBell(self,str):
        printer.suspend()
        for i in range(_DEFAULT_BELL_TIME):
            for each in range(3):
                clear()
                sys.stdout.write("%s%s\r" % (str , each*"!!"))
                sys.stdout.flush()
                time.sleep(0.5)
        printer.resume()

    def getText(self):
        fstr = '#%s%'+str(len(str(_TIMERS_TO_SPAWN)))+'d:%s %02d:%02d'
        return fstr % (self.getReverse(),self.id,self.name,(self.seconds/60.0),(self.seconds % 60))

    def setMinutes(self,minutesStr): # sets minutes as you think: 1:30 -> 1Minute 30Seconds
        if minutesStr:
            try:
                if "-" in minutesStr: # nah just positive values allowed
                    raise(ValueError)
                min, sec = minutesStr.split(":")
            except ValueError:
                printer.suspend()
                clear()
                sys.stdout.write('illegal format:"%s" should be eg: 10:43\r' % minutesStr)
                sys.stdout.flush()
                time.sleep(3.5)
                printer.resume()
                return False
            self.seconds = int(float(min)*60)+int(sec) # sets the clock

    def getMinutes(self):
        return '%d:%d' % ((self.seconds/60.0),(self.seconds % 60))

def log(log,filename): # only writes what it gets to file
    try:
        f = open(filename, "a")
        f.writelines(log)
        f.close()
    except all as e:
        print e
        exit()

def dump(timers,filename): # dumps all data to given file
        f = open(filename,"a")
        txt=""
        for each in timers:
            txt+= "%s " % each.getText()
        txt =  "%s -> %s\n" % (time.ctime(),txt)
        log(txt,filename)

def autoDump():
    if _AUTO_DUMP_ON_CHANGE == True:
       dump(timers,_AUTO_DUMP_FILE[os.name]) # calls dump with the autodump path

def load(timers,filename): # loads the las dump from spezified file
    try:
        f = open(filename,"r")
        lastline = f.readlines()[-1] # this will get only the last line
        data = lastline.split("->")[1].strip().split(" ") # skip the cdate format and get only the data in form '#1:noName','00:11',...,...
        i = 0
        for each in timers:
            each.setName(data[i].split(":")[1]) # get name from string and set it for each timer
            i += 1
            each.setMinutes(data[i]) # get value from string and set it
            i += 1
    except IndexError:
        pass # when this except is thrown you have more timers than the file has saved, but we dont care LOL.
    except IOError as e:
        printer.suspend()
        clear()
        sys.stdout.write('Could not load from: %s -> [%s]\r'% (_DEFAULT_DUMP_FILE_NAME[os.name],e) )
        sys.stdout.flush()
        time.sleep(3.5)
        printer.resume()
    except all as e:
        print e

def fit(str=""): # try to set geometry, based on given str
    if _AUTO_RESIZE_WINDOW == True:
        if os.name == "nt":
            if len(str) != 0:
                lines = str.split("\n")
                height = len(lines)
                max = 0
                for each in lines:
                    if len(each) > max:
                        max = len(each)
                width = max
                os.system("mode con cols=%d lines=%d" % (width+1,height+1))
            else:
                os.system("mode con cols=%d lines=%d" %(_DEFAULT_WIDTH,_DEFAULT_HEIGHT))

        elif os.name == "posix":
            pass
            #os.system("clear")

def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
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
timers = [] # timers holds all the timers for the user!

def spawnTimer(number):
    _timer = Timer(_DEFAULT_NAME_OF_TIMERS ,int(len(timers) + 1)) # number+1; for easy access via keyboard
    _timer.setDaemon(True) # This will shut down the threads on keyboard interrupt
    _timer.start()
    timers.append(_timer)
def remTimer(number):
    timers[number].stop()
    del(timers[number])  



for each in range(_TIMERS_TO_SPAWN): # going to create the timers
    spawnTimer(each)


# START PRINTING THREAD
printer = Printer(timers)
printer.setDaemon(True) # This will shut down the threads on keyboard interrupt
printer.start()

# First Autodump on Startup
autoDump()

setColor(_DEFAULT_COLOR)

# Parsing loop in MAIN THREAD,parse
while True:
    cmd = getpass.getpass("") # use getpass for no response
    autoDump() # auto dump on EVERY user command (also illegal) TODO brainwave aquired
    if cmd.startswith("q"):
        exit()

    elif cmd.startswith("c"):
        printer.suspend()
        fit("set color to? (default %s)  " % _DEFAULT_COLOR)
        setColor(raw_input_fit("set color to? (default %s):" % _DEFAULT_COLOR))
        printer.resume()
    
    elif cmd.startswith("p"): # toggle printer
        printer.toggleSuspend()


    #elif cmd.startswith(""):
    #    copyToClipboard(printer.
        
    elif cmd.startswith("n"): # spawn new timer
        spawnTimer(len(timers)-1)

    elif cmd.startswith("b"): # remove a timer
        remTimer(len(timers)-1)

    elif cmd.startswith("h"): # display in programm help, timers'll still run
        printer.suspend()
        help()
        getpass.getpass("press enter for exit help")
        printer.resume()

    elif cmd.startswith("d"): # dump to given file
        printer.suspend()
        new_filename = raw_input_fit("dump to [%s]: " % _DEFAULT_DUMP_FILE_NAME[os.name] )
        if len(new_filename) == 0:
            dump(timers,_DEFAULT_DUMP_FILE_NAME[os.name])
        else:
            dump(timers,new_filename)
        printer.resume()

    elif cmd.startswith("l"): # load from the last line
        printer.suspend()
        new_filename = raw_input_fit("load last line from [%s]: " % _DEFAULT_DUMP_FILE_NAME[os.name] )
        if len(new_filename) == 0:
            load(timers,_DEFAULT_DUMP_FILE_NAME[os.name])
        else:
            load(timers,new_filename)
        printer.resume()
        autoDump()

    elif cmd.startswith("v"): # toggle vertical
        printer.toggleVertical()

    elif cmd.startswith("sss"):
        for each in timers:
            each.reset()
            each.suspend()
            each.setReverse(0)
            each.setName(_DEFAULT_NAME_OF_TIMERS)

    elif cmd.startswith("ss"): # super stop stops all timers
        for each in timers:
            each.suspend()

    elif cmd.startswith("a"): # operate on all timers
        if cmd.startswith("ar"): # reset all timers
            for each in timers:
                each.reset()
        elif cmd.startswith("ai"): # all timers run backwards
            for each in timers:
                each.toggleReverse()
            autoDump()
        elif cmd.startswith("an"):
            printer.suspend()
            newName=raw_input_fit( "Set new name for all: ")
            if len(newName) != 0:
                for each in timers:
                    each.setName(newName)
            printer.resume()
            autoDump()
        elif cmd.startswith("as"):
            printer.suspend()
            newVal=raw_input_fit("Set new Value for all: ")
            if len(newVal) != 0:
                for each in timers:
                    sucess = each.setMinutes(newVal)
                    if sucess == False:
                        break
            printer.resume()
            autoDump()
        elif cmd.startswith("a"):
            for each in timers:
                each.toggle() # this swaps the running variable

    else:

        """ 
            when the commandline begins with a NUMBER 
        """
        
        for each in timers:
            """ Reset timer """
            if cmd.startswith("%sr" % each.id): #reset 1r, 2r ... + enter
                each.reset()

             
            elif cmd.startswith("%si" % each.id):
                """ Inverse timers , make timers run backwards """
                each.toggleReverse()
                if each.reverse == True: # if reverse is True after toggle set new counter value
                    printer.suspend()
                    clear()
                    newVal=raw_input_fit("Set val to count backwards for #%s%d %s: " % (each.getReverse(),each.id,each.getName()))
                    each.setMinutes(newVal)
                    printer.resume()

            elif cmd.startswith("%sn" % each.id): #set name 1n, 2n ... + enter
                """ Set name for n'th counter """
                printer.suspend()
                clear()
                newName=raw_input_fit("Set new Name for #%s%d %s: " % (each.getReverse(),each.id,each.getName()))
                if len(newName) != 0:
                    each.setName(newName)
                printer.resume()

            elif cmd.startswith("%ss" % each.id): #set timer 1s, 2s ... + enter
                """ Set new value vor counter """   
                printer.suspend()
                clear()
                newVal=raw_input_fit("Set new Value for #%s%d %s(%s): " % (each.getReverse(),each.id,each.getName(),each.getMinutes()))
                if len(newVal) != 0:
                    each.setMinutes(newVal)
                printer.resume()

            elif cmd.startswith(str(each.id)): # set running 1,2,3... + enter
                """ Toggle timers eg: number <enter> """
                each.toggle() # this swaps the running variables
