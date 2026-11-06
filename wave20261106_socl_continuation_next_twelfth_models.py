from wave20261106_socl_continuation_next_ninth_models import Plan
from wave20261106_socl_continuation_next_twelfth_callbacks import TARGETS,CONTRACTS

CTX,OTHER,OUT,SOCKET,INPUT,RECORD,SP,STOP=0x02400000,0x02402000,0x02410000,0x02420000,0x02430000,0x02440000,0x027f0000,0x027d0000
ALLOCATE,RELEASE=0x021cfd0c,0x021cfd38
SPECS={'02092854':24,'020928f8':8,'02092938':24}
NAMES=list(SPECS)


def fixtures(name):
    cases={'02092854':['held','read-error','parse-held','parse-clear-fill','empty-fill','empty-error','parse-clear-error'],'020928f8':['partial','exact','larger','null-exact','wrap-partial','zero-remaining'],'02092938':['short-header','no-input','oversized','allocation-error','new-partial','new-held','new-cleared','existing-partial','existing-held','maximum-header','existing-exact']}
    return [dict(case=c,mode=mode)for c in cases[name]for mode in ['thumb','arm']]


def setup(f,ordinal):
    p=Plan({CTX:2176,OTHER:2176,OUT:4,SOCKET:72,INPUT:0x4900,RECORD:0x4900,ALLOCATE:4,RELEASE:4},ordinal);m=p.memory;m.set(SOCKET+12,CTX);m.set(SOCKET+68,9);m.set(CTX+2084,RECORD);m.set(CTX+2088,10);m.set(CTX+2092,2);m.set(CTX+1110,0,1);m.set(CTX+1109,3,1)
    for slot,kind in [(ALLOCATE,'allocate'),(RELEASE,'release')]:m.set(slot,TARGETS[(kind,f['mode'])]|int(f['mode']=='thumb')^int(bool(f.get('badTag'))))
    p.writable=[(CTX+2084,12),(CTX+1110,1),(CTX+1109,1),(OUT,4)]
    return p


def callback(p,name,f,kind,args,returned=None,mutations=()):
    p.call(TARGETS[(kind,f['mode'])],args,returned,mutations);p.actions[-1]['site']=CONTRACTS[name]['call']


def finish(p,initial,args,f):
    value=p.finish(initial,args);value['indirectProviders']={TARGETS[(kind,f['mode'])]:dict(mode=f['mode'],kind='function',program='',processor='arm9',module='main',fixtureProvider=True,interface='void*(u32)'if kind=='allocate'else 'void(void*)')for kind in ['allocate','release']};return value


def consume(f,ordinal):
    p=setup(f,ordinal);m=p.memory;case=f['case'];count={'partial':3,'exact':8,'larger':0xffffffff,'null-exact':8,'wrap-partial':2,'zero-remaining':0}[case]
    if case=='null-exact':m.set(CTX+2084,0)
    if case=='wrap-partial':m.set(CTX+2088,1);m.set(CTX+2092,0xfffffffe)
    if case=='zero-remaining':m.set(CTX+2088,2)
    initial=m.snapshot();left=(m.get(CTX+2088)-m.get(CTX+2092))&0xffffffff
    if count>=left:
        if m.get(CTX+2084):callback(p,'020928f8',f,'release',[m.get(CTX+2084)],mutations=[(CTX+2084,(RECORD+32).to_bytes(4,'little'))])
        m.set(CTX+2084,0)
    else:m.set(CTX+2092,m.get(CTX+2092)+count)
    return finish(p,initial,[count,SOCKET,0x55667788,0x99aabbcc],f)


