import math
import random
import pandas as pd
import numpy as np
# this follow function are to make me easier to think=))
def convertList(li):
    s=''
    for i in li:
        s+=str(i)+','
    return s
def convertListString(s):
    li=[]
    for i in s.split(",")[:-1]:
        li.append(int(i))
    return li
def creatState(s:str):
    tmp=s.split("|")
    li=convertListString(tmp[0])
    cr_tr=int(tmp[1])
    cr_dr=int(tmp[2])
    re_ti_tr=float(tmp[3])
    re_ti_dr=float(tmp[4])
    return li,cr_tr,cr_dr,re_ti_tr,re_ti_dr
def createAction(a:str):
    tmp=a.split("|")
    tr=int(tmp[0])
    dr=int(tmp[1])
    return tr,dr
def ten_best(li:list,pos_vi:int):
    tmp=li[:]
    tmp.sort(key=lambda pos: city[pos].dis_bet(city[pos_vi]))
    if len(tmp)>10:
        return tmp[:10]
    return tmp
# those classes are just to make color/think less :v
class State():
    def __init__(self) -> None:
        self.not_vistied=index[1:]
        self.current_truck=0
        self.current_drone=0
        self.remainingTimeOfTruck=0.0
        self.remainingTimeOfDrone=0.0
    def init(self,s:str):
        self.not_vistied,self.current_truck,self.current_drone,self.remainingTimeOfTruck,self.remainingTimeOfDrone=creatState(s)
    def __str__(self) -> str:
        return f'{self.not_vistied}\n{self.current_truck}\n{self.current_drone}\n{self.remainingTimeOfTruck}\n{self.remainingTimeOfDrone}'
    def convertToString(self):
        return f'{convertList(self.not_vistied)}|{self.current_truck}|{self.current_drone}|{self.remainingTimeOfTruck}|{self.remainingTimeOfDrone}'

class Action():
    def __init__(self) -> None:
        self.truck=1
        self.drone=1
    def init(self,a:str):
        self.truck,self.drone=createAction(a)
    def __str__(self) -> str:
        return f'{self.truck}|{self.drone}'
    def convertToString(self):
        return f'{self.truck}|{self.drone}'
    def __eq__(self, value: object) -> bool:
        return self.truck==value.truck and self.drone==value.drone
class Point():
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
    def dis_bet(self,value: object):
        return math.sqrt((self.x - value.x)**2+(self.y - value.y)**2)
    def __str__(self) -> str:
        return f'{self.x},{self.y}'
# take data to set up
drone_speed=0
city=[]
with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\dataset\\Input_TSPD_48.txt") as f:
    drone_speed=int(f.readline())
    for i in f.readlines():
        x,y=i.split()[1:]
        x=int(x)
        y=int(y)
        city.append(Point(x,y))
index=[i for i in range(0,len(city))]
actions=[]
for i in index:
    for j in index:
        actions.append(f'{i}|{j}')
