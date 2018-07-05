#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
def Help():
  return '''First script.
  Usage: template'''

def Run(ct,*args):
  #print len(args)
  #print args[0]
  #q = list(ct.robot.Q())            #ct.robot.Q()関節角を取得、タプルになっていて変更できないのでlist()でくくる
  #print q
  #q[3] += 0.2
  #print q
  #ct.robot.MoveToQ(q, 2.0)          #関節を動かす（関節の角度、　何秒で動かすか）
  
  #x = list(ct.robot.FK())     #手先の座標取得   
  #print x
  #x[0] += 0.1
  #print x
  #ct.robot.MoveToX(x, 2.0)              #手先を動かす（座標、時間）
  
  #x = list(ct.robot.FK())     #手先の座標取得   
  #print x
  #for i in range(10):
    #x[0] += 0.1
    #ct.robot.MoveToX(x, 2.0, blocking=Ture)              #手先を動かす（座標、時間）
    #x[0] -= 0.1
    #ct.robot.MoveToX(x, 2.0, blocking=Ture)              #手先を動かす（座標、時間）
    
  #q = list(ct.robot.Q())
  #q_traj = []
  #t_traj = []
  #q_traj.append(q)
  #t_traj.append(0.0)
  #for i in range(1, 20):
    #t_traj.append(0.1*i)
    #q2 = copy.deepcopy(q)
    #q2[2] += 0.5*math.sin(10.0*0.1*i) 
    #q_traj.append(q2)
  #print t_traj
  #print q_traj
  #ct.robot.FollowQTraj(q_traj, t_traj)
  
  #手先が円を描く
  r = 0.1
  x = list(ct.robot.FK())
  x1 = copy.deepcopy(x)
  x1[1] -= r
  ct.robot.MoveToX(x1, 1.0,  blocking=True)
  x_traj = []
  t_traj = []
  x_traj.append(x1)
  t_traj.append(0.0)
  for i in range(1, 50):
    t_traj.append(0.1*i)
    x2 = copy.deepcopy(x)
    x2[1] += -r*math.cos(3.0*0.1*i)
    x2[2] += r*math.sin(3.0*0.1*i) 
    x_traj.append(x2)
  print t_traj
  print x_traj
  ct.robot.FollowXTraj(x_traj, t_traj)
    
  
