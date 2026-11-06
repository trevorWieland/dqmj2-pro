import struct
import ov005_copy568_machine_20261101 as M


def signed(value):return value if value<0x80000000 else value-0x100000000


def copy_return(before,source,destination,length):
    initialSource,initialDestination,initialLength=source,destination,length
    if not length:return source
    if destination&1:
        source+=1;destination+=1;length-=1
        if not length:return source
    if(source^destination)&1:return((source&~1)+2*(length//2+1))&0xFFFFFFFF
    if length&1:return before[initialSource-M.BASE+initialLength-1]|before[initialDestination-M.BASE+initialLength]<<8
    return(source+length)&0xFFFFFFFF


def profiles():
    rows=[]
    for stride in[1,2,3,4,5,7,8,16]:
        for count in[1,3]:
            for total in[count*stride,count*stride-1]:
                for index in sorted(set([0,count-1])):
                    for sourceAlign in range(4):
                        for destAlign in[0,2]:rows.append(dict(stride=stride,rows=count,total=total,index=index,sourceAlign=sourceAlign,destAlign=destAlign))
    for index in[0xFFFF,0xFFFE,0xFFFD]:
        for sourceAlign in range(4):
            for destAlign in[0,2]:rows.append(dict(stride=7,rows=3,total=17,index=index,sourceAlign=sourceAlign,destAlign=destAlign))
    for index in[0xFFFFFFFF,0xFFFFFFFE,0xFFFFFFFD,0x10000,0x10001,0x80000000,0x7FFFFFFF]:
        for sourceAlign in[0,1]:
            for destAlign in[0,2]:rows.append(dict(stride=0,rows=3,total=7,index=index,sourceAlign=sourceAlign,destAlign=destAlign))
    for index in[0xFFFFFFFF,0xFFFFFFFE,0xFFFFFFFD]:
        for sourceAlign in range(4):
            for destAlign in[0,2]:rows.append(dict(stride=1,rows=3,total=3,index=index,sourceAlign=sourceAlign,destAlign=destAlign))
    for stride in[1,3,8]:
        for index in[0,2]:
            for destAlign in[0,2]:rows.append(dict(stride=stride,rows=3,total=3*stride-1,index=index,destAlign=destAlign,alias=True))
    for total in[0,1,7,65535]:rows.append(dict(stride=0,rows=1,total=total,index=0))
    for index in[0xFFFF,0xFFFE,0xFFFD]:
        for flags in[dict(nullData=True),dict(nullContext=True),dict(nullData=True,nullContext=True)]:rows.append(dict(stride=3,rows=3,total=7,index=index,**flags))
    rows.extend([dict(stride=3,rows=0,total=0,index=0),dict(stride=2,rows=1,total=2,index=3)])
    return[dict(p,name=f'copy-{i:04d}')for i,p in enumerate(rows)]


def model(r):
    p=r['profile'];before=r['before'];expected=bytearray(before);source,destination=r['source'],r['target'];calls=[];defined=True
    if r['direct']:length=p['length'];returned=copy_return(before,source,destination,length)
    else:
        index=p['index']&0xFFFFFFFF;struct.pack_into('<H',expected,destination-M.BASE+2,index&65535)
        if index in[0xFFFF,0xFFFE,0xFFFD]:length=0;returned=M.NODE2 if index==0xFFFF else index
        else:
            stride=p['stride']&65535;count=p['rows']&0xFFFFFFFF;total=signed(p['total']&0xFFFFFFFF);source=(source+index*stride)&0xFFFFFFFF;destination+=4;length=stride
            if index==(count-1)&0xFFFFFFFF:
                quotient=(abs(total)//stride)*(-1 if total<0 else 1)if stride else total;remainder=total-quotient*stride if stride else 0;calls.append((M.DIV,[total&0xFFFFFFFF,stride],[quotient&0xFFFFFFFF,remainder&0xFFFFFFFF]));defined=stride!=0
                if remainder:length=remainder
            if not 0<=length<=65535:raise ValueError('568 unsupported negative/excess copy extent')
            returned=copy_return(expected,source,destination,length);calls.append((M.COPY,[source,destination,length],[returned]))
    if not M.BASE<=source<=M.BASE+0x800000-length:raise ValueError('568 unsupported source extent')
    expected[destination-M.BASE:destination-M.BASE+length]=expected[source-M.BASE:source-M.BASE+length];stack=M.STACK-M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError(('568 independent full RAM differs',p['name']))
    if r['returnedWords'][0]!=returned:raise ValueError(('568 independent physical R0 differs',p['name'],r['returnedWords'][0],returned))
    if not r['direct']:
        if len(r['nativeReturns'])!=len(calls):raise ValueError('568 native call count differs')
        for actual,(entry,arguments,results)in zip(r['nativeReturns'],calls):
            if actual['entry']!=entry or actual['inputWords'][:len(arguments)]!=arguments or actual['returnedWords'][:len(results)]!=results:raise ValueError(('568 native call contract differs',p['name']))
    return dict(returnedR0=returned,length=length,copySource=source,copyDestination=destination,nativeContracts=calls,abstractCDefinedRemainderDomain=defined)
