from sys import *
from subprocess import *

print "executing", argv[1]

if argv[1] == "cache":
    call("python -m RocketBooster.F1Engine.J2Engine.cache")