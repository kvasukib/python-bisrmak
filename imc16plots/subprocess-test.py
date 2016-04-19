import sys
import re
import os
import getopt
import subprocess
from sets import Set
from  myexceptions import *
ip_formatted = "'69.241.8.114'"
filename = 'this-fil.test'
subprocess.call(["echo", ip_formatted, ">", filename])
