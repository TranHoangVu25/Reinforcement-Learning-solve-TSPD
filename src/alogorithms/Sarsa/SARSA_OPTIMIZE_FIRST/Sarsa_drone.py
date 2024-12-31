import math
import random
import pandas as pd
import numpy as np
import Sarsa_truck as Sa
data=[]
drone_speed=50
with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\dataset\\50.20.2.txt",'r') as f:
    f.readline()
    f.readline()
    for i in f.readlines():
        x,y,z=i.split()[:]
        x=float(x)
        y=float(y)
        point=Sa.Point(x,y)
        data.append(point)
indexes=[i for i in range(len(data))]
route=Sa.run()

class Sarsa():
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
    def get_next_action(self,state,available_action):
        self.check_if_state_action_exist(state)
        tmp_actions=available_action[:]
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
        if len(available_action) !=0 :
            q_value_real = reward + self.gamma * self.q_table.loc[next_state,next_action]
        else:
            q_value_real = reward
        self.q_table.loc[state,action] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\result\\raw\\TspD_48.txt",'w') as fi: 
            cp=float(1e9)
            for episode in range(80):
                pos_truck=0
                pos_drone=0
                time=0.0
                tmp_route_truck=[]
                tmp_route_drone=[]
                available_actions=self.route[1:]
                action=self.get_next_action(pos_drone,available_actions)
                tmp_route_truck.append(pos_truck)
                tmp_route_drone.append(pos_drone)
                available_actions.remove(action)
                while len(available_actions):
                    remainingTimeOfTruck=0.0
                    remainingTimeOfDrone=(data[pos_drone].distance(data[action]))*0.08
                    reward=0.0
                    tmp_route_drone.append(action)
                    while len(available_actions)!=0 and remainingTimeOfTruck <= remainingTimeOfDrone:
                        remainingTimeOfTruck+=data[available_actions[0]].distance(data[pos_truck])*1.65
                        pos_truck=available_actions[0]
                        available_actions.remove(pos_truck)
                        tmp_route_truck.append(pos_truck)
                    remainingTimeOfDrone+=(data[pos_drone].distance(data[pos_truck]))*0.08
                    # reward=max(remainingTimeOfDrone,remainingTimeOfTruck)
                    reward= remainingTimeOfDrone + remainingTimeOfTruck
                    next_pos_drone=pos_truck
                    tmp_route_drone.append(next_pos_drone)
                    if len(available_actions)==0:
                        next_action=0
                        tmp_route_drone.append(next_action)
                        tmp_route_truck.append(next_action)
                    else:
                        next_action=self.get_next_action(next_pos_drone,available_actions)
                        available_actions.remove(next_action)
                        if len(available_actions)==0:
                            time+=max(data[next_action].distance(data[0])+ data[next_action].distance(data[next_pos_drone]) ,data[pos_truck].distance(data[0]))
                    self.update_q_table(pos_drone,action,reward,next_pos_drone,next_action,available_actions)
                    action=next_action
                    pos_drone=next_pos_drone
                    time+=reward
                fi.write(f'{episode} : {time}\n')
                # print(time)
                if time < cp:
                    cp=time
                    self.ans=time
                    self.route_truck=tmp_route_truck
                    self.route_drone=tmp_route_drone    

main=Sarsa(route=route,action=indexes)
main.train()
print(main.route_truck)
print(main.route_drone)
print(f'ans: {main.ans}')
distance=0
for i in range(1,len(main.route_truck)):
    distance+= data[main.route_truck[i]].distance(data[main.route_truck[i-1]]) 
print(f'truck: {distance*1.65}')
distance=0
for i in range(1,len(main.route_drone)):
    distance+= data[main.route_drone[i]].distance(data[main.route_drone[i-1]]) 
print(f'drone: {distance*0.08}')

with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\result\\raw\\TspD_48.txt","a") as fi:
    fi.write(f'{main.route_truck}\n')
    fi.write(f'{main.route_drone}\n')
    fi.write(f'ans: {main.ans}')

