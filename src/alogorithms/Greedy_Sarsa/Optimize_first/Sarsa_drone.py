import math
import random
import pandas as pd
import numpy as np

class Point():
    def __init__(self,x,y,demand,cus) -> None:
        self.x=x
        self.y=y
        self.demand=demand
        self.satisfaction=cus
    def distance(self,b):
        sqr_x=(self.x-b.x)**2
        sqr_y=(self.y-b.y)**2
        return math.sqrt(sqr_x+sqr_y)
    def __str__(self) -> str:
        return f'({self.x},{self.y})'

location = []
location.append(Point(0,0,0,0))
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
        location.append(point)
indexes=[i for i in range(len(location))]
CustomerNumber=len(location)-1

class Truck():
    def __init__(self) -> None:
        self.speed=50
        self.capacity=1500
        self.ghg=674.3
        self.route=[0]
        self.available=[]
        self.remainTime=0.0
        self.destination = None

class Drone():
    def __init__(self) -> None:
        self.speed=43.2
        self.capacity=1
        self.ghg=14.4
        self.route=[0]
        self.available=[]
        self.remainTime=0.0
        self.maxDistance=4
        self.availableDistance=4
        self.destination = None

class Solution():
    def __init__(self) -> None:
        self.Total=1e9
        self.TruckRoute=[]
        self.DroneRoute=[]
    def __str__(self) -> str:
        return f'Total: {self.Total}\nTruckRoute: {self.TruckRoute}\nDroneRoute: {self.DroneRoute}'

class SarsaT():
    def __init__(self,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.al=0.01
        self.be=0.99

    def check_if_state_action_exist(self,state):
        if state not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(0)] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )
    
    def get_next_action(self,state,locationIndexes):
        self.check_if_state_action_exist(state)
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(locationIndexes)
            for action in locationIndexes:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(locationIndexes)
        return target_action
    
    def update_q_table(self,state, action, reward, next_state, next_action, availableLocation):
        self.check_if_state_action_exist(next_state)
        q_value_predict=self.q_table.loc[state,action]
        if len(availableLocation):
            q_value_real = reward + self.gamma * self.q_table.loc[next_state,next_action]
        else:
            q_value_real = reward
        self.q_table.loc[state,action] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        solution = Solution()
        for episode in range(80):
            TotalResult=0.0
            TotalTime=0.0
            TotalSatisfaction=0.0
            TotalGHG=0.0
            truck = Truck()
            truck.available = indexes[1:]
            state = indexes[0]
            action = self.get_next_action(state,truck.available)
            while len(truck.available):
                DeliveryTime = location[state].distance(location[action])/truck.speed
                TotalTime += DeliveryTime
                CustomerSatisfaction = location[action].satisfaction/DeliveryTime
                TotalSatisfaction += CustomerSatisfaction
                DeliveryGhg = location[state].distance(location[action])*truck.ghg 
                TotalGHG += DeliveryGhg
                reward = self.al * DeliveryGhg + self.be * 1/CustomerSatisfaction
                next_state = action
                truck.available.remove(next_state)
                truck.route.append(next_state)
                next_action = None
                if len(truck.available):
                    next_action = self.get_next_action(next_state,truck.available)
                else:
                    next_action = indexes[0]
                self.update_q_table(state,action,reward,next_state,next_action,truck.available)
                state = next_state
                action = next_action
            truck.route.append(indexes[0])
            TotalGHG += location[state].distance(location[indexes[0]]) * truck.ghg
            TotalResult = TotalGHG 
            TotalResult = self.al * TotalGHG + self.be * 1/TotalSatisfaction
            if TotalResult < solution.Total:
                solution.TruckRoute = truck.route[:]
                solution.Total = TotalResult
        return solution

def run():
    mainn=SarsaT(action=indexes)
    return mainn.train()

tmp=run().TruckRoute
# print(len(tmp[1:-1]))
def getLocationForDrone(droneCapacity):
    locationForDrone = []
    for i in range(1,len(indexes)):
        if location[i].demand <= droneCapacity:
            locationForDrone.append(i)
    return locationForDrone

def tenNearestLocation(available,LocationDrone,maxDistanceOfDrone):
    availableLocation =[]
    if len(available) == 0:
        return availableLocation
    for i in available:
        if location[LocationDrone].distance(location[i]) <= maxDistanceOfDrone:
            availableLocation.append(i)
    availableLocation.sort(key = lambda destination: location[LocationDrone].distance(location[destination]))
    if len(availableLocation) > 10:
        return availableLocation[:10]
    return availableLocation

actionForTrainingDrone = [-2,-1]
# -2: two vehicle will meet each others, -1: the truck continue its route
actionForTrainingDrone += getLocationForDrone(Drone().capacity)
# print(actionForTrainingDrone[2:])

