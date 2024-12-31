def get_next_action(self,state,indexes):
        self.check_if_state_action_exist(state)
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(indexes)
            for action in indexes:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(indexes)
        return target_action