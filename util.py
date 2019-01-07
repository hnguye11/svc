from __future__ import division
import random
from datetime import datetime
import cPickle as pickle


def print_buffer(buf_name, msg, isWrite=True):
    print "%s %s %s"%(datetime.now(), "write to" if isWrite else "read from", buf_name)
    print msg
    print

    
def print_udp(ip, port, msg, isSend=True):
    if isSend: print "%s send to %s:%d"%(datetime.now(), ip, port)
    else: print "%s recv from :%d"%(datetime.now(), port)
    print msg
    print

    
def rand(lower, upper):
    return lower + (upper - lower) * random.random()


def saveObjectBinary(obj, filename):
    with open(filename, "wb") as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
    print "# " + filename + " saved"


def loadObjectBinary(filename):
    with open(filename, "rb") as input:
        obj = pickle.load(input)
    print "# " + filename + " loaded"
    return obj


def kv_to_str(key, value):
    return "%d,%.6f"%(key, value)


def str_to_kv(msg):
    tmp = msg.split(",")
    return int(tmp[0]), float(tmp[1])
