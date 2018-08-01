#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
def Help():
  return '''First script.
  Usage: template'''

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

def Run(ct,*args):
  #q_init2 = [2.300, 0.037, -0.741, -2.200, 0.019, 0.657, -0.040]
  #ct.robot.MoveToQ(q_init2, 5.0)
  
  #print 1
  ##sleep(ct)
  ##rospy.sleep(5.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0.1, 0, 0, 0, 0, 0, 0]), 0.5)
  ##sleep(ct)
  #rospy.sleep(1.0)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([-0.1, 0, 0, 0, 0, 0, 0]), )
  
  #print 2
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0.1, 0, 0, 0, 0, 0]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, -0.1, 0, 0, 0, 0, 0]), 1.0)
  
  #print 3
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0.1, 0, 0, 0, 0]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, -0.1, 0, 0, 0, 0]), 1.0)
  
  #print 4
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0.1, 0, 0, 0]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, -0.1, 0, 0, 0]), 1.0)
  
  #print 5
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, 0.1, 0, 0]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, -0.1, 0, 0]), 1.0)
  
  #print 6
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, 0.1, 0]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, -0.1, 0]), 1.0)
  
  #print 7
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, 0, 0.1]), 1.0)
  ##sleep(ct)
  #rospy.sleep(1.5)
  #ct.robot.MoveToQ(list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, 0, -0.1]), 1.0)
  
  q_traj = [list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0.1, 0, 0, 0, 0, 0, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0.1, 0, 0, 0, 0, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0, 0.1, 0, 0, 0, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0, 0, 0.1, 0, 0, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0, 0, 0, 0.1, 0, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, 0.1, 0]),
	    list(ct.robot.Q()),
	    list(ct.robot.Q())+np.array([0, 0, 0, 0, 0, 0, 0.1]),
	    list(ct.robot.Q())						]
  t_traj = [0.0]
  for i in range(14):
    t_traj.append(0.5*(i+1))
    
  #print q_traj
  #print t_traj
  
  ct.robot.FollowQTraj(q_traj, t_traj)
  
  rospy.sleep(t_traj[14])
  ct.robot.MoveGripper(0.0)
  rospy.sleep(1.0)
  ct.robot.MoveGripper(1.0)