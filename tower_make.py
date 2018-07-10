def tower_make(x, y, z, stage):
  cup_diameter = 0.08
  cup_height = 0.10
  
  cup_list =[]
  for i in range(stage, 0, -1):
    tmp = (x+cup_diameter*(i-1))/2
    for j in range(i):
      cup_list.append([tmp-cup_diameter*j, y, z+cup_height*(stage-i)])
  
  return cup_list

if __name__ == "__main__":
  print (tower_make(0, 0, 0, 3))