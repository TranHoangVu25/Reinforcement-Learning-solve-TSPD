def ten_best(li:list,pos_vi:int):
    tmp=li[:]
    tmp.sort(key=lambda pos: city[pos].dis_bet(city[pos_vi]))
    if len(tmp)>10:
        return tmp[:10]
    return tmp