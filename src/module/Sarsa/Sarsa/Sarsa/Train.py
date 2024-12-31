def train(self):
        for episode in range(60):
            tmp_ans=0.0
            state=State()
            action=Action()
            action.init(self.get_next_action(state.convertToString())) 
            while len(state.not_vistied)!=0 :
                next_state=State()
                next_state.init(state.convertToString())
                next_state.remainingTimeOfTruck += (city[state.current_truck].dis_bet(city[action.truck]))
                next_state.remainingTimeOfDrone += (city[state.current_drone].dis_bet(city[action.drone])/self.droneSpeed)
                if action.truck == action.drone:
                    Ct=max(next_state.remainingTimeOfTruck,next_state.remainingTimeOfDrone)
                    next_state.remainingTimeOfTruck =0.0
                    next_state.remainingTimeOfDrone =0.0
                else:
                    Ct=min(next_state.remainingTimeOfTruck,next_state.remainingTimeOfDrone)
                    next_state.remainingTimeOfTruck -= Ct
                    next_state.remainingTimeOfDrone -= Ct
                reward=Ct
                tmp_ans+=Ct
                next_state.current_truck=action.truck
                next_state.current_drone=action.drone
                if action.truck in next_state.not_vistied:
                    next_state.not_vistied.remove(action.truck)
                if action.drone in next_state.not_vistied:
                    next_state.not_vistied.remove(action.drone)
                if len(next_state.not_vistied) == 0:
                    next_action=action
                    next_action.init(f'{next_state.current_truck}|{next_state.current_drone}')
                else:
                    next_action=action
                    next_action.init(self.get_next_action(next_state.convertToString()))
                self.update_q_table(state.convertToString(),action.convertToString(),reward,next_state.convertToString(),next_action.convertToString())
                state=next_state
                action=next_action
            tmp_ans+=max(state.remainingTimeOfDrone , state.remainingTimeOfTruck)
            tmp_ans+=max(city[state.current_truck].dis_bet(city[0]),city[state.current_drone].dis_bet(city[0])/drone_speed)
            print(tmp_ans)
            if tmp_ans < self.ans:
                self.ans=tmp_ans
