import copy

def start_tower(cup_location, stage):
  cup_step = 0.042/9
  cup_num = 0
  cup_list =[]
  
  for i in range(stage):
    cup_num += (i+1)
  
  for i in range(cup_num):
    tmp = copy.deepcopy(cup_location)
    #print tmp
    tmp[2] += cup_step*(cup_num-i-1)
    #print tmp
    cup_list.append(tmp[:])
    #print cup_list
  
  return cup_list


def Run(ct,*arg):
  print start_tower([0,0,0.22], 3)
  
if __name__ == "__main__":
  print start_tower([0,0,0.22], 2)