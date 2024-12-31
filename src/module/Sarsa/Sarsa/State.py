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
