timer.py


Small, easy to use, windows/linux, tui python timer for use in service desks and similar.
It's very usefull when you have a busy desktop but also want to keep track of the customerst time.
Which equals money :)

by David Krause
baradock@gmx.de

eg usage:

q {enter} : quit/exits the timer program
h {enter} : this help 
fit {enter} : will try to fit console window to size, windows/linux !EXPERIMENTAL!

d {enter} : dump timer to a file; will append a timestamp!
l  {enter} : Load last dump from given or defaul file

v  {enter} : Toggle vertical, horizontal view

feel free to replace 1 with the timer you like to change. eg "6s {enter}" or "57s {enter}"
1 {enter} : toggle timer 1
1s {enter} : set minutes for timer 1
1n {enter} : set name for timer 1
1r {enter} : reset timer 1

the prefix "a" will operate on all timers eg:
a {enter} : toggle all timers
as {enter} : set minutes for all timers
an {enter} : set name for all timers
ar {enter} : reset all timers

ss {enter} : aka super stop stops all timers
sss {enter} : aka super stop stops all timers and also set default name
