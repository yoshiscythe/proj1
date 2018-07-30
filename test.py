#!/usr/bin/python
# -*- coding: utf-8 -*-             #日本語を書くためのおまじない
from core_tool import *
import time

def Help():
  return '''First script.
  Usage: template'''

def sleep(ct):
  a = 0
  while(1):
    current = list(ct.robot.Q())
    if a == current:
      break
    rospy.sleep(0.05)
    a = copy.deepcopy(current)
  return

def arm_speed(ct, next_pos):
  speed = 0.30
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

def Run(ct,*args):
  #time_start = time.time()
  
  q_init2 = [2.300, 0.037, -0.741, -2.200, 0.019, 0.657, -0.040]
  #x1 = [0.30, 0.55, 0.50, -0.5, 0.5, 0.5, 0.5]
  
  #print '0:', list(ct.robot.Q())
  #ct.robot.MoveToQ(q_init2, 3.0, blocking=True)	#初期化
  #print '1:', list(ct.robot.Q())
  ##ct.robot.StopMotion()
  ##rospy.sleep(1.0)
  ##a = 0
  ##while(1):
    ##current = list(ct.robot.Q())
    ##if a == current:
      ##break
    ##rospy.sleep(0.1)
    ##a = copy.deepcopy(current)
  #sleep(ct)
  #ct.robot.MoveToXI(x1, 3.0, blocking=True, inum=100)
  #print '2:', list(ct.robot.Q())
  ###ct.robot.StopMotion()
  ##x1[0] = -0.32
  ###a = 0
  ###while(1):
    ###current = list(ct.robot.Q())
    ###if a == current:
      ###break
    ###rospy.sleep(0.1)
    ###a = copy.deepcopy(current)
  ##sleep(ct)
  ##ct.robot.MoveToXI(x1, 3.0, blocking=True)
  ##print '3:', list(ct.robot.Q())
  
  ##q_out = [2.895030975341797, 1.3684132099151611, -0.9679418206214905, -1.8703477382659912, -0.8228060007095337, 0.7685091495513916, -0.5564741492271423]
  
  #elapsed_time = time.time()-time_start
  #print 'elapsed time is', int(elapsed_time//60), '[m]', int(elapsed_time%60), '[s]\n'
  
  
  
  
  q1 = [1.469144582748413, 0.6579244136810303, -0.8009049892425537, -1.5478472709655762, 0.816594123840332, 1.060421109199524, -1.085035800933838]
  q2 = [3.0154144763946533, 1.415796160697937, -0.9958117008209229, -1.6129883527755737, -1.2736597061157227, 0.5792979598045349, -0.11706379801034927]
  x1 = [0.29996908004088241, 0.55000364085940134, 0.49826751488292159, -0.4999900340797781, 0.49985282899303357, 0.50023539998301281, 0.49992165363424546]
  x2 = [-0.33002107433952665, 0.50112067311172093, 0.22003802902636502, -0.50003124263322185, 0.49973825183241688, 0.50020263979657198, 0.50002775441638925]
  
  #sleep(ct)
  #ct.robot.MoveToQ(q1, 10.0, blocking=True)
  
  #x1[:2] = [-0.32999999999999996, 0.55]
  #sleep(ct)
  #ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
  
  #x1[2] = 0.15 + 0.07
  #sleep(ct)
  #ct.robot.MoveToXI(x1, 1.5*arm_speed(ct, x1), blocking=True)
  
  #sleep(ct)
  #ct.robot.MoveGripper(0.058)	
  
  #x1[1] -= 0.05
  #sleep(ct)
  #ct.robot.MoveToXI(x1, arm_speed(ct, x1), blocking=True)
  
  x1 = copy.deepcopy(x2)
  ct.robot.MoveToQ(q2, 5.0, blocking=True)
  
  x1[2] =0.45
  sleep(ct)
  rospy.sleep(0.5)
  print 4.0*arm_speed(ct, x1), x1
  ct.robot.MoveToXI(x1, 4.0*arm_speed(ct, x1), limit_vel=False, blocking=True)
  #ct.robot.MoveToX(x1, 4.0*arm_speed(ct, x1), blocking=True)
  print 'finished'
  
  sleep(ct)
  ct.robot.MoveToQ(q_init2, 1.5*arm_speed(ct, list(ct.robot.FK(q_init2))), blocking=True)	#初期化