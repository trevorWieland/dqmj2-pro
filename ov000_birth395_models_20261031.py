import struct
import ov000_birth395_fixture_20261031 as G
import prove_ov000_selection333_20261031 as S
F=G.F

def read(raw,address,size=4):return int.from_bytes(raw[address-F.BASE:address-F.BASE+size],'little')
def keyed(raw):return{int.from_bytes(raw[i+20:i+24],'little'):raw[i:i+132]for i in range(0,len(raw),132)if int.from_bytes(raw[i+20:i+24],'little')}
def compact(values,parents):
    result=[]
    for block in[values[:3],values[3:]]:
        block=list(block)
        for i in range(3):
            if block[i]in parents:
                for j in range(i,2):block[j]=block[j+1]
                block[-1]=0
        result.extend(block)
    return result

def commit_model(obj,before,returned):
    old=keyed(before['rows']);parents=[old[uid]for uid in before['parents']];scratch=before['scratch'];species=int.from_bytes(scratch[24:26],'little');table=obj.assets['ItemTbl.bin'][8:];flags=int.from_bytes(obj.assets['EnmyKindTbl.bin'][8+100*species+4:8+100*species+6],'little')
    selector,rng,draws=S.model(table[88*parents[0][49]+42],table[88*parents[1][49]+42],before['rng'],bool(flags&0x8000))
    uid=(before['counter']+1)&0xFFFFFFFF;child=bytearray(132);child[20:24]=struct.pack('<I',uid);child[24:27]=scratch[24:27];child[32:64]=scratch[32:64];child[64:122]=scratch[64:122];child[27]=selector
    for offset in[28,29,30]:child[offset]=scratch[offset]
    expected=dict(old)
    for parent in set(before['parents']):expected.pop(parent)
    expected[uid]=bytes(child)
    actual=keyed(bytes(obj.u.mem_read(0x021BD674,13200)));groups=list(struct.unpack('<6I',obj.u.mem_read(0x021BD540,24)))
    if actual!=expected or returned!=uid or groups!=compact(before['groups'],set(before['parents']))or obj.read_word(0x021BD520)!=uid or obj.read_word(0x020F6044)!=rng:raise ValueError('Birth395 independent native commit record/group/counter/RNG differs')
    return dict(returnedUid=uid,parentUids=before['parents'],raw33=child[51],beforeLiveRecords=len(old),afterLiveRecords=len(actual),groupsBefore=before['groups'],groupsAfter=groups,rngAfter=rng,expectedRngDraws=draws,independentAllLiveRecords=True)

def check(obj,result):
    p=result['profile'];controller=p['controller'];phase=p['phase'];kind=p.get('kind',0);option=p['option'];menu=p.get('menu',16);before=obj.before;after=bytes(obj.u.mem_read(F.BASE,0x800000))
    expected=1;phasewrite=None;field6=0;ctxaction=p['action']
    if controller==1 and phase not in[2,3]:
        if phase in[0,11]and menu!=16:expected=0
        else:
            field6=1
            if kind==8:ctxaction=read(before,F.CHOICE+3,1)+(3 if option else 2)
    if controller==8 and phase!=9 and menu!=8:expected=0
    if result['returnWord']!=expected:raise ValueError('Birth395 independent controller return differs')
    if read(after,F.VIEW+6,1)!=field6 or read(after,F.CONTEXT)!=ctxaction:raise ValueError('Birth395 independent controller state field differs')
    listcount=p.get('listCount',2);listcount=listcount if listcount<0x80000000 else listcount-0x100000000;expected_pops=0
    if controller==0 and phase==1:expected_pops=max(0,listcount-option-1)
    if controller==1 and phase not in[2,3]and expected:
        if phase==0:expected_pops=max(0,listcount-option-1)
        if phase==11:expected_pops=max(0,listcount-1)
    if controller==8:
        if phase==9:expected_pops=max(0,listcount-1)
        elif menu==8:expected_pops=max(0,listcount)
    if controller==9:expected_pops=max(0,listcount-1)
    pops=[r for r in result['trace']if r['entry']=='0x221cf60']
    if len(pops)!=expected_pops:raise ValueError('Birth395 independent list-pop loop bound differs')
    for row in result['trace']:
        if row['entry']in['0x221fa70','0x2220160']and row['arguments'][:2]!=[F.CONTEXT,0]:raise ValueError('Birth395 required GUI context/zero option differs')
    if controller==6:
        if len(result['commitChecks'])!=1:raise ValueError('Birth395 native replacement boundary missing')
        uid=result['commitChecks'][0]['returnedUid'];rawcount=p.get('skills',0)&255;count=rawcount if rawcount<128 else rawcount-256
        if read(after,F.VIEW+12)!=uid or read(after,F.VIEW+28)!=(count&0xFFFFFFFF)or read(after,F.VIEW+36)!=0x02620000:raise ValueError('Birth395 native UID/count/pointer forwarding differs')
        calls=[r for r in result['trace']if r['entry']=='0x2062e44'];expected_calls=[[uid,index,0x02620000+2*(count-index-1)]for index in range(max(0,count))]
        if[r['arguments'][:3]for r in calls]!=expected_calls:raise ValueError('Birth395 independent reverse slot/buffer inputs differ')
        row=bytes(obj.u.mem_read(obj.record(uid),132));expected_slots=b''.join(bytes([index,0])for index in range(max(0,count),0,-1))+bytes(10-2*max(0,count))
        if row[122:132]!=expected_slots or row[51]!=0:raise ValueError('Birth395 independent child packed slots/raw33 differs')
        expected_tally=min((p.get('tally',0)+1)&65535,obj.counterLimit)
        oldgold=read(before,obj.goldAddress);cost=p.get('cost',-1);gold=oldgold if cost==-1 else min(obj.goldLimit,max(0,oldgold-cost))
        if read(after,obj.counterAddress,2)!=expected_tally or read(after,obj.goldAddress)!=gold:raise ValueError('Birth395 native tally/gold arithmetic differs')
        events=result['lifecycle'];writer=[r for r in events if r['stage']=='native-write']
        if len(writer)!=1 or writer[0]['uid']!=uid or writer[0]['before']!=p['scratch33']or writer[0]['value']!=0:raise ValueError('Birth395 original saved raw33 writer differs')
        if[stage['stage']for stage in events]!=['after-commit','before-refresh','native-write']:raise ValueError('Birth395 raw33 caller boundary order differs')
    else:
        if result['commitChecks']or result['lifecycle']:raise ValueError('Birth395 unexpected destructive path')
    if result['scratch33Writes']or result['scratch33After']!=p['scratch33']:raise ValueError('Birth395 scratch33 must remain supplied')
    return dict(returnWord=expected,listPops=expected_pops,requiredGuiOptionWord=0,raw33SavedClearExpected=controller==6,scratch33Preserved=p['scratch33'],wholeCallerOriginalSourceRamAndTracePaired=True,independentAllCallerRam=False,independentCommitLiveRecordGroupRng=controller==6,unsupported='Real UI lifecycle and reachability, null/broken records, duplicate parents, exhausted allocation,counterwrap andpositive skill counts>3 remain outside this caller fixture')
