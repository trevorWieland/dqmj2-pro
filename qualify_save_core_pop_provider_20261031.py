import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn import arm_const as R
import save_core_historical_link_20261031 as B
from save_core_selection_transition_fixtures_20261031 import sha,sidecar
from match_mechanics_save_20261029_record33 import verify_inputs
ENTRY=0x0206DB90
STOP=0x027FF800


def main():
    verify_inputs();arm=B.measured_module('main')[1];offset=ENTRY-0x02000000;native=arm[offset:offset+76];assert native[:16]==bytes.fromhex('7f0050e30030a0e37f00a0031eff2f01');table=int.from_bytes(native[72:76],'little');assert 0x02000000<=table and table+63<=0x02000000+len(arm);original=arm[table-0x02000000:table-0x02000000+63];contexts=[('measured_initialized_bytes',original),('synthetic_identity',b''.join(bytes((i,0xA5,0x5A)) for i in range(21))),('synthetic_negative',b''.join(bytes((128+i,0xA5,0x5A)) for i in range(21))),('synthetic_duplicate',bytes((255,0xA5,0x5A))*21)];vectors=[]
    words=[(v if v<128 else v-256)&0xFFFFFFFF for v in range(256)]+[0x17F,0x80000000,0x7FFFFFFF]
    for name,data in contexts:
        for word in words:
            for seed in (0,0xFFFFFFFF):
                u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.reg_write(R.UC_ARM_REG_CPSR,0x1F);u.mem_map(0x02000000,0x800000);u.mem_write(0x02000000,arm);u.mem_write(table,data);u.reg_write(R.UC_ARM_REG_SP,0x027FE000);u.reg_write(R.UC_ARM_REG_LR,STOP);u.reg_write(R.UC_ARM_REG_R0,word);saved={}
                for i in range(1,13):
                    reg=getattr(R,'UC_ARM_REG_R'+str(i));value=(seed+i*0x1234567)&0xFFFFFFFF;u.reg_write(reg,value)
                    if 4<=i<=11:saved[reg]=value
                reads=[];seen=set();returned=[]
                def code(machine,pc,size,user):
                    if pc==STOP:returned.append(True);machine.emu_stop();return
                    assert ENTRY<=pc and pc+size<=ENTRY+72;seen.add(pc-ENTRY)
                def read(machine,access,address,size,value,user):
                    if ENTRY<=address and address+size<=ENTRY+76:return
                    assert table<=address and address+size<=table+63 and size==1 and (address-table)%3==0;reads.append((address-table)//3)
                def write(*args):raise AssertionError('Unexpected native write')
                u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_READ,read);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(ENTRY,STOP+4,count=1000);assert returned and u.reg_read(R.UC_ARM_REG_SP)==0x027FE000 and all(u.reg_read(reg)==value for reg,value in saved.items());expected=127;expected_reads=[]
                if word!=127:
                    expected=0
                    for i in range(21):
                        expected_reads.append(i);value=data[3*i];value=value if value<128 else value-256
                        if word==value&0xFFFFFFFF:expected=i;break
                actual=u.reg_read(R.UC_ARM_REG_R0);assert actual==expected and reads==expected_reads and (actual==127)==(word==127);vectors.append(dict(context=name,incomingR0=word,seed=seed,actualReturn=True,returnWord=actual,tableReadIndices=reads,ownInstructionOffsets=sorted(seen)))
    vector=sidecar(vectors,'evidence/vectors/save-core-pop-provider-qualification-20261031.json.gz');reports=[]
    for report in ['evidence/application/save-core-live-count-loops-source-20261031.json','evidence/application/save-core-pop-index-abi-source-20261031.json']:
        path=ROOT/report
        if path.exists():
            r=json.loads(path.read_text());import gzip;cases=json.loads(gzip.decompress((ROOT/r['vectorSidecar']['path']).read_bytes()));unreachable=sum(any(e['entry']==ENTRY and ((e['arguments'][0]==127 and e['returnWord']!=127) or (e['arguments'][0]!=127 and not 0<=e['returnWord']<=20)) for e in c['providers']) for c in cases);reports.append(dict(report=report,nativeCaseDigest=r['nativeCaseDigest'],cases=len(cases),casesWithSuppliedOutcomeOutsideOriginalRange=unreachable,classification='Deliberate supplied caller-contract tests;not a claim of original-callee or scene reachability'))
    out=dict(schemaVersion=1,sourceCredit=0,newFunctions=0,newBytes=0,module='main',processor='arm9',mode='arm',address=hex(ENTRY),nativeBytes=76,nativeSpanSha256=sha(native),initializedTable=dict(address=hex(table),bytes=63,sha256=sha(original)),actualNativeReturns=len(vectors),providers=0,ownInstructionAddresses=len(set.union(*(set(v['ownInstructionOffsets']) for v in vectors))),vectorSidecar=vector,nativeCaseDigest=vector['uncompressedSha256'],callerContractQualifications=reports,generatorSha256=sha(Path(__file__).read_bytes()),limitations=['Actual original76-byte leaf executes with measured initialized table bytes and three explicit synthetic table contexts;no function providers or memory writes occur. All256 signed-byte words plus three high fullwords and two independent register seeds are tested. No table lifecycle/field meaning is inferred.','Native output is127 exactly for full incoming word127;all other observed outputs and the bounded21-entry search are0..20. The caller matrices deliberately supply broader0/127 outcomes. Their impossible combinations are robustness contracts only and never establish physical scene reachability or original lower behavior. Earlier files are preserved unchanged.'])
    target=ROOT/'evidence/verification/save-core-pop-provider-qualification-20261031.json';target.write_text(json.dumps(out,indent=2)+'\n');verify_inputs();print(dict(actualReturns=len(vectors),providers=0,qualifications=reports,sha256=sha(target.read_bytes())))


if __name__=='__main__':main()
