mport sys
import re
import os
import getopt
from sets import Set
from  myexceptions import *
from bdrmap_parse import * 

routers = []
interface2rtr = {}
interface2name = {}

filename = str(sys.argv[1])
(routers,interface2rtr,interface2name) = read_bdrmap_file(filename)
print(routers[0])

