import struct
import ov000_birth388_fixture_20261031 as F

def word(raw,address,size=4):return int.from_bytes(raw[address-F.BASE:address-F.BASE+size],'little')

def check(obj,result,assets):
    p=result['profile'];phase=0 if p.get('outAlias')=='phase'else p['phase'];action=0 if p.get('outAlias')=='action'else p['action'];option=p['option']
    expected=p['phase']if p['phase']<128 else p['phase']-256
    owned={};builder=False;dialog=False;predicate=None
    owned[obj.outAddress]=(4,0)
    owned[F.CONTEXT]=(4,action)
    if p.get('outAlias')=='phase':owned[F.CONTEXT+16]=(4,0)
    else:owned[F.CONTEXT+16]=(1,p['phase'])
    owned[F.VIEW+7]=(1,0x7E);owned[F.VIEW+48]=(4,0);owned[obj.rawState+1]=(1,0x69)
    category=((int.from_bytes(assets['EnmyKindTbl.bin'][8+100*obj.species+4:8+100*obj.species+6],'little')>>8)&15)//3
    gate=category!=2 or p.get('feature',p['policy'])!=0
    if phase==0:
        if action==0:expected=1
        if action==1:owned[F.VIEW+7]=(1,8)
    elif phase==1:
        common=action<=1 or action==2 and option!=0
        if common:predicate=bool(p['policy'])if action in[0,1]else True
        else:
            predicate=bool(p['policy'])and gate
            if p['policy']:owned[F.CHOICE+3]=(1,(action-(3 if option else 2))&255)
        if action in[0,1]:expected=2 if predicate else 1
        elif action==2 and option:expected=3
        elif predicate:expected=8;builder=True
        else:dialog=True;owned[F.VIEW+7]=(1,5);owned[obj.rawState+1]=(1,p['rawByte'])
    elif phase==2:
        if p['ready']!=0:expected=1
    elif phase==3:
        if p['ready']!=0:expected=1
    elif phase==8:
        expected=9 if p['ready']<=0 else 8;owned[obj.outAddress]=(4,1)
    elif phase==9:
        if action==0:expected=6;owned[F.VIEW+48]=(4,1)
        if action==1:expected=8
    elif phase==10:
        if p['ready']!=0:expected=11
        elif p.get('menu',p['ready'])==2:owned[F.VIEW+7]=(1,5)
    elif phase==11:
        if action==0:expected=1
        if action==1:owned[F.VIEW+7]=(1,8)
    after=bytes(obj.u.mem_read(F.BASE,0x800000))
    if result['returnWord']!=(expected&0xFFFFFFFF):raise ValueError('Birth388 independent return model differs')
    for address,(size,value)in owned.items():
        if word(after,address,size)!=value:raise ValueError(('Birth388 independent caller field differs',hex(address),word(after,address,size),value))
    predicate_calls=[r for r in result['trace']if r['entry']=='0x22207a0']
    if len(predicate_calls)!=(1 if phase==1 else 0)or any(r['arguments'][:2]!=[F.CONTEXT,option]for r in predicate_calls):raise ValueError('Birth388 required predicate input contract differs')
    actual_predicate=[r['result']for r in result['nativeReturns']if r['entry']=='0x22207a0']
    if actual_predicate!=([]if predicate is None else[int(predicate)]):raise ValueError('Birth388 independent native predicate model differs')
    builder_calls=[r for r in result['trace']if r['entry']=='0x2229100']
    if len(builder_calls)!=int(builder)or len(result['builderChecks'])!=int(builder):raise ValueError('Birth388 builder boundary differs')
    if builder:
        expected_args=[int.from_bytes(obj.parents[0][20:24],'little'),int.from_bytes(obj.parents[1][20:24],'little'),obj.species,0]
        if builder_calls[0]['arguments']!=expected_args or builder_calls[0]['stackWords'][0]!=0 or word(after,F.VIEW+40)!=F.SCRATCH:raise ValueError('Birth388 independent builder inputs/pointer forwarding differ')
        selector=[r for r in result['trace']if r['entry']=='0x22298ec']
        returned=[r['result']for r in result['nativeReturns']if r['entry']=='0x22298ec']
        if len(selector)!=1 or selector[0]['arguments']!=expected_args or selector[0]['stackWords'][0]!=0x022460B4 or word(after,F.VIEW+28)!=returned[0]:raise ValueError('Birth388 native selection return forwarding differs')
    setters=[r for r in result['trace']if r['entry']=='0x20c484c']
    if len(setters)!=int(dialog)or any(r['arguments'][0]!=p['rawByte']for r in setters):raise ValueError('Birth388 clean raw-byte forwarding differs')
    if dialog:
        messages=[r['arguments'][:3]for r in result['trace']if r['entry']=='0x20c48d0']
        expected_message=[5,6,43]if not gate else[9,0,16]if p.get('level',10)<10 else[9,0,17]
        if messages!=[expected_message]:raise ValueError('Birth388 independent raw message branch differs')
    if result['scratch33Writes']or result['scratch33After']!=p['scratch33']:raise ValueError('Birth388 unsupported scratch33 initializer observed')
    for i in range(100):
        address=0x021BD674+132*i+51
        if word(obj.before,address,1)!=word(after,address,1):raise ValueError('Birth388 saved raw33 unexpectedly changed')
    return dict(returnWord=expected&0xFFFFFFFF,outputWord=result['outWord'],predicateExpected=predicate,builderExpected=builder,dialogExpected=dialog,callerFieldsIndependentlyChecked=len(owned),nestedBuilderFullIndependentNonstackRam=bool(builder),pairedFullNonstackRam=True,independentFullCallerNonstackRam=False,scratch33Input=p['scratch33'],scratch33Writes=0,savedRecord33Unchanged=True,limits='Native selection-result contents and native roster-rebuild bitmap effects are paired and hash-compared,but not independently semantically modeled; supplied UI callbacks do not establish real lifecycle')
