from sys import stdin
import re
import math


##g = [ [True, True, False, False], [False, True, True, False]]
##p = [ [True, True, False, False], [True, True, False, False]]
##b = [ [False, True, True, False], [True, True, False, False]]
##v = [ [True, True, True, False], [False, False, True, False]]
##l = [ [False, False, True, False], [True, True, True, False]]
##r = [ [True, True, True, True], [False, False, False, False]]
##y = [ [True, True, True, False], [False, True, False, False]]


def addItem(chart, L):
    L1 = [1,1,1]
    L2 = [L,L,L]
    S1 = [1,L-1,1]
    T1 = [1,1,L-1]
    T2 = [L-1,1,L]
    T3 = [L-1,1,1]
    T4 = [L,1,L-1]
    L1 = [L,L,1]
    L2 = [1,1,l-2]
    L3 = [1,L,L]
    L4 = [L-2,1,1]
    L5 = [L,L-1,1]
    L6 = [L,1,1]
    L7 = [1,L-1,L]
    L8 = [1,1,L]
    S1 = [1,L-1,1]
    S2 = [L,1,L]
    S3 = [1,L,1]
    S4 = [L-1,1,L-1]
    
