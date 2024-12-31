import math
import random
import pandas as pd
import numpy as np
class Point():
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
    def distance(self,b):
        sqr_x=(self.x-b.x)**2
        sqr_y=(self.y-b.y)**2
        return math.sqrt(sqr_x+sqr_y)
    def __str__(self) -> str:
        return f'({self.x},{self.y})'

data=[]
with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\dataset\\50.20.2.txt",'r') as f:
    f.readline()
    f.readline()
    for i in f.readlines():
        x,y,z=i.split()[:]
        x=float(x)
        y=float(y)
        point=Point(x,y)
        data.append(point)
indexes=[i for i in range(len(data))]

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
            state=self.actions[0]
            available_actions=self.actions[1:]
            action=self.get_next_action(state,available_actions)
            counting_state=1
            self.ans.append(state)
            while counting_state <= len(self.actions)-1:
                reward=data[state].distance(data[action])
                next_state=action
                available_actions.remove(next_state)
                if not available_actions :
                    available_actions.append(self.actions[0])
                next_action=self.get_next_action(next_state,available_actions)
                self.update_q_table(state,action,reward,next_state,next_action,counting_state)
                self.ans.append(next_state)
                action=next_action
                state=next_state
                counting_state+=1
            distance=0
            for i in range(1,len(self.ans)):
                distance+= data[self.ans[i]].distance(data[self.ans[i-1]]) 
            if distance < cp:
                self.route=self.ans[:]
                cp=distance
            self.ans.clear()
        print(cp*1.65)
def run():
    mainn=Sarsa(action=indexes)
    mainn.train()
    return mainn.route
def city():
    return data
run()



   




            




