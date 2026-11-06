import struct
import ov001_float574_machine_20261101 as M


def signed(value):
    value&=0xFFFFFFFF
    return value if value<0x80000000 else value-0x100000000


def words(value):return list(struct.unpack('<II',struct.pack('<d',float(value))))


def profiles():
    rows=[]
    for limit in[-2,-1,0,1,2,3,4,8,11,12,0x7FFFFFFF,0x80000000]:
        for number in[0,1,9,10,99,100,123456789,2147483647,0x80000000,0xFFFFFFFF]:rows.append(dict(name=f'float-{len(rows):03d}',limit=limit,number=number,flagsSet=bool(len(rows)&1)))
    return rows


def model(r):
    p=r['profile'];number=signed(p['number']);bound=signed(p['limit']-1);count=0 if bound<=0 else min(len(str(number))if number>0 else 1,bound);expected=bytearray(r['before']);events=[];returns=[];forward=[];writes=[]
    def event(kind,entry,arguments):events.append((kind,entry,[x&0xFFFFFFFF for x in arguments]))
    def returned(entry,arguments,values):returns.append((entry,[x&0xFFFFFFFF for x in arguments],[x&0xFFFFFFFF for x in values]))
    for exponent in range(count-1,-1,-1):
        power=10**exponent;target=M.TARGETS+(exponent+1)*256;quotient=(abs(number)//power)*(-1 if number<0 else 1);remainder=number-quotient*power;expwords=words(exponent);powerwords=words(power);powerargs=words(10)+expwords;forward.append(powerargs)
        event('native',M.CONVERT,[exponent]);returned(M.CONVERT,[exponent],expwords);event('native',M.POWER,powerargs);returned(M.POWER,powerargs,powerwords);event('native',M.TRUNC,powerwords);returned(M.TRUNC,powerwords,[power]);event('provided',M.GETTER,[M.HANDLE,exponent+1]);event('native',M.DIV,[number,power]);returned(M.DIV,[number,power],[quotient,remainder]);event('provided',M.SETTER,[target,quotient&255]);address=target+0x7C;value=struct.unpack_from('<I',expected,address-M.BASE)[0]|2;struct.pack_into('<I',expected,address-M.BASE,value);writes.append([address,4,value]);event('native',M.DIV,[number,power]);returned(M.DIV,[number,power],[quotient,remainder]);number=remainder
    actual=r['callEvents']
    if len(actual)!=len(events):raise ValueError(('574 independent call count differs',p['name'],len(actual),len(events)))
    for record,(kind,entry,arguments)in zip(actual,events):
        if record['kind']!=kind or record['entry']!=entry or record['words'][:len(arguments)]!=arguments:raise ValueError(('574 independent native/provided input differs',p['name'],record,arguments))
    direct=[record for record in r['nativeReturns']if record['direct']]
    if len(direct)!=len(returns):raise ValueError('574 direct native return count differs')
    for record,(entry,arguments,values)in zip(direct,returns):
        if record['entry']!=entry or record['inputWords'][:len(arguments)]!=arguments or record['returnedWords'][:len(values)]!=values:raise ValueError(('574 independent native return contract differs',p['name'],entry))
    if r['powerTargetWords']!=forward:raise ValueError(('574 actual power veneer forwarding differs',p['name']))
    if [[address,size,value]for pc,address,size,value in r['nonstackWrites']]!=writes:raise ValueError(('574 independent ordered own writes differ',p['name']))
    stack=M.STACK-M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError(('574 independent full RAM differs',p['name']))
    if r['returnedWords'][0]!=0:raise ValueError('574 physical top R0 differs')
    return dict(count=count,selectorBytes=[entry[2][1]for entry in events if entry[0]=='provided'and entry[1]==M.SETTER],ownWrites=writes,directNativeReturns=len(returns),providedCalls=2*count,rawLimitWrapModeled=True,intMinLimitCase=signed(p['limit'])==-2147483648)
