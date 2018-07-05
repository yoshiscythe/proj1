#!/usr/bin/python
from core_tool import *
def Help():
  return '''Template of script.
  Usage: template'''
def Run(ct,*args):
  x = list(ct.robot.FK())
  x[2] = 0.5
  ct.robot.MoveToXI(x, 5.0)