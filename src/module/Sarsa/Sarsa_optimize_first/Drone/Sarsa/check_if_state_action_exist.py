def check_if_state_action_exist(self,state):
        if state not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(0)] * len(self.actions),
                    index=self.q_table.columns,
                    name=state
                )
            )