import math
import random
import pandas as pd
import numpy as np
from src.plot_figure.plot_route_truck import plot_route_truck_s,plot_route_drone_s

drone_speed=43.2
truck_speed=50
drone_capacity=1
maxDisDrone=4
truck_capacity=1500
al=0.01
be=0.99
ghgTruck=674.3
ghgdrone=14.4
ED=0.08
ET=1.65
class Point():
    def __init__(self,x,y,demand,cus) -> None:
        self.x=x
        self.y=y
        self.demand=demand
        self.cus=cus
    def distance(self,b):
        sqr_x=(self.x-b.x)**2
        sqr_y=(self.y-b.y)**2
        return math.sqrt(sqr_x+sqr_y)
    def __str__(self) -> str:
        return f'({self.x},{self.y})'
data=[]
data.append(Point(0,0,0,0.000000001))
# this will take the input data
file_path = "D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\dataset\\new data TSPD.txt" 
with open(file_path,'r') as f:
    # 
    f.readline()
    f.readline()
    for i in f.readlines():
        x,y,demand,cus=i.split()
        x=float(x)
        y=float(y)
        demand=float(demand)
        cus=float(cus)
        point=Point(x,y,demand,cus)
        data.append(point)
indexes=[i for i in range(len(data))]
numCus=len(data)-1

class Sarsa():
    def __init__(self,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=[]
        self.route=[]

    def check_if_state_action_exist(self,state):
        if state not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(0)] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )
    
    def get_next_action(self,state,indexes):
        self.check_if_state_action_exist(state)
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(indexes)
            for action in indexes:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(indexes)
        return target_action
    
    def update_q_table(self,state, action, reward, next_state, next_action, counting_state):
        self.check_if_state_action_exist(next_state)
        q_value_predict=self.q_table.loc[state,action]
        if counting_state <= len(self.actions):
            q_value_real = reward + self.gamma * self.q_table.loc[next_state,next_action]
        else:
            q_value_real = reward
        self.q_table.loc[state,action] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        cp=float(1e9)
        for episode in range(80):
            total=0.0
            totaltime=0.0
            totalSaCus=0.0
            totalghg=0.0
            state=self.actions[0]
            available_actions=self.actions[1:]
            action=self.get_next_action(state,available_actions)
            counting_state=1
            self.ans.append(state)
            while counting_state <= len(self.actions)-1:
                time=data[state].distance(data[action])/truck_speed
                totaltime+=time
                saCus=totaltime/data[state].cus/numCus
                totalSaCus+=data[state].cus/(totaltime/numCus)
                totalghg+=ghgTruck*(data[state].distance(data[action]))
                reward=  ghgTruck*(data[state].distance(data[action]))*al + saCus*be
                next_state=action
                available_actions.remove(next_state)
                if not available_actions :
                    available_actions.append(self.actions[0])
                    totalghg+=ghgTruck*(data[next_state].distance(data[0]))
                next_action=self.get_next_action(next_state,available_actions)
                self.update_q_table(state,action,reward,next_state,next_action,counting_state)
                self.ans.append(next_state)
                action=next_action
                state=next_state
                counting_state+=1
            # distance=0
            # for i in range(1,len(self.ans)):
            #     distance+= data[self.ans[i]].distance(data[self.ans[i-1]]) 

            total=totalghg*al + 1/totalSaCus*be
            # print(total,totalghg*al,1/totalSaCus*be)
            if total < cp:
                self.route=self.ans[:]
                cp=total
            self.ans.clear()
        # print(cp)

def run():
    mainn=Sarsa(action=indexes)
    mainn.train()
    return mainn.route
    # print(mainn.route)

# print(run())
route=run()

def ten_best(li:list,pos_drone:int,pos_truck):
    tmp=li[:]
    tmp.sort(key=lambda pos: data[pos].distance(data[pos_drone]))
    able_pos=[]
    for i in tmp:
        if data[i].distance(data[pos_drone]) + data[i].distance(data[pos_truck]) <= maxDisDrone:
            able_pos.append(i)
    if len(able_pos)>10:
        return able_pos[:10]
    return able_pos
def get_des_for_drone(indexes):
        available_drone=[]
        for i in range(1,len(indexes)):
            if data[i].demand <= drone_capacity:
                available_drone.append(i)
        return available_drone
indexes = get_des_for_drone(indexes)

