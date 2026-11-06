import struct
import overlay_builder590_machine_20261101 as M
from main_builder584_models_20261101 import signed_byte


def signed(value):return(value&0xFFFFFFFF)-0x100000000 if value&0x80000000 else value&0xFFFFFFFF


def profiles():
    rows=[]
    for count in[0,1,2,7,127]:
        for mode in[0,1,2,0x80000000]:
            for total in[0,17,0xFFFFFFFF,0x80000000]:
                n=len(rows);rows.append(dict(name=f'builder-{n:03d}',args=[0x123400FE,0x567800FF,[0,12,13,0xABCDFFFF][n%4],0xDEAD00FF,0xF00D0000|count,0xABCD0080,mode,total],bank=n%2,counter=0xFFFFFFF0,occupiedIndices=[4,5,14]if n%3==0 else[]))
    return rows


def model(r):
    p=r['profile'];x,y,width,height,count,metadata,mode,total=p['args'];count&=255;height&=255;metadata&=255;total=signed(total);unit=r['unit'];expected=bytearray(r['before']);q=(abs(total)//count)*(-1 if total<0 else 1)if count else total;rem=total-q*count if count else 0
    struct.pack_into('<HH',expected,M.DESCRIPTOR-M.BASE+0xC,count,metadata);struct.pack_into('<II',expected,M.DESCRIPTOR-M.BASE,rem&0xFFFFFFFF,(count*q)&0xFFFFFFFF);final=mode if unit['entry']==M.UNITS['ov005']['entry']else 0;struct.pack_into('<I',expected,unit['globalAddress']+unit['globalOffset']-M.BASE,final&0xFFFFFFFF)
    views=[[1,4,127,12,x,y,(width+2)&255,(height+2)&255,1,0]];baseX=(x+1)&255;currentY=(y+1)&255
    for index in range(count):
        if unit['entry']==M.UNITS['ov005']['entry']and mode==1:views.extend([[1,signed_byte(index+5),127,7,baseX,currentY,(width-13)&255,2,1,1],[1,signed_byte(index+14),127,8,(baseX+width-13)&255,currentY,13,2,1,1]])
        else:views.append([1,signed_byte(index+5),127,0,baseX,currentY,width,2,1,1])
        currentY=(currentY+2)&255
    counter=p['counter'];mainCalls=[];lower=[]
    for words in views:
        words=[value&0xFFFFFFFF for value in words];index=signed(words[1]);address=M.slot(index,p['bank']);occupied=struct.unpack_from('<I',r['before'],address-M.BASE)[0];mainCalls.append(dict(preparedWords=words,returnedR0=0 if occupied else 1))
        if not occupied:
            args=[address,words[0],words[2],words[3]]+[value&255 for value in words[4:8]]+[counter,signed_byte(words[8]),words[9]];lower.append(dict(entry=M.M.LOWER,preparedWords=[value&0xFFFFFFFF for value in args]))
            if words[9]:counter=(counter+(words[6]&255)*(words[7]&255))&0xFFFFFFFF
    struct.pack_into('<I',expected,M.M.COUNTER-M.BASE,counter);stack=M.STACK-M.BASE
    if r['after'][:stack-65536]!=expected[:stack-65536]or r['after'][stack+4096:]!=expected[stack+4096:]:raise ValueError(('590 independent full RAM differs',p['name']))
    if r['mainCalls']!=mainCalls:raise ValueError(('590 ten-word source-to-main calls differ',p['name']))
    if r['providedCalls']!=lower:raise ValueError(('590 eleven-word lower boundary differs',p['name']))
    divides=[ret for ret in r['nativeReturns']if ret['entry']==M.DIV]
    if len(divides)!=2 or any(ret['inputWords'][:2]!=[total&0xFFFFFFFF,count]or ret['returnedWords'][:2]!=[q&0xFFFFFFFF,rem&0xFFFFFFFF]for ret in divides):raise ValueError('590 native divide pair differs')
    return dict(mainCallCount=len(mainCalls),lowerProvidedCount=len(lower),finalCounter=counter,descriptorWords=[rem&0xFFFFFFFF,(count*q)&0xFFFFFFFF],globalWord=final&0xFFFFFFFF,abstractCDefinedDivisionDomain=count!=0,sourceMeaningIsVoidView=True)
