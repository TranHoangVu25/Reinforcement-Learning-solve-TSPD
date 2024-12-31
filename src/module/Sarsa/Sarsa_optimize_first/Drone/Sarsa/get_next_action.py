def get_next_action(self,state,available_action):
        self.check_if_state_action_exist(state)
        tmp_actions=ten_best(available_action,state)
        if random.uniform(0,1) < self.epsilon :
            index=None
            min_value= float(1e7)
            np.random.shuffle(tmp_actions)
            for action in tmp_actions:
                if self.q_table.loc[state, action] < min_value:
                    index=action
                    min_value=self.q_table.loc[state, action]
            target_action = index
        else:
            target_action=random.choice(tmp_actions)
        return target_action