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

def Run(ct,*args):
	def add_cups_to_attr(cup_locate):
		for i in range(len(cup_locate)):
			x_box= cup_locate[i]+[0.0, 0.0, 0.0, 1.0]
			x_box[1] += 0.20
			box_dim= [0.07,0.07,0.096]
			#Add a box to the planning scene
			box_attr={
					'x': x_box,
					'bound_box': {
					  'dim':box_dim,
					  'center':[0.0,0.0,0.0, 0.0,0.0,0.0,1.0]
					  },
					'shape_primitives': [
					  {
					    'kind': 'rtpkCuboid',
					    'param': [l/2.0 for l in box_dim],  #[half_len_x,half_len_y,half_len_z]
					    'pose': [0.0,0.0,0.0, 0.0,0.0,0.0,1.0],
					    },
					  ],
				}
			#Add box to an internal dictionary:
			ct.SetAttr('box'+str(i),box_attr)
			#Add box to the planning scene:
			ct.SetAttr(TMP,'scene', LUnion(ct.GetAttrOr([],TMP,'scene'),['box'+str(i)]))
		
		#Visualize scene:
		ct.Run('viz','')
	def arm_speed(next_pos):
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

	def sleep():
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
	
	"""
	def start_goal(start, goal):
		x1 = copy.deepcopy(start[:3])+quaternion_cup
	
		print 0
		x1[2] = 0.45
		x1[1] -= catch_margin
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
	
		print 1
		x1[2] = copy.deepcopy(start[2])+catch_height
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
	
		print 1.1
		x1[1] += catch_margin
		ct.robot.MoveGripper(float(grip_open))
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
	
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
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
		print list(ct.robot.Q())
	
		print 4
		x1[:2] = copy.deepcopy(goal[:2])
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
		x1[2] = copy.deepcopy(goal[2]) + catch_height
		#print x1
		#rospy.sleep(3.0)
		sleep()
		ct.robot.MoveToXI(x1, 1.5*arm_speed(x1), blocking=True)
	
		print 5
		#はなす
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveGripper(float(grip_open))	
	
		print 6
		x1[1] -= catch_margin
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
		print list(ct.robot.Q())
	
		print 7
		x1[2] =0.45
		#rospy.sleep(1.0)
		sleep()
		ct.robot.MoveToXI(x1, arm_speed(x1), blocking=True)
	"""
	def collision_move(start, goal, i):
		#Move to the target with planning a collision free path:
		xc = copy.deepcopy(start)
		xc += quaternion_cup
		xc[1] -= catch_margin
		dt= arm_speed(xc)  #Duration
		conservative= False  #Ask Yes/No before moving
		ct.Run('adv.move_to_x', xc, dt, lw_xe, arm, {}, conservative)
		
		xc[1] += catch_margin
		sleep()
		ct.robot.MoveToXI(xc, arm_speed(xc), blocking=True)
		
		#Virtually grasp the object
		ct.Run('scene','grab',arm,'box'+str(i))
		ct.robot.MoveGripper(float(grip_close))
		
		xc[2] += 0.12
		sleep()
		ct.robot.MoveToXI(xc, 2.0, blocking=True)
		
		print 'margin yet'
		xc = copy.deepcopy(goal)
		xc += quaternion_cup
		xc[2] += 0.12
		print '1', xc
		dt= arm_speed(xc)  #Duration
		conservative= False  #Ask Yes/No before moving
		ct.Run('adv.move_to_x', xc, dt, lw_xe, arm, {}, conservative)
		
		print 'margin ?'
		xc[2] -= 0.12
		print '2', xc
		sleep()
		ct.robot.MoveToXI(xc, arm_speed(xc), blocking=True)
		print 'margin ok'
		
		ct.robot.MoveGripper(float(grip_open))
		#Virtually release the object
		ct.Run('scene','release','box'+str(i))
		
		xc[1] -= catch_margin
		sleep()
		ct.robot.MoveToXI(xc, arm_speed(xc), blocking=True)
		
	lw_xe= [0.0,0.0,0.0, 0.0,0.0,0.0,1.0]
	arm= 0
	
	print 8
	time_start = time.time()
        stage = 3
	
	cup_location = [0.30, 0.55, 0.0+table_height]
	cup_start =  start_tower.start_tower(cup_location, stage)
 	
 	cup_goal_set = [-0.35, 0.45, 0.0+table_height]
	cup_goal = tower_make.tower_make(cup_goal_set, stage)
	
	#rospy.sleep(1.0)
	sleep()
	ct.robot.MoveToQ(q_init2, 8.0, blocking=True)	#初期化	
	ct.robot.MoveGripper(float(grip_open))
	
	print 'go'
	add_cups_to_attr(cup_start)
	print 'end'
	
	for i in range(len(cup_start)):
		collision_move(cup_start[i], cup_goal[i], i)
	
	
	"""
	for i in range(len(cup_start)):
		print 'sequence:', i+1
		if i != 0:
		  #rospy.sleep(3.0)
		  sleep()
		  print 'a'
		  ct.robot.MoveToQ(q_init2, 1.5*arm_speed(list(ct.robot.FK(q_init2))), blocking=True)	#初期化	
		print 'b'
		ct.robot.MoveGripper(float(grip_open))
		print 'c'
		start_goal(cup_start[i], cup_goal[i])
		print 'd'
	"""
	
	
	#rospy.sleep(1.0)
	sleep()
	ct.robot.MoveToQ(q_init2, 1.5*arm_speed(list(ct.robot.FK(q_init2))), blocking=True)	#初期化
	
	elapsed_time = time.time()-time_start
	print 'elapsed time is', int(elapsed_time//60), '[m]', int(elapsed_time%60), '[s]\n'
