def convertListString(s):
    li=[]
    for i in s.split(",")[:-1]:
        li.append(int(i))
    return li