import matplotlib.pyplot as plt 


def plot_route_truck_q(data,route):
    plt.figure(figsize=(10,8))

    for city in range (len(data)):
        plt.scatter(data[city,1],data[city,2], c='blue',label='City' if city ==0 else "")
        plt.text(data[city, 1], data[city, 2], str(city), fontsize=15, color='green')
        for i in range(len(route) -1):
            city1 = route[i]
            city2 = route[i+1]
            plt.plot(
                [data[city1, 1], data[city2, 1]],
                [data[city1, 2], data[city2, 2]],
                c='red', linewidth=1.5
            )
	
  
    city_last = route[-1]
    city_start = route[0]
    plt.plot(
        [data[city_last, 1], data[city_start, 1]],
        [data[city_last, 2], data[city_start, 2]],
        c='red', linewidth=1.5,label='Truck route'
    )

    # Thiết lập tiêu đề và chú thích
    plt.title("Truck's route (Q-learning)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.savefig("D:\\Tran Hoang Vu\\Lab\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\figure\\truck_route_qlearning.png")
    plt.close() 
    # plt.show()




def plot_route_drone_q(data,route):
    plt.figure(figsize=(10,8))

    for city in range (len(data)):
        plt.scatter(data[city,1],data[city,2], c='blue',label='City' if city ==0 else "")
        plt.text(data[city, 1], data[city, 2], str(city), fontsize=15, color='green')
        for i in range(len(route) -1):
            city1 = route[i]
            city2 = route[i+1]
            plt.plot(
                [data[city1, 1], data[city2, 1]],
                [data[city1, 2], data[city2, 2]],
                c='red', linewidth=1.5
            )
	
  
    city_last = route[-1]
    city_start = route[0]
    plt.plot(
        [data[city_last, 1], data[city_start, 1]],
        [data[city_last, 2], data[city_start, 2]],
        c='red', linewidth=1.5,label='Drone route'
    )

    # Thiết lập tiêu đề và chú thích
    plt.title("Drone's route (Q-learning)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.savefig("D:\\Tran Hoang Vu\\Lab\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\figure\\drone_route_qlearning.png")
    plt.close() 
    # plt.show()

def plot_route_drone_s(data,route):
    plt.figure(figsize=(10,8))

    for city in range (len(data)):
        plt.scatter(data[city,1],data[city,2], c='blue',label='City' if city ==0 else "")
        plt.text(data[city, 1], data[city, 2], str(city), fontsize=15, color='green')
        for i in range(len(route) -1):
            city1 = route[i]
            city2 = route[i+1]
            plt.plot(
                [data[city1, 1], data[city2, 1]],
                [data[city1, 2], data[city2, 2]],
                c='red', linewidth=1.5
            )
	
  
    city_last = route[-1]
    city_start = route[0]
    plt.plot(
        [data[city_last, 1], data[city_start, 1]],
        [data[city_last, 2], data[city_start, 2]],
        c='red', linewidth=1.5,label='Drone route'
    )

    # Thiết lập tiêu đề và chú thích
    plt.title("Drone's route (SARSA)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.savefig("D:\\Tran Hoang Vu\\Lab\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\figure\\drone_route_SARSA.png")
    plt.close() 
    # plt.show()

def plot_route_truck_s(data,route):
    plt.figure(figsize=(10,8))

    for city in range (len(data)):
        plt.scatter(data[city,1],data[city,2], c='blue',label='City' if city ==0 else "")
        plt.text(data[city, 1], data[city, 2], str(city), fontsize=15, color='green')
        for i in range(len(route) -1):
            city1 = route[i]
            city2 = route[i+1]
            plt.plot(
                [data[city1, 1], data[city2, 1]],
                [data[city1, 2], data[city2, 2]],
                c='red', linewidth=1.5
            )
	
  
    city_last = route[-1]
    city_start = route[0]
    plt.plot(
        [data[city_last, 1], data[city_start, 1]],
        [data[city_last, 2], data[city_start, 2]],
        c='red', linewidth=1.5,label='Truck route'
    )

    # Thiết lập tiêu đề và chú thích
    plt.title("Truck's route (SARSA)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.savefig("D:\\Tran Hoang Vu\\Lab\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\figure\\truck_route_SARSA.png")
    # plt.show()
    plt.close() 