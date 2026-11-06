import itertools
def cases():
    result=[]
    for index,(mode,preamble,wep,power,operation,bssid)in enumerate(itertools.product(range(5),(False,True),(0,1),(0,1),(0,8,32,40),(0,1))):
        result.append(dict(mode=mode,shortPreamble=preamble,wep=wep,power=power,operation=operation,bssid=bssid,initializeLists=True,sequence=(0,1,0x8000,0xffff)[index%4],tsf=(0,1,0xffffffff,0xffffffffffffffff)[index%4],beaconPeriod=(1,100,1000)[index%3],maxSta=(1,2)[index%2],contextOffset=(0,4,0x100)[index%3]))
    for value,preamble in itertools.product((0,1,1<<32,0xffffffffffffffff),(False,True)):
        result.append(dict(mode=1,shortPreamble=preamble,initializeLists=True,beaconPeriod=0,tsf=value,power=1,contextOffset=4))
    for mode in(5,65535):result.append(dict(mode=mode,initializeLists=True,contextOffset=0x100,rawModeProducerValidityUnproved=True))
    for mode in(0,3):result.append(dict(mode=mode,initializeLists=True,signal=0,contextOffset=4))
    result.append(dict(mode=1,initializeLists=True,beaconPeriod=65535,tsf=0xffffffffffffffff,contextOffset=0x100))
    return result
