import math
import struct
import ov001_rows595_machine_20261101 as M


def f32(value):return struct.unpack('<f',struct.pack('<f',value))[0]
def signed(value):return(value&0xFFFFFFFF)-0x100000000 if value&0x80000000 else value&0xFFFFFFFF
def trunc_div(a,b):return(abs(a)//abs(b))*(-1 if(a<0)!=(b<0)else 1)


def profiles():
    rows=[]
    for kind in[0,1,2]:
        for seed in[0,1,0x80000000,0xFFFFFFFF]:
            for present,count in[(False,0),(True,0),(True,1),(True,4)]:
                for modifier in[0,40,140,0x80000000]:
                    n=len(rows);first=((((seed*0x41C64E6D+0x3039)&0xFFFFFFFF)>>16)%255)+1;rows.append(dict(name=f'row-{n:03d}',kind=kind,seed=seed,present=present,fileCount=count,modifier=modifier,row=n%3,identity=0xABC00000|n,firstId=first if n%2 else 0,restricted=n%3==0,payload=[0,1,127,255,63,128,13,254],species=[-1,1,32767][n%3],variant=[0,1,255][n%3]))
    return rows


def model(r):
    p=r['profile'];expected=bytearray(r['before']);base=M.ROWS+p['row']*132;wanted=p['kind']+3;ids=[p['firstId']];seed=p['seed'];draws=[];events=[dict(entry=M.LOOKUP,preparedWords=[p['identity']],providedR0=M.RECORD),dict(entry=M.KIND,preparedWords=[p['identity']],providedR0=p['kind'])]
    for attempt in range(4096):
        if len(ids)==wanted:break
        seed=(seed*0x41C64E6D+0x3039)&0xFFFFFFFF;candidate=((seed>>16)%255)+1;draws.append(dict(state=seed,candidate=candidate));allowed=not p['restricted']or candidate%4!=0;events.append(dict(entry=M.PREDICATE,preparedWords=[candidate],providedR0=1 if allowed else 0))
        if allowed and candidate not in ids:ids.append(candidate)
    else:raise ValueError('595 unsupported insufficient candidate pool')
    events.append(dict(entry=M.OPEN,preparedWords=[M.PATH,1],providedR0=M.PAYLOAD if p['present']else 0));points=wanted*50
    if p['present']:
        ratio=f32(wanted/5.0)
        for value in p['payload'][:p['fileCount']]:points=((points+math.ceil(f32(float(value)*ratio))+32768)&65535)-32768
        events.append(dict(entry=M.CLOSE,preparedWords=[1,M.PAYLOAD],providedR0=0xE5950001))
    if p['modifier']>=40:
        factor=trunc_div(signed(p['modifier']-40),100)+1;scaled=(points*factor)&65535;points=min(scaled,999)
    quotient=trunc_div(points,wanted);remainder=points-quotient*wanted;allocation=min(quotient&65535,100);values=[allocation]*len(ids)
    if not 0<=remainder<=len(ids):raise ValueError('595 unsupported remainder store extent')
    for index in range(remainder):values[index]=(values[index]+1)&255
    for index,(ident,value)in enumerate(zip(ids,values)):expected[base-M.BASE+0x7A+2*index]=ident;expected[base-M.BASE+0x7B+2*index]=value
    struct.pack_into('<h',expected,base-M.BASE+0x3C,points);struct.pack_into('<I',expected,M.RNGSTATE-M.BASE,seed);events.append(dict(entry=M.SINK,preparedWords=[p['species']&0xFFFFFFFF,p['variant'],base+0x7A,M.OUTPUT+p['row']*64],providedR0=0xD5950001));stack=M.STACK-M.BASE
    if r['providedCalls']!=events:raise ValueError(('595 independent prepared/provided calls differ',p['name']))
    actualDraws=[ret for ret in r['nativeReturns']if ret['entry']==M.RNG]
    if len(actualDraws)!=len(draws)or any(ret['inputWords'][0]!=255 or ret['returnedWords'][0]!=draw['candidate']-1 for ret,draw in zip(actualDraws,draws)):raise ValueError('595 actual RNG return sequence differs')
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError(('595 independent full RAM differs',p['name'],ids,points,values))
    if r['returnedWords'][0]!=0xD5950001:raise ValueError('595 independent forwarded physical R0 differs')
    return dict(ids=ids,values=values,points=points,finalRngState=seed,actualRngDraws=len(draws),sourceDomain='Synthetic category0..2,row0..2,fileCount0..4,sufficient supplied candidate pool',sceneReachability=False)
