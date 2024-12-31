import random
import pandas as pd
import numpy as np
from utils import creatState,convertList,createAction
import math


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


drone_speed=0
city=[]
with open("D:\\Tran Hoang Vu\\Lab\\reinforcement learning\\Q-learning_tspd\\data\\48.txt") as f:
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

class QLearning:
    def __init__(self, actions, alpha=0.01, gamma=0.9, epsilon=0.9, drone_speed=drone_speed):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=self.actions, dtype=float)
        self.ans = float(1e9)
        self.droneSpeed = drone_speed

    def check_if_state_action_exist(self, stringState):
        if stringState not in self.q_table.index:
            self.q_table = self.q_table._append(
                pd.Series(
                    [float(1e4)] * len(self.actions),
                    index=self.actions,
                    name=stringState
                )
            )

    def get_next_action(self, stringState: str):
        self.check_if_state_action_exist(stringState)
        state = State()
        state.init(stringState)
        available_action = []

        if state.remainingTimeOfTruck == state.remainingTimeOfDrone:
            if state.current_truck == state.current_drone:
                if len(state.not_vistied) > 10:
                    tmp_not_visited = state.not_vistied[:]
                    available_city = []
                    while len(available_city) < 10 and len(tmp_not_visited) > 0:
                        available_city.append(tmp_not_visited.pop(random.randint(0, len(tmp_not_visited) - 1)))
                    for i in available_city:
                        for j in available_city:
                            available_action.append(f'{i}|{j}')
                else:
                    for i in state.not_vistied:
                        for j in state.not_vistied:
                            available_action.append(f'{i}|{j}')
            else:
                for i in state.not_vistied:
                    available_action.append(f'{i}|{i}')
        elif state.remainingTimeOfTruck < state.remainingTimeOfDrone:
            for i in state.not_vistied:
                available_action.append(f'{i}|{state.current_drone}')
        elif state.remainingTimeOfTruck > state.remainingTimeOfDrone:
            available_action.append(f'{state.current_truck}|{state.current_truck}')

        if not available_action:
            # Handle case where no actions are available
            return f'{state.current_truck}|{state.current_drone}'

        # epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            index = None
            min_value = float(1e7)
            np.random.shuffle(available_action)
            for action in available_action:
                if self.q_table.loc[stringState, action] < min_value:
                    index = action
                    min_value = self.q_table.loc[stringState, action]
            target_action = index
        else:
            target_action = random.choice(available_action)

        return target_action

    def update_q_table(self, stringState: str, stringAction, reward, stringNextSate):
        self.check_if_state_action_exist(stringNextSate)
        next_state = State()
        next_state.init(stringNextSate)

        q_value_predict = self.q_table.loc[stringState, stringAction]

        if len(next_state.not_vistied) != 0:
            q_value_real = reward + self.gamma * self.q_table.loc[stringNextSate].min()
        else:
            q_value_real = reward

        self.q_table.loc[stringState, stringAction] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        for episode in range(60):

            #
            distance_matrix = np.zeros((len(city), len(city)))

            for i in range(len(city)):
                for j in range(len(city)):
                    distance_matrix[i][j] = city[i].dis_bet(city[j])
                    #

            tmp_ans = 0.0
            truck_distance = 0.0
            path_truck = [0]
            path_drone = [0]
            state = State()
            # Khởi tạo trạng thái ban đầu của state
            state.init(f'{convertList(state.not_vistied)}|0|0|0.0|0.0')

            action = Action()
            action.init(self.get_next_action(state.convertToString()))

            while len(state.not_vistied) != 0:
                next_state = State()  # Tạo một đối tượng state mới
                next_state.init(state.convertToString())  # Sao chép từ state hiện tại

                next_state.remainingTimeOfTruck += (city[state.current_truck].dis_bet(city[action.truck]))
                next_state.remainingTimeOfDrone += (
                            city[state.current_drone].dis_bet(city[action.drone]) / self.droneSpeed)



                truck_distance += city[state.current_truck].dis_bet(city[action.truck])



                if action.truck == action.drone:
                    Ct = max(next_state.remainingTimeOfTruck, next_state.remainingTimeOfDrone)
                    next_state.remainingTimeOfTruck = 0.0
                    next_state.remainingTimeOfDrone = 0.0
                else:
                    Ct = min(next_state.remainingTimeOfTruck, next_state.remainingTimeOfDrone)
                    next_state.remainingTimeOfTruck -= Ct
                    next_state.remainingTimeOfDrone -= Ct

                reward = Ct
                tmp_ans += Ct
                next_state.current_truck = action.truck
                next_state.current_drone = action.drone

                path_truck.append(action.truck)
                path_drone.append(action.drone)

                if action.truck in next_state.not_vistied:
                    next_state.not_vistied.remove(action.truck)
                if action.drone in next_state.not_vistied:
                    next_state.not_vistied.remove(action.drone)

                next_action = self.get_next_action(next_state.convertToString())
                self.update_q_table(state.convertToString(), action.convertToString(), reward,
                                    next_state.convertToString())

                state = next_state  # Cập nhật state hiện tại thành next_state
                action.init(next_action)

            truck_distance += city[state.current_truck].dis_bet(city[0])

            tmp_ans += max(state.remainingTimeOfDrone, state.remainingTimeOfTruck)
            tmp_ans += max(city[state.current_truck].dis_bet(city[0]),
                           city[state.current_drone].dis_bet(city[0]) / drone_speed)

            if tmp_ans < self.ans:
                self.ans = tmp_ans
            print(f'Path traveled by drone: {path_drone}')
            print(f'Traveled distance: {truck_distance}')
        # return path_truck,path_drone