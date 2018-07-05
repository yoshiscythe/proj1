#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
def Help():													#-helpをつけてやると呼び出せる
  return '''First script.
  Usage: template'''
def quaternion(axis, angle):
	return [i*math.sin(angle/2) for i in axis]+[math.cos(angle/2)]
def Run(ct,*args):
	#（moveq 1）と同じ位置姿勢
	q_init = [-0.02225494707637879, 0.027604753814144237, 0.02256845844164128, -2.2001560115435073, -0.00047772651727832574, 0.6569580325147487, 0.0010119170182285682]
	
	
	grip_open = 0.10
	
	grip_close = 0.055
	
	#手先からグリッパの中心までの距離
	distance_to_gripper = 0.1
	
	#カップのつかむ高さz
	catch_height = 0.07
	
	#table_height
	table_height = 0.12
	
	#カップのある位置(x,y,z)口の中心
	x_cup = [0.35, 0.45, 0.0+table_height]
	
	#カップを置きたい位置(x,y,z)
	x_goal = [-0.45, 0.45, 0.0+table_height]
	
	#カップを持つ姿勢
	#axis = [1.0, 0.0, 0.0]
	#angle = -math.pi/2
	#quaternion_cup = quaternion(axis, angle)
	quaternion_cup = [-0.5, 0.5, 0.5, 0.5]
	
	#print x_cup+quaternion_cup
	
	ct.robot.MoveToQ(q_init, 10, blocking=True)	#初期化
	ct.robot.OpenGripper()
	
	x1 = copy.deepcopy(x_cup[:3])+quaternion_cup
	
	x1[2] = 0.5
	x1[1] -= 0.05
	print '1',x1
	ct.robot.MoveToX(x1, 16.0, blocking=True)
	rospy.sleep(1.0)
	
	x1[2] = copy.deepcopy(x_cup[2])+catch_height
	print '2',x1
	ct.robot.MoveToXI(x1, 9.0, blocking=True)
	rospy.sleep(1.0)
	
	x1[1] += 0.05
	print '3',x1
	ct.robot.MoveToXI(x1, 5.0, blocking=True)
	rospy.sleep(1.0)
	
	#ct.robot.MoveGripper(float(grip_close))
	#rospy.sleep(1.0)
	
	#x1[2] = 0.5
	#print '4',x1
	#ct.robot.MoveToXI(x1, 10.0, blocking=True)
	#rospy.sleep(1.0)
	
	#x1[:2] = x_goal[:2]
	#ct.robot.MoveToXI(x1, 5.0, blocking=True)			#ct.robot.MoveToXI（ｘ，ｄｔ，） 間を直線で補間してくれるinum=　　で引数渡してやると補間点数が可変
	
	#x1[2] = 0.1
	##print x1
	#ct.robot.MoveToX(x1, 5.0, blocking=True)
	
	#x1[1] -= 0.1
	#ct.robot.MoveToX(x1, 5.0, blocking=True)
	
	#ct.robot.MoveGripper(float(grip_open))
	
	#ct.robot.MoveToQ(q_init, 5.0, blocking=True)	#初期化
	
	
