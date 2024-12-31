class Point():
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
    def dis_bet(self,value: object):
        return math.sqrt((self.x - value.x)**2+(self.y - value.y)**2)
    def __str__(self) -> str:
        return f'{self.x},{self.y}'