SP=0x027fc000
STOP=0x02010000


def fixtures():
    rows=[]
    for operation in range(23):
        for value in [0,1,3,0x12ab,65535]:rows.append(dict(entry=0x03804d40,operation=operation,value=value,register=0xa5,pattern=0x1234abcd))
    for value in range(8):
        for register in [0,1,0xff]:rows.append(dict(entry=0x03804d40,operation=15,value=value,register=register,pattern=0xffffffff if register else 0))
    rows.append(dict(entry=0x03804d40,operation=0xffffffff,value=65535,register=0xff,pattern=0xffffffff))
    return rows


def scenario(f,ordinal):
    actions=[];operation,value=f['operation'],f['value'];returned=0
    def action(at,args=(),result=0):actions.append(dict(address=at,args=list(args),returned=result,checks=[],mutations=[]))
    if operation in [1,2,3]:
        pattern={1:1,2:3,3:2}[operation];action(0x0380528c,[pattern]);action(0x03804f54,[pattern])
    elif operation in [4,6,8,10,13]:action(0x03804cf0,[{4:4,6:8,8:12,10:1,13:2}[operation]])
    elif operation in [5,7,9,11,12]:action(0x03804d14,[{5:4,7:8,9:12,11:1,12:2}[operation]])
    elif operation==14:action(0x037fe708);action(0x03804cf0,[64])
    elif operation==15:
        if value in [0,1,2,4,5]:
            index,mask={0:(1,1),1:(0,12),2:(0,1),4:(2,1),5:(3,3)}[value];action(0x03804c7c,[index],f['register']);returned=f['register']&mask
        elif value==6:action(0x038052a8,result=f['pattern']);returned=f['pattern']&65535
        elif value!=3:returned=2
    elif operation==16:action(0x03804c00,[2,value&1])
    elif operation==17:action(0x03804c00,[3,value&3])
    elif operation==18:action(0x0380528c,[value])
    elif operation==19:action(0x03804c7c,[value],f['register']);returned=f['register']
    elif operation==20:action(0x03804c00,[(value>>8)&255,value&255])
    return dict(args=[operation,value],initial={},regions={},actions=actions,allowedWriteRanges=[],frame=8,returnValue=returned)