def read(f,ordinal):
    p=setup(f,ordinal);m=p.memory;case=f['case'];m.set(CTX+1110,128 if case=='held'else 0,1)
    if case.startswith('empty'):m.set(CTX+2084,0)
    initial=m.snapshot()
    if m.get(CTX+2084)and not m.get(CTX+1110,1):
        p.call(0x2091f54,[RECORD+2,8,SOCKET],0xffffffff if case=='read-error'else 0)
        if case=='read-error':
            callback(p,'02092854',f,'release',[RECORD]);m.set(CTX+2084,0);m.set(OUT,0);p.result=0;return finish(p,initial,[OUT,SOCKET,0x55667788,0x99aabbcc],f)
        held=case=='parse-held';p.call(0x2091fbc,[CTX,RECORD],mutations=[(CTX+1110,bytes([128 if held else 0]))])
        if not held:m.set(CTX+2084,0)
    if not m.get(CTX+2084):
        error=case.endswith('error');p.call(0x2092174,[SOCKET],9 if error else 0)
        if error:m.set(OUT,0);p.result=0;return finish(p,initial,[OUT,SOCKET,0x55667788,0x99aabbcc],f)
        p.call(0x2092174,[SOCKET],8,[(CTX+2084,(RECORD+16).to_bytes(4,'little')),(CTX+2088,(25).to_bytes(4,'little')),(CTX+2092,(7).to_bytes(4,'little'))])
    m.set(OUT,(m.get(CTX+2088)-m.get(CTX+2092))&0xffffffff);p.result=(m.get(CTX+2084)+m.get(CTX+2092))&0xffffffff
    return finish(p,initial,[OUT,SOCKET,0x55667788,0x99aabbcc],f)


def receive(f,ordinal):
    p=setup(f,ordinal);m=p.memory;case=f['case'];new=not case.startswith('existing')and case!='no-input';m.set(CTX+2084,0 if new else RECORD)
    if case=='short-header':m.set(SOCKET+68,4)
    if case=='no-input':m.set(SOCKET+68,0)
    size=0x4801 if case=='oversized'else 0x4800 if case=='maximum-header'else 7;header=bytes([23,3,0,size>>8,size&255]);m.put(INPUT,header);initial=m.snapshot();amount_pointer=SP-24
    if not m.get(CTX+2084):
        if m.get(SOCKET+68)<5:return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],f)
        p.call(0x208d9a0,[amount_pointer,SOCKET],INPUT);p.actions[-1]['mutations']=[(amount_pointer,(m.get(SOCKET+68)).to_bytes(4,'little'))];amount=size+5
        if amount>0x4805:m.set(CTX+1109,9,1);return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],f)
        failed=case=='allocation-error';callback(p,'02092938',f,'allocate',[amount],0 if failed else RECORD);m.set(CTX+2084,0 if failed else RECORD)
        if failed:m.set(CTX+1109,9,1);return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],f)
        m.set(CTX+2088,amount);m.set(CTX+2092,0);m.set(CTX+1110,0,1)
    elif not m.get(SOCKET+68):return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],f)
    partial=case in ['new-partial','existing-partial','maximum-header'];available=3 if partial else 8 if case=='existing-exact'else 29;p.call(0x208d9a0,[amount_pointer,SOCKET],INPUT);p.actions[-1]['mutations']=[(amount_pointer,available.to_bytes(4,'little'))];left=(m.get(CTX+2088)-m.get(CTX+2092))&0xffffffff;complete=available>=left;amount=min(available,left);destination=m.get(CTX+2084)+m.get(CTX+2092);p.call(0x2008e0c,[INPUT,destination,amount],mutations=[(destination,m.read(INPUT,amount))]);p.call(0x208da30,[amount,SOCKET])
    if complete:
        held=case in ['new-held','existing-held'];p.call(0x2091fbc,[CTX,m.get(CTX+2084)],mutations=[(CTX+1110,bytes([128 if held else 0]))])
        if not held:m.set(CTX+2084,0)
    else:m.set(CTX+2092,m.get(CTX+2092)+amount)
    return finish(p,initial,[SOCKET,0x11223344,0x55667788,0x99aabbcc],f)


def scenario(name,f,ordinal):return {'02092854':read,'020928f8':consume,'02092938':receive}[name](f,ordinal)
