#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
import tower_make
def Help():													#-helpをつけてやると呼び出せる
  return '''First script.
  Usage: template'''
def quaternion(axis, angle):
	return [i*math.sin(angle/2) for i in axis]+[math.cos(angle/2)]
	
#グリッパの開閉距離
grip_open = 0.075	
grip_close = 0.055

#カップを持つ姿勢
#axis = [1.0, 0.0, 0.0]
#angle = -math.pi/2
#quaternion_cup = quaternion(axis, angle)
quaternion_cup = [-0.5, 0.5, 0.5, 0.5]

#手先からグリッパの中心までの距離
distance_to_gripper = 0.1

#カップのつかむ高さz
catch_height = 0.07

#つかむ時のマージン
catch_margin = 0.05	

#
table_height = 0.12

#（moveq 1）と同じ位置姿勢
q_init1 = [-0.022, 0.027, 0.022, -2.200, -0.0004, 0.656, 0.001]

#original init (pi/2 from moveq 1)
q_init2 = [2.300, 0.037, -0.741, -2.200, 0.019, 0.657, -0.040]
	
def start_goal(ct, start, goal):
	x1 = copy.deepcopy(start[:3])+quaternion_cup
	
	x1[2] = 0.5
	x1[1] -= catch_margin
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 5.0, blocking=True)
	
	x1[2] = copy.deepcopy(start[2])+catch_height
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 5.0, blocking=True)
	x1[1] += catch_margin
	ct.robot.MoveGripper(float(grip_open))
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	
	#つかむ
	rospy.sleep(1.0)
	ct.robot.MoveGripper(float(grip_close))
	
	x1[2] = 0.5
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 5.0, blocking=True)
	
	x1[:2] = copy.deepcopy(goal[:2])
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 3.0, blocking=True)
	x1[2] = copy.deepcopy(goal[2]) + catch_height
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 5.0, blocking=True)
	
	#はなす
	rospy.sleep(1.0)
	ct.robot.MoveGripper(float(grip_open))	
	
	x1[1] -= catch_margin
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
	
	x1[2] =0.5
	rospy.sleep(1.0)
	ct.robot.MoveToXI(x1, 2.0, blocking=True)
def Run(ct,*args):
        stage = 2
  
	cup_start =  [[ 0.35, 0.45, 0.0+table_height],
		      [ 0.27, 0.45, 0.0+table_height],
		      [ 0.19, 0.45, 0.0+table_height]]
 	
 	cup_goal_set = [-0.40, 0.45, 0.0+table_height]
	cup_goal = tower_make.tower_make(cup_goal_set, stage)
	
	rospy.sleep(1.0)
	ct.robot.MoveToQ(q_init1, 5.0, blocking=True)	#初期化	
	ct.robot.MoveGripper(float(grip_open))
	
	for i in range(len(cup_start)):
		rospy.sleep(1.0)
		ct.robot.MoveToQ(q_init2, 3.0, blocking=True)	#初期化	
		ct.robot.MoveGripper(float(grip_open))
		start_goal(ct, cup_start[i], cup_goal[i])	
	
	rospy.sleep(1.0)
	ct.robot.MoveToQ(q_init1, 5.0, blocking=True)	#初期化
