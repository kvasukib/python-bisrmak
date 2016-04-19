import sys
import re
import os
import getopt
import subprocess
#import plot_link
from sets import Set
from  myexceptions import *
from bdrmap_parse import *

nothing = subprocess.check_output(['python', 'as_plot_all.py', 'bed-us.Comcast-Netflix.201601.712.far1.ts bed-us.Comcast-Netflix.201601.712.near3.ts bed-us.Comcast-Netflix.201601.712.near5.ts'])
