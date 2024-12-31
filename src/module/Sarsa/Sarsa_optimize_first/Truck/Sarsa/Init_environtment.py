def __init__(self,action, alpha=0.01, gamma=0.9,epsilon=0.99) -> None:
        self.actions=action
        self.alpha=alpha
        self.gamma=gamma
        self.epsilon=epsilon
        self.q_table=pd.DataFrame(columns=self.actions,dtype=float)
        self.ans=[]
        self.route=[]
