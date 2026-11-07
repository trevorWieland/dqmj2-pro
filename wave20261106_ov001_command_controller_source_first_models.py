from project import ROOT,read_json
from wave20261106_arm7_wl_followon_source_receive_fixture import Plan,SP,STOP,CTX,REQ,CFM,OUT,GAME,p16,p32
FIELD=0x02239c10
ARRAY=0x02239c64
STATE=0x0223df3c
SLOTS=0x0223df44
SWITCH=0x0223e054
ITEM=0x02720000
FLAGS=0x02721000
LINK2=0x02722000
RESOURCE2=0x02723000
TABLE=0x020dbc18
BANK=0x02102a18


def word(value):return value&0xffffffff

def signed(value,bits):return value-(1<<bits)if value&(1<<(bits-1))else value


def fixtures():
    result=[]
    for i in range(12):
        result.append(dict(entry=0x021fe4ac,index=i%4,a=word(0x81234567+i),b=word(0xdeadbeef-i),c=[0,1,128,255][i%4],d=(i*31)&255,e=(i*43)&255,f=(i*67)&255,g=[-128,-1,0,127][i%4],h=i%3,counter=[0,31,0x80000000,0x7fffffff][i%4],mutate=i%2))
        result.append(dict(entry=0x0220aba0,index=i%6,a=word(0x81234567+i),b=word(0xdeadbeef-i),c=[0,1,128,255][i%4],d=(i*31)&255,e=(i*43)&255,f=(i*67)&255,g=[-128,-1,0,127][i%4],h=i%3,counter=[0,31,0x80000000,0xffffffff][i%4],count=i%4,replace=i%2))
        result.append(dict(entry=0x021fe618,group=i%4,index=i%6,a=word(0x81234567+i),b=word(0xdeadbeef-i),chars=[(i*17+j*41)&255 for j in range(6)],counter=[0,31,0x80000000,0x7fffffff][i%4],added=[0,1,31,0xffffffff][i%4],mutate=i%2))
        result.append(dict(entry=0x0220afe4,owner=[-128,-1,0,127][i%4],updatedOwner=[127,0,-1,-128][i%4],value=word(0xaabbcc00+i),itemId=[-32768,-1,0,32767][i%4],updatedItemId=[32767,0,-1,-32768][i%4],bits=[0,0xffff,0xabcd,0x00f0][i%4]))
    result.extend(dict(entry=0x0220b3e4,mode=mode,a=0x81234567,b=0xffffffff,c=0xa5a55a5a,flags=flags)for mode in[0,1,2,3,4,0xffffffff,0x80000000]for flags in[0,0xffffffff])
    result.extend(dict(entry=0x0220ac9c,index=i%4,code=code,position=position,style=[0,1,128,255][i%4],flag=[-128,-1,0,127][i%4])for i,code in enumerate([0,1,13,100,65535])for position in[-32768,-1,0,32767])
    return result


