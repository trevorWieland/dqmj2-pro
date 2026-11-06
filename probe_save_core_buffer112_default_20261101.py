import hashlib,itertools,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_buffer112_machine_20261101 as M
from unicorn import UC_HOOK_CODE
PIN='124f9594e3b51ab9f63ddd54b5ca34e88a47938b83fdc81bc06dd356eaa11d6e'
CHECKPOINT=0x20918D4


def main():
    assert hashlib.sha256(Path(M.__file__).read_bytes()).hexdigest()==PIN;arm,inventory,unresolved=M.I.inventory();assert not unresolved;rows=[]
    for kind,slots,r2 in itertools.product((0,1,3,4,5,6,65535),((0,0),(16,16),(20,16),(0xFFFFFFFF,0),(0xA5A5A5A5,0x5A5A5A5A)),(0,1,0xFFFFFFFF,0x80000000)):
        p=dict(seed=1,kind=kind,direction=0,word1=0x12345678,word2=r2);m=M.Machine(arm,inventory,p);local=M.S.STACK-80;m.word(local+8,slots[1]);m.word(local+12,slots[0]);observed=[]
        def checkpoint(u,pc,size,user):
            if pc==CHECKPOINT:observed.append(dict(rawLength=u.reg_read(M.R.UC_ARM_REG_R0),incomingR2Now=u.reg_read(M.R.UC_ARM_REG_R2),slotC=int.from_bytes(u.mem_read(local+12,4),'little'),slot8=int.from_bytes(u.mem_read(local+8,4),'little')));u.emu_stop()
        m.u.hook_add(UC_HOOK_CODE,checkpoint);m.u.emu_start(M.ENTRY|1,M.S.STOP+4,count=64);assert len(observed)==1 and not m.returned;c,b=(16,16) if kind==4 else (20,16) if kind==5 else slots;expectedR2=0 if kind in (4,5) else r2;assert observed[0]==dict(rawLength=((c+b+expectedR2)*2)&0xFFFFFFFF,incomingR2Now=expectedR2,slotC=c,slot8=b);rows.append(dict(kind=kind,preexistingLocalWords=slots,incomingR2=r2,checkpoint=observed[0],actualFunctionReturn=False,sourceLanguageClaim=False,postCheckpointClaim=False))
    asm=ROOT/'asm/_dsd_gap@main_3.s';text=asm.read_text();callers=[]
    for match in re.finditer(r'^\s*bl func_020918a4$',text,re.M):
        prefix=text[:match.start()];decl=list(re.finditer(r'^\s*\.global (func_[0-9a-f]+)$',prefix,re.M))[-1];name=decl[1];end=text.index('func_end '+name,match.end())+len('func_end '+name);start=decl.start();callers.append(dict(caller=name,nearCall=text[max(start,match.start()-900):min(end,match.end()+300)],localKind4Or5GateEstablished=False))
    producer_findings=[dict(entry='0x0209154c',kind='bounded-selector',tableAddress='0x020de830',tableBytes=arm[0xde830:0xde834].hex(),possibleOutputs=[0,4,5],qualification='Static original loop over exactly two measured halfwords;lower membership predicate still to be dynamically qualified'),dict(entry='0x0209158c',kind='row32-writer',source='nonzero result of0209154c'),dict(entry='0x0209161c',kind='row32-writer',source='result of0209154c includingzero'),dict(entry='0x02091490',kind='row32-writer',source='two incoming bytes decoded big-endian and stored without a local4/5 check') ]
    out=dict(schemaVersion=1,upstreamStaticFindings=producer_findings,entry=M.ENTRY,module='main',processor='arm9',mode='thumb',nativeOnly=True,checkpoint=CHECKPOINT,counts=dict(prefixCheckpoints=len(rows),otherKindPrefixes=sum(r['kind'] not in (4,5) for r in rows),supportedKindControls=sum(r['kind'] in (4,5) for r in rows),actualFunctionReturns=0,creditedReturns=0,sourceLanguageCredit=0,sourceBytesCredit=0),cases=rows,directMainCallerAssembly=dict(path=asm.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(asm.read_bytes()).hexdigest(),callSites=callers),frozenMachineSha256=PIN,producerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),limitations=['The original default branch020918B4 skips both local stores. Actual LDRs020918CA/CC then read preexisting local words and ADD020918D0 uses incomingR2. Kind4/5 overwrite both locals andR2. This is measured native prefix dependence,not a decode/boundary uncertainty or observed supported C/native discrepancy.','Stop at020918D4 before the shared length store/derived loops. No actual function return,source-language correctness,post-checkpoint behavior or ordinary caller reachability is claimed for other kinds. Frozen400 source/producer/oracles are untouched.','Three static direct main call sites are identified in callers02091A34 and02092778. Nearby code alone does not establish a complete4/5 precondition;upstream setup/validation and other executable-module callers remain unresolved.']);path=ROOT/'evidence/functional/save-core-buffer112-default-native-20261101.json';path.write_text(json.dumps(out,indent=2)+'\n');print(out['counts']);print([r['caller'] for r in callers]);print(hashlib.sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':main()
