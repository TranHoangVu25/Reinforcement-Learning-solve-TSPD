def update_q_table(self,stringState:str,stringAction,reward,stringNextSate,stringNextAction):
        self.check_if_state_action_exist(stringNextSate)
        next_state=State()
        next_state.init(stringNextSate)
        q_value_predict=self.q_table.loc[stringState,stringAction]
        if len(next_state.not_vistied) != 0:
            q_value_real = reward + self.gamma * self.q_table.loc[stringNextSate,stringNextAction]
        else:
            q_value_real = reward
        self.q_table.loc[stringState,stringAction] += self.alpha * ( q_value_real - q_value_predict )
    