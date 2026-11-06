import json
import struct
from pathlib import Path
import match_runtime
from match_runtime import REGISTERS
from unicorn import UC_HOOK_CODE
import arm7_sdk306_task_command_context_20261102 as context
import prove_arm7_sdk340_mlme_timeout_callback_scope_20261102 as scope
from project import ROOT,sha256,write_json

def run(main,wram,entry,mode,offset,ms,index):
    cpu,meta=context.setup(main,wram,index,mode=mode,offset=offset,heap=True);base=meta['context'];req=context.base.DATA+0x5200;cpu.mem_write(req,bytes(160));scope.word(cpu,base+0x41c,req);scope.half(cpu,base+0x34c,16);calls=[]
    def hook(machine,pc,width,user):
        if pc==0x027eaaf8:calls.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:2]]))
    token=cpu.hook_add(UC_HOOK_CODE,hook);result=None;error=None;parent=False
    try:
        if entry['task']==0:
            scope.half(cpu,base+0x404,0x12);scope.half(cpu,req+0x38,1);scope.half(cpu,base+0x410,ms);result=context.base.call(cpu,entry['parent'],[],100000);parent=True
        elif entry['task']==1:
            scope.half(cpu,base+0x404,0x20);scope.half(cpu,req+0x10,ms);result=context.base.call(cpu,entry['parent'],[],100000);parent=True
        else:result=context.base.call(cpu,0x027eaaf8,[ms,entry['address']],100000)
    except Exception as exc:error=type(exc).__name__+':'+str(exc)
    finally:cpu.hook_del(token)
    installed=scope.getword(cpu,base+0x634);passed=bool(result and calls and calls[-1]['arguments'][1]==entry['address']and installed==entry['address'])
    return dict(name=entry['name'],mode=mode,offset=offset,time=ms,actualParentTaskReturn=bool(parent and result),actualDirectTimeoutInstallerReturn=bool(not parent and result),result=result,error=error,observedOriginalTimeoutCalls=calls,alarmPointerWord=hex(base+0x634),installedWord=hex(installed),passed=passed,postFaultStateCredited=False,sourceCredit=0,providers=[])

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for e in scope.ENTRIES:
        for mode in(0,2):
            for offset in(0,4):
                for ms in(0,1,65535):results.append(run(main,wram,e,mode,offset,ms,len(results)))
        print(json.dumps(dict(name=e['name'],passed=sum(r['passed']for r in results if r['name']==e['name']),examples=[r for r in results if r['name']==e['name']][:1])),flush=True)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),scopeGenerator=Path(scope.__file__).name,scopeGeneratorSha256=sha256(scope.__file__),results=results,actualParentTaskReturns=sum(r['actualParentTaskReturn']for r in results),actualDirectTimeoutInstallerReturns=sum(r['actualDirectTimeoutInstallerReturn']for r in results),qualifiedInstalledPointers=sum(r['passed']for r in results),sourceCredit=0,providers=[],limitations=['MeasChannel task channel/flash producer remains unexercised; its actual SetupTimeOut API is invoked directly with the statically proved callback pointer','Alarm storage installation is not physical timer dispatch or scene reachability','Any fault has zero supported return or post-fault state credit']);write_json(ROOT/'evidence/attempts/arm7-sdk342-mlme-timeout-installation-20261102.json',report)

if __name__=='__main__':main()
