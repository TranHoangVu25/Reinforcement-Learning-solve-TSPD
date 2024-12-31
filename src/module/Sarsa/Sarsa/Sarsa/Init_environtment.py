def __init__(self,actions, alpha=0.01, gamma=0.9,epsilon=0.9,drone_speed=drone_speed) -> None:
        self.actions=actions
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=float(1e9)
        self.droneSpeed=drone_speed