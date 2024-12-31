def check_if_state_action_exist(self,stringState):
        if stringState not in self.q_table.index:
            self.q_table=self.q_table._append(
                pd.Series(
                    [float(1e4)]*len(self.actions),
                    index=self.actions,
                    name=stringState
                )
            )