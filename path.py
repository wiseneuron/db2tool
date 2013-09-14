#!/usr/bin/python
# author Chunhui Li wiseneuron@gmail.com
import os
def path(sys):
    root = os.path.abspath(os.path.dirname(sys.argv[0]))
    root = root.replace('\\', '/')
    return root