# main think:v
class Sarsa():
    def __init__(self,actions, alpha=0.01, gamma=0.9,epsilon=0.9,drone_speed=drone_speed) -> None:
        self.actions=actions
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=float(1e9)
        self.droneSpeed=drone_speed
        self.route_truck=[]
        self.route_drone=[]
    def check_if_state_action_exist(self,stringState):
        if stringState not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(1e4)]*len(self.actions),
                    index=self.actions,
                    name=stringState
                )
            )
    def get_next_action(self,stringState:str):
        self.check_if_state_action_exist(stringState)
        state=State()
        state.init(stringState)
        available_action=[]
        if state.remainingTimeOfTruck == state.remainingTimeOfDrone :
            if state.current_truck==state.current_drone:
                if len(state.not_vistied)>10:
                    available_city_truck=[]
                    available_city_drone=[]
                    available_city_truck=ten_best(state.not_vistied,state.current_truck)
                    available_city_drone=ten_best(state.not_vistied,state.current_drone)
                    for i in available_city_truck:
                        for j in available_city_drone:
                            available_action.append(f'{i}|{j}')
                else:
                    for i in state.not_vistied:
                        for j in state.not_vistied:
                            available_action.append(f'{i}|{j}')
            else:
                available_city_truck=[]
                available_city_truck=ten_best(state.not_vistied,state.current_truck)
                for i in available_city_truck:
                    available_action.append(f'{i}|{i}')
        elif state.remainingTimeOfTruck < state.remainingTimeOfDrone :
            available_city_truck=[]
            available_city_truck=ten_best(state.not_vistied,state.current_truck)
            for i in available_city_truck:
                available_action.append(f'{i}|{state.current_drone}')
        elif state.remainingTimeOfTruck > state.remainingTimeOfDrone :
            available_action.append(f'{state.current_truck}|{state.current_truck}')
        if random.uniform(0,1) <  self.epsilon:
            index=None
            min_value = float(1e7)
            np.random.shuffle(available_action)
            for action in available_action:
                if self.q_table.loc[stringState,action] < min_value:
                    index = action
                    min_value = self.q_table.loc[stringState,action]
            target_action=index
        else:
            target_action=random.choice(available_action)
        # this gonna return string, don't be a d***=)
        return target_action
    def update_q_table(self,stringState:str,stringAction,reward,stringNextSate,stringNextAction):
        self.check_if_state_action_exist(stringNextSate)
        next_state=State()
        next_state.init(stringNextSate)
        q_value_predict=self.q_table.loc[stringState,stringAction]
        if len(next_state.not_vistied) != 0:
            q_value_real = reward + self.gamma * self.q_table.loc[stringNextSate,stringNextAction]
        else:
            q_value_real = reward
        self.q_table.loc[stringState,stringAction] += self.alpha * ( q_value_real - q_value_predict )
    def train(self):
        with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\result\\raw\\TspD_48.txt","w") as fi:
            for episode in range(60):
                tmp_ans=0.0
                state=State()
                action=Action()
                action.init(self.get_next_action(state.convertToString()))
                tmp_route_truck=[0]
                tmp_route_drone=[0]
                while len(state.not_vistied)!=0 :
                    if action.truck not in tmp_route_truck: 
                        tmp_route_truck.append(action.truck)
                    if action.drone not in tmp_route_drone:
                        tmp_route_drone.append(action.drone)
                    next_state=State()
                    next_state.init(state.convertToString())
                    next_state.remainingTimeOfTruck += (city[state.current_truck].dis_bet(city[action.truck]))
                    next_state.remainingTimeOfDrone += (city[state.current_drone].dis_bet(city[action.drone])/self.droneSpeed)
                    if action.truck == action.drone:
                        Ct=max(next_state.remainingTimeOfTruck,next_state.remainingTimeOfDrone)
                        next_state.remainingTimeOfTruck =0.0
                        next_state.remainingTimeOfDrone =0.0
                    else:
                        Ct=min(next_state.remainingTimeOfTruck,next_state.remainingTimeOfDrone)
                        next_state.remainingTimeOfTruck -= Ct
                        next_state.remainingTimeOfDrone -= Ct
                    reward=Ct
                    tmp_ans+=Ct
                    next_state.current_truck=action.truck
                    next_state.current_drone=action.drone
                    if action.truck in next_state.not_vistied:
                        next_state.not_vistied.remove(action.truck)
                    if action.drone in next_state.not_vistied:
                        next_state.not_vistied.remove(action.drone)
                    if len(next_state.not_vistied) == 0:
                        next_action=action
                        next_action.init(f'{next_state.current_truck}|{next_state.current_drone}')
                    else:
                        next_action=action
                        next_action.init(self.get_next_action(next_state.convertToString()))
                    self.update_q_table(state.convertToString(),action.convertToString(),reward,next_state.convertToString(),next_action.convertToString())
                    state=next_state
                    action=next_action
                tmp_route_truck.append(0)
                tmp_route_drone.append(0)
                tmp_ans+=max(state.remainingTimeOfDrone , state.remainingTimeOfTruck)
                tmp_ans+=max(city[state.current_truck].dis_bet(city[0]),city[state.current_drone].dis_bet(city[0])/drone_speed)
                fi.write(f'{episode}: {tmp_ans}\n')
                if tmp_ans < self.ans:
                    self.ans=tmp_ans
                    self.route_truck=tmp_route_truck[:]
                    self.route_drone=tmp_route_drone[:]
main=Sarsa(actions=actions)
main.train()
with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\result\\raw\\TspD_48.txt","a") as fi:
    fi.write(f'Truck: {main.route_truck}\n')
    fi.write(f'Drone: {main.route_drone}\n')
    fi.write(f'ans: {main.ans}')