import struct
import main_builder584_machine_20261101 as M


def signed_byte(value):return((value+128)&255)-128


def profiles():
    rows=[];values=[0,1,127,128,255,256,0xFFFF,0x80000080,0xFFFFFFFF]
    for mode in[0,1,255]:
        for index in[-128,-92,-36,-1,0,1,35,36,91,92,127,128]:
            for occupied in[0,1,256,0x80000000,0xFFFFFFFF]:
                for flag in[0,1,0x80000000]:
                    n=len(rows);args=[0xA0000000|n,index,0x12340000|n,0xF0000000|n]+[values[(n+i*2)%len(values)]for i in range(5)]+[flag];rows.append(dict(name=f'constructor-{n:04d}',mode=mode,occupied=occupied,counter=[0,17,0xFFFFFFFF,0xFFFFFF00][n%4],args=args))
    for field in range(4,9):
        for value in range(256):
            args=[1,4,127,12,0xA0A00102,0xB0B00304,0xC0C00506,0xD0D00708,0xE0E0090A,1];args[field]=(0xFF800000|value);rows.append(dict(name=f'byte-field-{field}-{value}',mode=1,occupied=0,counter=0xFFFFFF00,args=args))
    return rows


def model(r):
    p=r['profile'];args=p['args'];expected=bytearray(r['before']);index=args[1]if p['mode']else signed_byte(args[1]+36);slot=(M.SLOTS+12*index)&0xFFFFFFFF;calls=[];native=[M.GETTER];returned=0
    if not p['occupied']:
        words=[slot,args[0],args[2],args[3]]+[a&255 for a in args[4:8]]+[p['counter'],signed_byte(args[8]),args[9]];words=[a&0xFFFFFFFF for a in words];calls=[dict(entry=M.LOWER,preparedWords=words,providedR0=0xE5840001)];native.append(M.RESOURCE);returned=1
        if args[9]:
            native.append(M.INCREMENT);value=(p['counter']+(args[6]&255)*(args[7]&255))&0xFFFFFFFF;struct.pack_into('<I',expected,M.COUNTER-M.BASE,value)
    if r['providedCalls']!=calls:raise ValueError(('584 eleven-word lower contract differs',p['name']))
    if[ret['entry']for ret in r['nativeReturns']]!=native:raise ValueError('584 actual native return chain differs')
    if r['nativeReturns'][0]['inputWords'][0]!=args[1]&0xFFFFFFFF or r['nativeReturns'][0]['returnedWords'][0]!=slot or r['tailForwardings']!=[index&0xFFFFFFFF]:raise ValueError('584 native index/bank result differs')
    if not p['occupied']and r['nativeReturns'][1]['returnedWords'][0]!=p['counter']:raise ValueError('584 actual initial counter read differs')
    if not p['occupied']and args[9]:
        ret=r['nativeReturns'][-1]
        if ret['inputWords'][0]!=(args[6]&255)*(args[7]&255)or ret['returnedWords'][0]!=struct.unpack_from('<I',expected,M.COUNTER-M.BASE)[0]:raise ValueError('584 actual counter addition differs')
    stack=M.STACK-M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError('584 independent full RAM differs')
    if r['returnedWords'][0]!=returned:raise ValueError('584 independent R0 differs')
    expectedWrites=[]if p['occupied']or not args[9]else[[M.INCREMENT+12,M.COUNTER,4,struct.unpack_from('<I',expected,M.COUNTER-M.BASE)[0]]]
    if r['nonstackWrites']!=expectedWrites:raise ValueError('584 independently ordered counter write differs')
    return dict(returnedR0=returned,slot=slot,lowerWords=calls,actualNativeEntries=native,zeroRamEffectLowerBoundary=True)
