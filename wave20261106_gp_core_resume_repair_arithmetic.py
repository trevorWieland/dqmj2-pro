import hashlib
import json
import re
import struct
from project import ROOT,write_json
from wave20261106_gp_randomchar_interface_repair_probe import native_call
from wave20261106_gp_core_resume_repair_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    row=next(e for e in rows if int(e['address'],0)==0x020aced4);context=(ROOT/row['source']).with_name('context.h').read_text(encoding='utf-8');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text(encoding='utf-8');primary=ROOT/'deps/reference/gamespy-openmohaa-a2f340195975f4f042e28a60b62561dd9a0b2700-gpi-connect/GP/gpiConnect.c';text=primary.read_text(encoding='utf-8');literal=re.search(r'^#define RANDSTRING\s+("[^"\n]+")',text,re.M)[1];alphabet=json.loads(literal).encode()+b'\0'
    if len(alphabet)!=63 or image[0xe0890:0xe0890+63]!=alphabet or 'extern const char native_data_020e0890[63];'not in context or '#define RANDOMCHAR() (RANDSTRING[rand() % (sizeof(RANDSTRING) - 1)])'not in context:raise ValueError('Actual primary complete alphabet/unsigned sizeof contract differs')
    if any(r['symbol']=='_s32_div_f'for r in row['relocations'])or row['nativeSymbolEntries'].get('_u32_div_f',{}).get('address')!='0x2026350':raise ValueError('Positive44 caller requires actual canonical unsigned divider')
    specs=[]
    for a,n in[(0x02026144,524),(0x02026350,484),(0x0201d5d4,52)]:
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        if line is None:raise ValueError('Actual complete canonical arithmetic/RNG entry differs')
        specs.append(dict(address=hex(a),bytes=n,mode='arm',nativeSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    unsigned=[];signed=[];differences=[]
    for n in[0,1,61,62,63,0x7fffffff,0x80000000,0xffffffff]:
        for d in[1,2,3,62,255,0x8000,0x7fffffff,0x80000000,0xffffffff]:
            u=native_call(image,0x02026350,484,n,d)
            if(u['r0'],u['r1'])!=(n//d,n%d):raise ValueError('Unsigned R0 quotient/R1 remainder differs')
            unsigned.append(dict(numerator=hex(n),denominator=hex(d),quotient=u['r0'],remainder=u['r1']));sn=n if n<0x80000000 else n-0x100000000;sd=d if d<0x80000000 else d-0x100000000
            if sn==-0x80000000 and sd==-1:continue
            q=abs(sn)//abs(sd)*(-1 if(sn<0)!=(sd<0)else 1);rem=sn-q*sd;s=native_call(image,0x02026144,524,n,d)
            if(s['r0'],s['r1'])!=(q&0xffffffff,rem&0xffffffff):raise ValueError('Signed R0 quotient/R1 remainder differs')
            signed.append(dict(numerator=sn,denominator=sd,quotient=q,remainder=rem))
            if(u['r0'],u['r1'])!=(s['r0'],s['r1']):differences.append(dict(numerator=hex(n),denominator=hex(d),unsigned=[u['r0'],u['r1']],signed=[s['r0'],s['r1']]))
    state_addr,multiplier,mask=struct.unpack_from('<III',image,0x1d5fc)
    if multiplier!=1103515245 or mask!=0x7fff or image[0x1d5e8:0x1d5f8].hex()!='390080e2030a80e2000082e5200801e0':raise ValueError('Actual LCG increment/mask instruction witness differs')
    seeds=[0,1,0xffffffff,*[1<<i for i in range(32)]];seed=0x73b19da5
    for i in range(128):seed=(seed*1664525+1013904223)&0xffffffff;seeds.append(seed)
    rand=[]
    for seed in seeds:
        expected=(seed*multiplier+12345)&0xffffffff;v=native_call(image,0x0201d5d4,52,0,state=(state_addr,seed))
        if v['state']!=expected or v['r0']!=(expected>>16)&0x7fff:raise ValueError('Actual full rand state/output differs')
        rand.append(dict(seed=hex(seed),nextState=hex(expected),result=v['r0']))
    result=dict(status='passed',actualOriginalHelperReturningCalls=len(unsigned)+len(signed)+len(rand),unsignedDivider=dict(address='0x2026350',bytes=484,quotientRegister='R0',remainderRegister='R1',cases=unsigned),signedDivider=dict(address='0x2026144',bytes=524,quotientRegister='R0',remainderRegister='R1',cases=signed),distinguishingSignedUnsignedCases=differences,nativeRand=dict(address='0x201d5d4',bytes=52,stateAddress=hex(state_addr),multiplier=multiplier,increment=12345,mask='0x7fff',cases=rand,universalOutputDomain=[0,32767],domainProof='Exact final native AND0x7fff proves sign bit zero for every32-bit seed'),canonicalSpecs=specs,primaryAlphabetLiteral=literal,alphabetExtentIncludingNul=63,sourceHelperStorageCredit=0,oldSignedLiteralDefectExplainsNominalCollision=True,limits='Actual helper execution separately verifies full32-bit arithmetic ABI; caller vectors use actual rand result domain. No helper source/storage credit,real game RNG progression,network or Windows/Android execution.')
    write_json(LANE/'arithmetic-abi-proof.json',result);return result
