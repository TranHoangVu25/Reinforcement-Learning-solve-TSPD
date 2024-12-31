def get_next_action(self,stringState:str):
        self.check_if_state_action_exist(stringState)
        state=State()
        state.init(stringState)
        available_action=[]
        if state.remainingTimeOfTruck == state.remainingTimeOfDrone :
            if state.current_truck==state.current_drone:
                if len(state.not_vistied)>10:
                    # tmp_not_visited=state.not_vistied[:]
                    available_city_truck=[]
                    available_city_drone=[]
                    # while len(available_city)<10:
                    #     available_city.append(tmp_not_visited.pop(random.randint(0,len(tmp_not_visited)-1))) 
                    available_city_truck=ten_best(state.not_vistied,state.current_truck)
                    available_city_drone=ten_best(state.not_vistied,state.current_drone)
                    for i in available_city_truck:
                        for j in available_city_drone:
                            available_action.append(f'{i}|{j}')
                else:
                    for i in state.not_vistied:
                        for j in state.not_vistied:
                            available_action.append(f'{i}|{j}')
            else:
                available_city_truck=[]
                available_city_truck=ten_best(state.not_vistied,state.current_truck)
                for i in available_city_truck:
                    available_action.append(f'{i}|{i}')
        elif state.remainingTimeOfTruck < state.remainingTimeOfDrone :
            available_city_truck=[]
            available_city_truck=ten_best(state.not_vistied,state.current_truck)
            for i in available_city_truck:
                available_action.append(f'{i}|{state.current_drone}')
        elif state.remainingTimeOfTruck > state.remainingTimeOfDrone :
            available_action.append(f'{state.current_truck}|{state.current_truck}')
        if random.uniform(0,1) <  self.epsilon:
            index=None
            min_value = float(1e7)
            np.random.shuffle(available_action)
            for action in available_action:
                if self.q_table.loc[stringState,action] < min_value:
                    index = action
                    min_value = self.q_table.loc[stringState,action]
            target_action=index
        else:
            target_action=random.choice(available_action)
        # this gonna return string, don't be a d*ck=)
        return target_action
