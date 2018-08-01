#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
import tower_make
import start_tower
import time
def Help():													#-helpをつけてやると呼び出せる
  return '''First script.
  Usage: template'''
def quaternion(axis, angle):
	return [i*math.sin(angle/2) for i in axis]+[math.cos(angle/2)]
	
#グリッパの開閉距離
grip_open = 0.075	
grip_close = 0.058

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
catch_margin = 0.10	

#
table_height = 0.15

#（moveq 1）と同じ位置姿勢
q_init1 = [-0.022, 0.027, 0.022, -2.200, -0.0004, 0.656, 0.001]

#original init (pi/2 from moveq 1)
q_init2 = [2.300, 0.037, -0.741, -2.200, 0.019, 0.657, -0.040]

def arm_speed(ct, next_pos):
  speed = 0.20
  current_pos = list(ct.robot.FK())
  distance = 0
  
  for i in range(3):
    distance += (current_pos[i]-next_pos[i])**2
  
  if distance <= 0.001:
    #print 'pos match\n'
    return 1
  else:
    #print 'pos mismatch\n'
    return math.sqrt(distance)/speed

def sleep(ct):
  a = 0
  while(1):
    current = list(ct.robot.Q())
    if a == current:
      print 'OK'
      break
    rospy.sleep(0.05)
    a = copy.deepcopy(current)
    print 'yet'
  return

def start_goal(ct, start, goal):
	x1 = copy.deepcopy(start[:3])+quaternion_cup
	
	print 0
	x1[2] = 0.45
	x1[1] -= catch_margin
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	
	print 1
	x1[2] = copy.deepcopy(start[2])+catch_height
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	
	print 1.1
	x1[1] += catch_margin
	ct.robot.MoveGripper(float(grip_open))
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	
	print 2
	#つかむ
	rospy.sleep(1.0)
	ct.robot.MoveGripper(float(grip_close))
	
	#x1[2] = 0.40
	##rospy.sleep(1.0)
	#sleep(ct)
	#ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	
	#x1[2] = 0.50
	##rospy.sleep(1.0)
	#sleep(ct)
	#ct.robot.MoveToXI(x1, 0.5, blocking=True)
	
	print 3
	x1[2] = 0.45
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	print list(ct.robot.Q())
	
	print 4
	x1[:2] = copy.deepcopy(goal[:2])
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	x1[2] = copy.deepcopy(goal[2]) + catch_height
	#print x1
	#rospy.sleep(3.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, 1.5*arm_speed(ct, x1), blocking=True)
	
	print 5
	#はなす
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveGripper(float(grip_open))	
	
	print 6
	x1[1] -= catch_margin
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	print list(ct.robot.Q())
	
	print 7
	x1[2] =0.45
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
	
	print 8
	
def Run(ct,*args):
	time_start = time.time()
        stage = 2
	
	cup_location = [0.30, 0.55, 0.0+table_height]
	cup_start =  start_tower.start_tower(cup_location, stage)
 	
 	cup_goal_set = [-0.35, 0.45, 0.0+table_height]
	cup_goal = tower_make.tower_make(cup_goal_set, stage)
	
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToQ(q_init2, 8.0, blocking=True)	#初期化	
	ct.robot.MoveGripper(float(grip_open))
	
	for i in range(len(cup_start)):
		print 'sequence:', i+1
		if i != 0:
		  #rospy.sleep(3.0)
		  sleep(ct)
		  print 'a'
		  ct.robot.MoveToQ(q_init2, 1.5*arm_speed(ct, list(ct.robot.FK(q_init2))), blocking=True)	#初期化	
		print 'b'
		ct.robot.MoveGripper(float(grip_open))
		print 'c'
		start_goal(ct, cup_start[i], cup_goal[i])
		print 'd'
	
	#rospy.sleep(1.0)
	sleep(ct)
	ct.robot.MoveToQ(q_init2, 1.5*arm_speed(ct, list(ct.robot.FK(q_init2))), blocking=True)	#初期化
	
	elapsed_time = time.time()-time_start
	print 'elapsed time is', int(elapsed_time//60), '[m]', int(elapsed_time%60), '[s]\n'
