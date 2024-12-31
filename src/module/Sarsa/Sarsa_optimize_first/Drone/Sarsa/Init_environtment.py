def __init__(self,route,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.route=route
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=0
        self.route_truck=[]
        self.route_drone=[]
