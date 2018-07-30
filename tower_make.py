def tower_make(cup_goal_set, stage):
  cup_diameter = 0.08
  cup_height = 0.096
  
  cup_list =[]
  for i in range(stage, 0, -1):
    tmp = cup_goal_set[0]+cup_diameter*(i-1)/2
    for j in range(i):
      cup_list.append([tmp-cup_diameter*j, cup_goal_set[1],cup_goal_set[2]+cup_height*(stage-i)])
  
  return cup_list

def Run(ct,*args):
  print (tower_make([-0.24, 0.45, 0.0], 2))

if __name__ == "__main__":
  print (tower_make(0, 0, 0, 3))