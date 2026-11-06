import struct
import ov001_float574_models_20261101 as P
import ov001_float578_machine_20261101 as M
TABLE=0x0222E100


def profiles():
    rows=[]
    for entry in M.ENTRIES:
        cap=7 if entry==0x0221239C else 6
        for number in[0,1,9,10,99,100,12345,10**cap-1]:
            for secondary in[0,123456,0xFFFFFFFF,0x80000000]:
                for x,y in[(0,0),(255,-32768),(-1,32767)]:rows.append(dict(entry=entry,number=number,secondary=secondary,x=x,y=y,flagsSet=bool(len(rows)&1),sourceDomain=True))
        for number in[0x7FFFFFFF,0x80000000,0xFFFFFFFF]:rows.append(dict(entry=entry,number=number,secondary=123456,x=-32768,y=-1,flagsSet=True,sourceDomain=False))
    return[dict(p,name=f'family-{i:03d}')for i,p in enumerate(rows)]


def model(r):
    p=r['profile'];variant=p['entry']==0x0221239C;cap=7 if variant else 6;offset=0x28 if variant else 0x20;header=0x1E if variant else 0x1F;terminal=1 if variant else 0;before=r['before'];expected=bytearray(before);events=[];returns=[];forward=[];writes=[];x=p['x']&255;y=p['y']if-32768<=p['y']<=32767 else((p['y']&65535)-65536 if p['y']&32768 else p['y']&65535)
    def event(kind,entry,arguments,scope):events.append((kind,entry,[v&0xFFFFFFFF for v in arguments],scope))
    def returned(entry,arguments,values,scope):returns.append((entry,[v&0xFFFFFFFF for v in arguments],[v&0xFFFFFFFF for v in values],scope))
    def store(address,size,value):
        value&=(1<<(size*8))-1;expected[address-M.M.BASE:address-M.M.BASE+size]=value.to_bytes(size,'little');writes.append([address,size,value])
    def flags(target,setting):
        value=struct.unpack_from('<I',expected,target+0x7C-M.M.BASE)[0];store(target+0x7C,4,value|2 if setting else value&~2)
    def math(number,exponent,scope):
        power=10**exponent;quotient=(abs(number)//power)*(-1 if number<0 else 1);remainder=number-quotient*power;arguments=P.words(10)+P.words(exponent);forward.append(arguments);event('native',M.M.CONVERT,[exponent],scope);returned(M.M.CONVERT,[exponent],P.words(exponent),scope);event('native',M.M.POWER,arguments,scope);returned(M.M.POWER,arguments,P.words(power),scope);event('native',M.M.TRUNC,P.words(power),scope);returned(M.M.TRUNC,P.words(power),[power],scope);return power,quotient,remainder
    def divide(number,power,quotient,remainder,scope):event('native',M.M.DIV,[number,power],scope);returned(M.M.DIV,[number,power],[quotient,remainder],scope)
    event('provided',M.M.GETTER,[M.M.HANDLE,0],'large');event('provided',M.M.SETTER,[M.M.TARGETS,header],'large');event('provided',M.POSITION,[M.M.TARGETS,x if variant else x+4,y],'large');event('provided',M.PROPERTY,[M.M.TARGETS,8],'large');x=(x+offset)&255;store(M.M.ROOTOBJ+0x26,2,10);store(M.M.ROOTOBJ+0x10,4,0);remaining=P.signed(p['number']);count=0;width=0
    while True:
        quotient=(abs(remaining)//10)*(-1 if remaining<0 else 1);remainder=remaining-quotient*10;width+=before[TABLE+remainder-M.M.BASE];count+=1;remaining=quotient
        if remaining<=0 or count>=cap:break
    x=(x+56-width)&255;remaining=P.signed(p['number'])
    for exponent in range(count-1,-1,-1):
        power,quotient,remainder=math(remaining,exponent,'large');target=M.M.TARGETS+(exponent+1)*256;event('provided',M.M.GETTER,[M.M.HANDLE,exponent+1],'large');event('provided',M.POSITION,[target,x,y],'large');event('provided',M.PROPERTY,[target,7],'large');flags(target,False);divide(remaining,power,quotient,remainder,'large');x=(x+before[TABLE+(quotient&255)-M.M.BASE])&255;divide(remaining,power,quotient,remainder,'large');remaining=remainder
    event('source-dependency',M.M.ENTRY,[M.M.ROOTOBJ,7,p['secondary']],'large');secondary=P.signed(p['secondary']);smallcount=min(len(str(secondary))if secondary>0 else 1,6)
    for exponent in range(smallcount-1,-1,-1):
        power,quotient,remainder=math(secondary,exponent,'small');target=M.M.TARGETS+(exponent+1)*256;event('provided',M.M.GETTER,[M.M.HANDLE,exponent+1],'small');divide(secondary,power,quotient,remainder,'small');event('provided',M.M.SETTER,[target,quotient&255],'small');flags(target,True);divide(secondary,power,quotient,remainder,'small');secondary=remainder
    returned(M.M.ENTRY,[M.M.ROOTOBJ,7,p['secondary']],[0],'large');store(M.M.ROOTOBJ+0x23,1,terminal)
    if len(r['callEvents'])!=len(events):raise ValueError(('578 independent event count differs',p['name'],len(r['callEvents']),len(events)))
    for actual,(kind,entry,arguments,scope)in zip(r['callEvents'],events):
        if actual['kind']!=kind or actual['entry']!=entry or actual['scope']!=scope or actual['words'][:len(arguments)]!=arguments:raise ValueError(('578 independent call input differs',p['name'],actual,arguments))
    named=[row for row in r['nativeReturns']if row['scope']!='nested_math']
    if len(named)!=len(returns):raise ValueError(('578 named return count differs',p['name'],len(named),len(returns)))
    for actual,(entry,arguments,values,scope)in zip(named,returns):
        if actual['entry']!=entry or actual['scope']!=scope or actual['inputWords'][:len(arguments)]!=arguments or actual['returnedWords'][:len(values)]!=values:raise ValueError(('578 independent return contract differs',p['name'],entry))
    if r['powerTargetWords']!=forward or[[address,size,value]for pc,address,size,value in r['nonstackWrites']]!=writes:raise ValueError(('578 forwarding/ordered stores differ',p['name']))
    stack=M.M.STACK-M.M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError(('578 independent full RAM differs',p['name']))
    if r['returnedWords'][0]!=terminal:raise ValueError(('578 physical return differs',p['name']))
    return dict(layoutCount=count,smallCount=smallcount,terminalByte=terminal,providedCalls=sum(kind=='provided'for kind,entry,args,scope in events),namedDirectAndSmallNativeReturns=len(returns),originalSmallDependencyReturns=1,sourceDomain=p.get('sourceDomain',True),ownOrderedWrites=writes)
