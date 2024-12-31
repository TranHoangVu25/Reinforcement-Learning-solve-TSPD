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