#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
def Help():													#-helpをつけてやると呼び出せる
  return '''First script.
  Usage: template'''
def quaternion(axis, angle):
	return [i*math.sin(angle/2) for i in axis]+[math.cos(angle/2)]
	
#グリッパの開閉距離
grip_open = 0.10	
grip_close = 0.04

#カップを持つ姿勢
axis = [1.0, 0.0, 0.0]
angle = -math.pi/2
quaternion_cup = quaternion(axis, angle)

#手先からグリッパの中心までの距離
distance_to_gripper = 0.1

#カップのつかむ高さz
catch_height = [0.05]

#つかむ時のマージン
catch_margin = 0.1	

#（moveq 1）と同じ位置姿勢
q_init = [-0.02225494707637879, 0.027604753814144237, 0.02256845844164128, -2.2001560115435073, -0.00047772651727832574, 0.6569580325147487, 0.0010119170182285682]
	
def start_goal(ct, start, goal):
	x1 = copy.deepcopy(start[:3])+quaternion_cup
	x1[2] += catch_height[0]
	
	x1[1] -= catch_margin
	ct.robot.MoveToX(x1, 2.0, blocking=True)
	x1[1] += catch_margin
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	
	#つかむ
	ct.robot.MoveGripper(float(grip_close))
	
	x1[2] += 0.5
	ct.robot.MoveToXI(x1, 2.0, blocking=True)	
	x1[:2] = copy.deepcopy(goal[:2])
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	x1[2] = goal[2] + catch_height[0]
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	
	#はなす
	ct.robot.MoveGripper(float(grip_open))	
	
	x1[1] -= catch_margin
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	
	x1[2] +=0.5
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
def Run(ct,*args):
	cup_start =  [[ 0.45, 0.45, 0.0],
	 							[ 0.35, 0.45, 0.0],
	 							[ 0.25, 0.45, 0.0]]
 							
	cup_goal =   [[-0.25, 0.45, 0.0],
								[-0.35, 0.45, 0.0],
								[-0.30, 0.45, 0.10]]
	
							
	for i in range(len(cup_start)):
		ct.robot.MoveToQ(q_init, 2.0, blocking=True)	#初期化	
		start_goal(ct, cup_start[i], cup_goal[i])
	ct.robot.MoveToQ(q_init, 2.0, blocking=True)	#初期化