class SarsaD():
    def __init__(self,route,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.route=route
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=0
        self.route_truck=[]
        self.route_drone=[]

    def check_if_state_action_exist(self,state):
        if state not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(0)] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )

    def get_next_action(self,state,available_action,pos_truck):
        self.check_if_state_action_exist(state)
        tmp_actions=ten_best(available_action,state,pos_truck)
        if len(tmp_actions) == 0:
            return -1
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(tmp_actions)
            for action in tmp_actions:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(tmp_actions)
        return target_action

    def update_q_table(self,state, action, reward, next_state, next_action, available_action):
        self.check_if_state_action_exist(next_state)
        q_value_predict=self.q_table.loc[state,action]
        if len(available_action) !=0 and next_action != -1:
            q_value_real = reward + self.gamma * self.q_table.loc[next_state,next_action]
        else:
            q_value_real = reward
        self.q_table.loc[state,action] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        # with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\result\\raw\\TspD_48.txt",'w') as fi: 
            cp=float(1e9)
            for episode in range(80):
                pos_truck=0
                pos_drone=0
                time=0.0
                totaltime=0.0
                totalghg=0.0
                total=0.0
                totalSaCus=0.0
                saCus=0.0
                tmp_route_truck=[]
                tmp_route_drone=[]
                available_actions_drone= self.actions[:]
                available_actions_truck= self.route[1:]
                action=self.get_next_action(pos_drone,available_actions_drone,available_actions_truck[0])

                while action ==-1 :
                    tmp_route_truck.append(pos_truck)
                    tmp_route_drone.append(pos_drone)
                    time =  data[pos_truck].distance(data[available_actions_truck[0]])/truck_speed
                    totaltime += time
                    saCus=totaltime/data[available_actions_truck[0]].cus/numCus
                    totalSaCus +=data[available_actions_truck[0]].cus/(totaltime/numCus)
                    totalghg += data[pos_truck].distance(data[available_actions_truck[0]])*ghgTruck
                    pos_truck=available_actions_truck[0]
                    pos_drone=available_actions_truck[0]
                    available_actions_truck.remove(pos_truck)
                    if pos_drone in available_actions_drone: 
                        available_actions_drone.remove(pos_drone)
                    action = self.get_next_action(pos_drone,available_actions_drone,available_actions_truck[0])

                tmp_route_truck.append(pos_truck)
                tmp_route_drone.append(pos_drone)
                available_actions_drone.remove(action)
                available_actions_truck.remove(action)

                while len(available_actions_drone):
                    reward=0.0
                    energy_truck=0.0
                    remainingTimeOfTruck=0.0
                    remainingTimeOfDrone=(data[pos_drone].distance(data[action]))/drone_speed
                    saCus=(totaltime + remainingTimeOfDrone)/data[action].cus/numCus
                    reward+=saCus*be
                    totalSaCus +=data[action].cus/(( totaltime + remainingTimeOfDrone )/numCus)
                    energy_drone = data[pos_drone].distance(data[action])*ghgdrone
                    tmp_route_drone.append(action)
                    while len(available_actions_truck)!=0 and remainingTimeOfTruck <= remainingTimeOfDrone and data[pos_drone].distance(data[action]) + data[available_actions_truck[0]].distance(data[action]) <= maxDisDrone:
                        remainingTimeOfTruck += data[available_actions_truck[0]].distance(data[pos_truck])/truck_speed
                        energy_truck+= data[available_actions_truck[0]].distance(data[pos_truck])*ghgTruck
                        saCus=(totaltime + remainingTimeOfTruck)/data[available_actions_truck[0]].cus/numCus
                        totalSaCus +=data[action].cus/(( totaltime + remainingTimeOfTruck )/numCus)
                        reward+=saCus*be
                        pos_truck=available_actions_truck[0]
                        available_actions_truck.remove(pos_truck)
                        if pos_truck in available_actions_drone: 
                            available_actions_drone.remove(pos_truck)
                        tmp_route_truck.append(pos_truck)

                    remainingTimeOfDrone+=(data[action].distance(data[pos_truck]))/drone_speed
                    energy_drone = data[pos_truck].distance(data[action])*ghgdrone
                    totaltime+=max(remainingTimeOfDrone,remainingTimeOfTruck)
                    totalghg += energy_drone + energy_truck

                    reward += (energy_truck + energy_drone)*al
                    
                    next_pos_drone=pos_truck
                    tmp_route_drone.append(next_pos_drone)

                    if len(available_actions_truck)==0 and  len(available_actions_drone)==0:
                        next_action=0
                        tmp_route_drone.append(next_action)
                        tmp_route_truck.append(next_action)
                        totaltime+= data[pos_truck].distance(data[0])/truck_speed
                        energy_truck = data[pos_truck].distance(data[0])*ghgTruck
                        totalghg+= energy_truck
                    elif len(available_actions_truck) != 0 and  len(available_actions_drone) != 0:
                        next_action=self.get_next_action(next_pos_drone,available_actions_drone,pos_truck)
                        if next_action in available_actions_drone: available_actions_drone.remove(next_action)
                        if next_action in available_actions_truck: available_actions_truck.remove(next_action)
                        if len(available_actions_truck)==0 and  len(available_actions_drone)==0:
                            tmp_route_drone.append(next_action)
                            tmp_route_drone.append(0)
                            tmp_route_truck.append(0)
                            energy_drone = data[next_action].distance(data[next_pos_drone])*2*ghgdrone
                            energy_truck = data[pos_truck].distance(data[0])*ghgTruck
                            totaltime+= data[next_action].distance(data[next_pos_drone])/drone_speed
                            totalSaCus += data[next_action].cus/(totaltime/numCus)
                            totalghg+=energy_truck+energy_drone
                    elif len(available_actions_truck) != 0 and  len(available_actions_drone) == 0:
                        next_action=available_actions_truck[0]
                    self.update_q_table(pos_drone,action,reward,next_pos_drone,next_action,available_actions_drone)

                    while next_action == -1 and len(available_actions_truck) !=0 and len(available_actions_drone)!=0 :
                        time =  data[pos_truck].distance(data[available_actions_truck[0]])/truck_speed
                        totaltime += time
                        saCus=totaltime/data[available_actions_truck[0]].cus/numCus
                        totalSaCus +=data[available_actions_truck[0]].cus/(totaltime/numCus)
                        totalghg += data[pos_truck].distance(data[available_actions_truck[0]])*ghgTruck
                        pos_truck=available_actions_truck[0]
                        next_pos_drone=available_actions_truck[0]
                        available_actions_truck.remove(pos_truck)
                        if next_pos_drone in available_actions_drone: 
                            available_actions_drone.remove(next_pos_drone)
                        next_action = self.get_next_action(next_pos_drone,available_actions_drone,pos_truck)
                        tmp_route_truck.append(pos_truck)
                        tmp_route_drone.append(next_pos_drone)

                    action=next_action
                    pos_drone=next_pos_drone
                    # time+=reward
                    if len(available_actions_truck) != 0 and  len(available_actions_drone) == 0:
                        for i in range(0,len(available_actions_truck)):
                            if(i==len(available_actions_truck)-1):
                                energy_truck = data[pos_truck].distance(data[0])*ghgTruck
                                totalghg += energy_truck
                                tmp_route_truck.append(0)
                                tmp_route_drone.append(0)
                            else:
                                time=data[pos_truck].distance(data[i])/truck_speed
                                totaltime+=time
                                # saCus=totaltime/data[i].cus/numCus
                                totalSaCus +=data[i].cus/(totaltime/numCus)
                                energy_truck = data[pos_truck].distance(data[i])*ghgTruck
                                totalghg += energy_truck
                                tmp_route_drone.append(i)
                                tmp_route_truck.append(i)
                                pos_truck=i
                total = totalghg*al + 1/totalSaCus*be
                # fi.write(f'{episode} : {time}\n')
                if total < cp:
                    cp=total
                    self.ans=total
                    self.route_truck=tmp_route_truck
                    self.route_drone=tmp_route_drone    

def SARSA():
    main=SarsaD(route=route,action=indexes)
    main.train()
    with open("D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\SARSA_result.txt","w") as fio:
        fio.write(f'{' '.join(map(str,main.route_drone))}\n')
        fio.write(f'{' '.join(map(str,main.route_truck))}\n')
        fio.write(f'{main.ans}\n\n')
    file_path = "D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\dataset\\plt.txt" 
    data = np.loadtxt(file_path, dtype=float)
    plot_route_truck_s(data,main.route_truck)
    plot_route_drone_s(data,main.route_drone)