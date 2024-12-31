def result_q_truck():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\result_q_learning.txt'
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()  # Đọc dòng đầu tiên và loại bỏ khoảng trắng/thừa
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    truck_route_q = [float(x) for x in first_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return truck_route_q

def result_q_drone():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\result_q_learning.txt'
    with open(file_path, 'r') as file:
        file.readline()
        second_line = file.readline().strip()
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    drone_route_q = [float(x) for x in second_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return drone_route_q

def emissions_q():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\result_q_learning.txt'
    with open(file_path, 'r') as file:
        file.readline()
        file.readline()
        second_line = file.readline().strip()
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    emissions = [float(x) for x in second_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return emissions

def result_sarsa_truck():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\SARSA_result.txt'
    with open(file_path, 'r') as file:
        file.readline()
        second_line = file.readline().strip()
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    truck_route_sarsa = [float(x) for x in second_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return truck_route_sarsa

def result_sarsa_drone():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\SARSA_result.txt'
    with open(file_path, 'r') as file:
        file.readline()
        third_line = file.readline().strip()
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    drone_route_sarsa = [float(x) for x in third_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return drone_route_sarsa

def emissions_sarsa():
    file_path = 'D:\\Tran Hoang Vu\\Lab\\VRDP\\Large Nearest Search (LNS)\\q_and_sarsa\\travelling-salesman-problem-tsp\\result\\raw\\SARSA_result.txt'
    with open(file_path, 'r') as file:
        file.readline()
        file.readline()
        third_line = file.readline().strip()
    
    # Chuyển dòng đầu tiên thành danh sách các số (nếu cần)
    emissions = [float(x) for x in third_line.split()]  # Tách bằng khoảng trắng hoặc dấu phân cách khác nếu cần
    return emissions