class SarsaD():
    def __init__(self,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.al=0.01
        self.be=0.99

    def check_if_state_action_exist(self,state):
        if state not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(0)] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )

    def get_next_action(self,state,available,truckDesination,droneDestination,maxDistanceOfDrone):
        self.check_if_state_action_exist(state)
        availableActionForDrone = None
        if truckDesination != droneDestination:
            availableActionForDrone = [-2,-1]
        else:
            availableActionForDrone = [-1] 
            availableActionForDrone += tenNearestLocation(available,droneDestination,maxDistanceOfDrone)
        
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(availableActionForDrone)
            for action in availableActionForDrone:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(availableActionForDrone)
        return target_action

    def update_q_table(self,state, action, reward, next_state, next_action, available_action):
        self.check_if_state_action_exist(next_state)
        q_value_predict=self.q_table.loc[state,action]
        if len(available_action) !=0:
            q_value_real = reward + self.gamma * self.q_table.loc[next_state,next_action]
        else:
            q_value_real = reward
        self.q_table.loc[state,action] += self.alpha * (q_value_real - q_value_predict)

    def train(self):
        solution = run()
        solution.DroneRoute = solution.TruckRoute[:]
        truckReference = solution.TruckRoute[1:-1]
        for episode in range(80):
            # print("newturn")
            truck = Truck()
            truck.available = truckReference[:]
            drone = Drone()
            drone.available = actionForTrainingDrone[2:]
            truck.destination = indexes[0]
            drone.destination = indexes[0]
            TotalResult = 0
            TotalTime = 0
            TotalSatisfaction = 0
            TotalGHG = 0
            state = f'{truck.destination}|{drone.destination}'
            action = self.get_next_action(state,drone.available,truck.destination,drone.destination,drone.maxDistance)
            while len(truck.available):
                reward = 0
                if action == -2:
                    # print("\n-2 ")
                    # print(truck.destination)
                    # print(drone.destination)
                    gap = location[drone.destination].distance(location[truck.destination])
                    meetGHG = gap * drone.ghg
                    TotalGHG += meetGHG
                    reward = self.al * meetGHG
                    TotalTime += truck.remainTime + drone.remainTime
                    if drone.availableDistance >= gap:    
                        drone.destination = truck.destination
                        TotalTime += gap/drone.speed
                        # drone.route.append(drone.destination)
                    else: 
                        truck.destination = drone.destination
                        TotalTime += gap/truck.speed
                        # truck.route.append(truck.destination)
                    drone.availableDistance = drone.maxDistance
                    truck.remainTime = 0
                    drone.remainTime = 0
                    if drone.destination != drone.route[-1]:
                        drone.route.append(drone.destination)
                    if truck.destination != truck.route[-1]:
                        truck.route.append(truck.destination)
                    # print(truck.destination)
                    # print(drone.destination)

                elif action == -1:
                    if drone.destination == truck.destination:
                        # print("\n-1 == ")
                        # print(truck.destination)
                        # print(drone.destination)
                        nextTruckDestination = truck.available[0]
                        gap = location[truck.destination].distance(location[nextTruckDestination])
                        TotalTime += gap/truck.speed
                        TotalGHG += gap * truck.ghg
                        customerSatisfaction = location[nextTruckDestination].satisfaction/ TotalTime
                        TotalSatisfaction += customerSatisfaction
                        reward = self.al * gap * truck.ghg + self.be * 1/customerSatisfaction
                        truck.destination = nextTruckDestination
                        drone.destination = nextTruckDestination
                        # truck.route.append(truck.destination)
                        # drone.route.append(truck.destination)
                        truck.available.remove(truck.destination)
                        if truck.destination in drone.available :
                            # print(f'removeD: {truck.destination}') 
                            drone.available.remove(truck.destination)
                        if drone.destination != drone.route[-1]:
                            drone.route.append(drone.destination)
                        if truck.destination != truck.route[-1]:
                            truck.route.append(truck.destination)
                        # print(truck.destination)
                        # print(drone.destination)
                    else:
                        # print("\n-1 == ")
                        # print(truck.destination)
                        # print(drone.destination)
                        nextTruckDestination = truck.available[0]
                        gap = location[truck.destination].distance(location[nextTruckDestination])
                        deliverTime = 0
                        if truck.remainTime > drone.remainTime:
                            deliverTime += truck.remainTime
                            deliverTime += gap/truck.speed
                            truck.remainTime = 0
                        else: 
                            if drone.remainTime < gap/truck.speed:
                                deliverTime += gap/truck.speed
                                drone.remainTime = 0
                            else:
                                deliverTime += gap/truck.speed
                                drone.remainTime -= gap/truck.speed
                        TotalTime += deliverTime
                        TotalGHG += gap * truck.ghg
                        customerSatisfaction = location[nextTruckDestination].satisfaction/ TotalTime
                        reward = self.al * gap * truck.ghg + self.be * 1/customerSatisfaction
                        truck.destination = nextTruckDestination
                        # truck.route.append(truck.destination)
                        if drone.destination != drone.route[-1]:
                            drone.route.append(drone.destination)
                        if truck.destination != truck.route[-1]:
                            truck.route.append(truck.destination)
                        # print("\n-1 != ")
                        # print(truck.available)
                        # print(drone.available)
                        # print(f'removeT: {truck.destination}')
                        truck.available.remove(truck.destination)
                        if truck.destination in drone.available : 
                            # print(f'removeD: {truck.destination}')
                            drone.available.remove(truck.destination)
                        # print(truck.destination)
                        # print(drone.destination)

                else:
                    truck.available.remove(action)
                    drone.available.remove(action)
                    nextTruckDestination = None
                    if len(truck.available) == 0 :
                        nextTruckDestination = truck.destination
                    else:
                        nextTruckDestination = truck.available[0]    
                        truck.available.remove(nextTruckDestination)
                        # print(f'removeT:truck {nextTruckDestination}')
                        if nextTruckDestination in drone.available:
                            drone.available.remove(nextTruckDestination)
                            # print(f'removeD:truck {nextTruckDestination}')
                    nextDroneDestination = action
                    if len(truck.available) == 0 :
                        gapDrone = location[drone.destination].distance(location[nextDroneDestination])
                        drone.availableDistance -= gapDrone
                        customerSatisfactionOfDrone = location[nextDroneDestination].satisfaction/(TotalTime + gapDrone/drone.speed)
                        TotalSatisfaction += customerSatisfactionOfDrone 
                        reward = self.al * (gapDrone * drone.ghg ) + self.be * ( 1/customerSatisfactionOfDrone)
                        TotalGHG += gapDrone * drone.ghg 
                        TotalTime += gapDrone/drone.speed
                        # drone.route.append(nextDroneDestination)
                        truck.destination = nextTruckDestination
                        drone.destination = nextDroneDestination
                        if drone.destination != drone.route[-1]:
                            drone.route.append(drone.destination)
                        if truck.destination != truck.route[-1]:
                            truck.route.append(truck.destination)
                    else:
                        gapDrone = location[drone.destination].distance(location[nextDroneDestination])
                        gapTruck = location[truck.destination].distance(location[nextTruckDestination])
                        drone.availableDistance -= gapDrone
                        customerSatisfactionOfDrone = location[nextDroneDestination].satisfaction/(TotalTime + gapDrone/drone.speed)
                        customerSatisfactionOfTruck = location[nextTruckDestination].satisfaction/(TotalTime + gapTruck/truck.speed)
                        TotalSatisfaction += customerSatisfactionOfDrone + customerSatisfactionOfTruck
                        reward = self.al * (gapDrone * drone.ghg + gapTruck * truck.ghg)/2 + self.be * (1/customerSatisfactionOfTruck + 1/customerSatisfactionOfDrone)/2
                        TotalGHG += gapDrone * drone.ghg + gapTruck * truck.ghg
                        TotalTime += min(gapDrone/drone.speed, gapTruck/truck.speed)
                        if gapDrone/drone.speed > gapTruck/truck.speed:
                            drone.remainTime = gapDrone/drone.speed - gapTruck/truck.speed
                            truck.remainTime = 0
                        else:
                            truck.remainTime = gapTruck/truck.speed - gapDrone/drone.speed
                            drone.remainTime = 0
                        # truck.route.append(nextTruckDestination)
                        # drone.route.append(nextDroneDestination)
                        truck.destination = nextTruckDestination
                        drone.destination = nextDroneDestination
                        if drone.destination != drone.route[-1]:
                            drone.route.append(drone.destination)
                        if truck.destination != truck.route[-1]:
                            truck.route.append(truck.destination)
                    # print(truck.destination)
                    # print(drone.destination)
                nextState = f'{truck.destination}|{drone.available}'
                nextAction = self.get_next_action(nextState,drone.available,truck.destination,drone.destination,drone.maxDistance)
                self.update_q_table(state,action,reward,nextState,nextAction,truck.available)
                state = nextState
                action = nextAction
            if drone.destination != truck.destination:
                if drone.availableDistance >= location[truck.destination].distance(location[drone.destination]):
                    drone.route.append(truck.destination)
                    TotalGHG += location[truck.destination].distance(location[drone.destination]) * drone.ghg
                else:
                    truck.route.append(drone.destination)
                    TotalGHG += location[drone.destination].distance(location[truck.destination]) * truck.ghg
            truck.route.append(indexes[0])
            drone.route.append(indexes[0])
            TotalGHG += location[truck.destination].distance(location[indexes[0]]) * truck.ghg
            # TotalResult = TotalGHG 
            TotalResult = self.al * TotalGHG + self.be * 1/TotalSatisfaction
            if TotalResult < solution.Total:
                solution.TruckRoute = truck.route[:]
                solution.DroneRoute = drone.route[:]
                solution.Total = TotalResult
        return solution

main = SarsaD(action=actionForTrainingDrone)
solution = main.train()
with open("D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\SARSA_result.txt","w") as fio:
    fio.write(f'Truck route: {solution.TruckRoute}\n')
    fio.write(f'Drone rpute: {solution.DroneRoute}\n')
    fio.write(f'ans: {solution.Total}\n\n')