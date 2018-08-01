#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
def Help():
  return '''First script.
  Usage: template'''

def Run(ct,*args):
  q_init2 = [1.5485366582870483, 0.027594611048698425, 0.022554073482751846, -2.2001535892486572, -0.00047082576202228665, 0.6569538116455078, 0.0009925758931785822]
  ct.robot.MoveToQ(q_init2, 5.0)