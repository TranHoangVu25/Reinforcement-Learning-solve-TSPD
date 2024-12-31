data=[]
drone_speed=0
with open("E:\\SARSA1\\travelling-salesman-problem-tsp\\dataset\\Input_TSPD_48.txt",'r') as f:
    drone_speed=int(f.readline())
    for i in f.readlines():
        x,y=i.split()[1:]
        x=int(x)
        y=int(y)
        point=Sa.Point(x,y)
        data.append(point)
indexes=[i for i in range(len(data))]
route=Sa.run()