def creatState(s:str):
    tmp=s.split("|")
    li=convertListString(tmp[0])
    cr_tr=int(tmp[1])
    cr_dr=int(tmp[2])
    re_ti_tr=float(tmp[3])
    re_ti_dr=float(tmp[4])
    return li,cr_tr,cr_dr,re_ti_tr,re_ti_dr