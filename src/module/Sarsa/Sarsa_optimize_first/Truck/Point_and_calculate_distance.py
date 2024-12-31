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