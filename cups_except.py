#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
import tower_make
import math
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


def arm_speed(ct, next_pos):
  speed = 0.10
  current_pos = list(ct.robot.FK())
  distance = 0
  
  for i in range(3):
    distance += (current_pos[i]-next_pos[i])**2
  
  return math.sqrt(distance)/speed
	
def start_goal(ct, start, goal):
	x1 = copy.deepcopy(start[:3])+quaternion_cup
	
	x1[2] = 0.5
	x1[1] -= catch_margin
        while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	x1[2] = copy.deepcopy(start[2])+catch_height
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	x1[1] += catch_margin
	
        while(1):
          i = 0
          try:
            ct.robot.MoveGripper(float(grip_open))
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	#つかむ
        while(1):
          i = 0
          try:
            ct.robot.MoveGripper(float(grip_close))
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	x1[2] = 0.5
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	x1[:2] = copy.deepcopy(goal[:2])
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	x1[2] = copy.deepcopy(goal[2]) + catch_height
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	#はなす
	while(1):
          i = 0
          try:
            ct.robot.MoveGripper(float(grip_open))
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	x1[1] -= catch_margin
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
	
	x1[2] =0.5
	while(1):
          i = 0
          try:
            ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
            
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
		while(1):
                  i = 0
                  try:
                    ct.robot.MoveToQ(q_init2, 3.0, blocking=True)	#初期化
                    break
                  except:
                    i += 1
                    print ('retry {0}\n', format(i))
                    rospy.sleep(0.1)
		ct.robot.MoveGripper(float(grip_open))
		start_goal(ct, cup_start[i], cup_goal[i])	
    
	while(1):
          i = 0
          try:
            ct.robot.MoveToQ(q_init1, 5.0, blocking=True)	#初期化
            break
          except:
            i += 1
            print ('retry {0}\n', format(i))
            rospy.sleep(0.1)
