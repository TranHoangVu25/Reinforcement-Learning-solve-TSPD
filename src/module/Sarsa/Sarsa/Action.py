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