def scenario(f,ordinal):
    entry=f['entry'];recordAddress=BANK+12*f.get('index',0);frame={0x021fe4ac:48,0x021fe618:56,0x0220aba0:48,0x0220ac9c:40,0x0220afe4:64,0x0220b3e4:0}[entry];p=Plan(ordinal,frame);tableReads=[];flagReads=[]
    p.buffer(FIELD,100,0x5a);p.buffer(STATE,8,0x77);p.buffer(SLOTS,16,0x88);p.buffer(SWITCH,52,0x99);p.buffer(ITEM,32,0x45);p.buffer(FLAGS,8,0xab);p.buffer(LINK2,8,0x4d);p.buffer(RESOURCE2,80,0x2b);p.allowed.extend([(OUT+24,OUT+28),(RESOURCE2+24,RESOURCE2+28),(FIELD,FIELD+92),(ARRAY,ARRAY+16),(STATE,STATE+8),(SLOTS,SLOTS+16),(SWITCH,SWITCH+52)]);p.buffer(BANK,72,0x3c);p.u32(recordAddress,CFM);p.u32(CFM+4,OUT);p.u32(LINK2+4,RESOURCE2)
    if entry in[0x021fe4ac,0x0220aba0]:
        p.args=[word(f['index']),f['a'],f['b'],f['c'],f['d'],f['e'],f['f'],word(f['g']),f['h']]
        if entry==0x021fe4ac:p.u32(FIELD+88,f['counter'])
        else:p.u32(STATE+4,f['counter']);p.write(STATE,bytes([f['count']]))
    elif entry==0x021fe618:p.args=[f['group'],f['index'],f['a'],f['b'],*f['chars']];p.u32(ARRAY+4*f['group'],f['counter'])
    elif entry==0x0220b3e4:p.args=[f['mode'],f['a'],f['b'],f['c']];p.u32(SWITCH,f['flags'])
    elif entry==0x0220ac9c:p.args=[f['index'],GAME,f['code'],word(f['position']),f['style'],word(f['flag'])];p.buffer(SP-32,8,0xa5)
    else:p.args=[CTX,f['value']];p.write(CTX+16,bytes([f['owner']&255]));p.u16(ITEM+24,f['itemId']&65535);p.u16(FLAGS+4,f['bits']);p.buffer(SP-44,32,0xa5)
    p.capture()
    if entry in[0x021fe4ac,0x0220aba0]:
        p.action(0x02049ad0,[word(f['index'])],recordAddress);counter=f['counter'];old=signed(counter,32)>>5 if entry==0x021fe4ac else counter;changes=[]
        if entry==0x021fe4ac and f['mutate']:counter^=0xa55a5aa5;changes.append((FIELD+88,p32(counter)));p.u32(FIELD+88,counter)
        elif entry==0x0220aba0 and f['replace']:changes.extend([(recordAddress,p32(LINK2)),(STATE+4,p32(counter^0xa55a5aa5)),(STATE,bytes([5]))]);p.u32(recordAddress,LINK2);counter^=0xa55a5aa5;p.u32(STATE+4,counter);p.write(STATE,bytes([5]))
        p.action(0x02049be4,[recordAddress,1,f['a'],f['b'],f['c'],f['d'],f['e'],f['f'],word(old),word(f['g']),f['h']],ordinal%2,mutations=changes)
        if entry==0x021fe4ac:
            if f['h']:p.u32(FIELD+88,word(counter+((f['e']*f['f'])<<5)))
            p.returned=recordAddress
        else:
            resource=RESOURCE2 if f['replace']else OUT;p.u32(resource+24,p.r32(resource+24)|2);p.u32(STATE+4,word(counter+f['e']*f['f']));count=p.read(STATE,1)[0];p.write(STATE,bytes([(count+1)&255]));p.write(SLOTS+count,bytes([f['index']&255]))
    elif entry==0x021fe618:
        p.action(0x02049ad0,[f['index']],recordAddress);a,b,c,d,e,h=f['chars'];counter=f['counter'];args=[f['index'],f['a'],8,f['b'],a,b,word(signed(counter,32)>>5),c,d,e,0,h];changes=[]
        if f['mutate']:counter^=0xa55a5aa5;changes=[(ARRAY+4*f['group'],p32(counter))]
        p.action(0x02068f70,args,f['added'],mutations=changes);p.u32(ARRAY+4*f['group'],word(counter+(f['added']<<5)));p.returned=recordAddress
    elif entry==0x0220b3e4:
        if f['mode']<4:
            offset=[4,28,16,40][f['mode']]
            for at,value in enumerate([f['a'],f['b'],f['c']]):p.u32(SWITCH+offset+4*at,value)
            p.u32(SWITCH,f['flags']|(1 if f['mode']in[0,2]else 2))
    elif entry==0x0220ac9c:
        local=SP-32;p.action(0x02049ad0,[f['index']],recordAddress);p.action(0x02049ffc,[OUT]);p.action(0x02008be0,[0,local,8],mutations=[(local,bytes(8))]);p.write(local,bytes(8))
        value=0x3000
        if f['code']:
            at=TABLE+2*(((f['code']+13)&65535)+0x17b);inputs=read_json(ROOT/'evidence/lanes/parallel-wave20261106/ov001-command-controller-next/first/native-inputs.json');raw=(ROOT/inputs['mainImage']['path']).read_bytes();value=int.from_bytes(raw[at-0x02000000:at-0x02000000+2],'little');tableReads=[(at,2,value)]
        p.u16(local,value);p.action(0x02087a48,[OUT,0,word(f['position']),f['style'],1,local],checks=[(local,p.read(local,8))]);p.action(0x02087a48,[OUT,0,word(signed((f['position']+8)&65535,16)),f['style'],word(f['flag']),GAME],checks=[(GAME,p.read(GAME,32))]);before=p.r32(OUT+12);p.action(0x02086b14,[OUT,0],OUT,mutations=[(OUT+16,p32(before)),(OUT+12,p32(0))]);p.u32(OUT+16,before);p.u32(OUT+12,0)
    else:
        local=SP-44;owner=word(f['owner']);p.action(0x0220aba0,[6,owner,2,1,3,16,2,0,1]);p.action(0x0220ac58,[6,5,4,1,16],mutations=[(CTX+16,bytes([f['updatedOwner']&255]))]);p.write(CTX+16,bytes([f['updatedOwner']&255]));p.action(0x0220aba0,[7,word(f['updatedOwner']),2,1,5,16,2,0,1]);p.action(0x02062a10,[f['value']],ITEM);text=b''.join(p16((0x3040+i*23+ordinal)&65535)for i in range(16));p.action(0x02046af4,[0x021c9698,ITEM,13,16,local,255],mutations=[(local,text),(ITEM+24,p16(f['updatedItemId']&65535))]);p.write(local,text);p.u16(ITEM+24,f['updatedItemId']&65535);p.action(0x02062a10,[f['value']],ITEM);p.action(0x020449d4,[word(f['updatedItemId'])],FLAGS);flagReads=[(FLAGS+4,2,f['bits'])];p.action(0x0220ac9c,[7,local,(f['bits']>>4)&15,16,0,1],checks=[(local,text)])
    result=p.finish();result.update(sramReads=[],sramWrites=[],sramFault='none',expectedMmioReads=[],faultRegisters=[],spiReadScript=[],instructionBudget=10000,expectedTableReads=tableReads,expectedFlagReads=flagReads);return result
