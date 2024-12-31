def train(self):
        cp=float(1e9)
        for episode in range(80):
            state=self.actions[0]
            available_actions=self.actions[1:]
            action=self.get_next_action(state,available_actions)
            counting_state=1
            self.ans.append(state)
            while counting_state <= len(self.actions)-1:
                reward=data[state].distance(data[action])
                next_state=action
                available_actions.remove(next_state)
                if not available_actions :
                    available_actions.append(self.actions[0])
                next_action=self.get_next_action(next_state,available_actions)
                self.update_q_table(state,action,reward,next_state,next_action,counting_state)
                self.ans.append(next_state)
                action=next_action
                state=next_state
                counting_state+=1
            distance=0
            for i in range(1,len(self.ans)):
                distance+= data[self.ans[i]].distance(data[self.ans[i-1]]) 
            if distance < cp:
                self.route=self.ans[:]
                cp=distance
            self.ans.clear()