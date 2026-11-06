import hashlib
import json
from pathlib import Path
import match_runtime
from unicorn.arm_const import UC_ARM_REG_PC
import arm7_sdk327_control_setters_key_native_20261102 as native
from project import ROOT,sha256,write_json

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();rows=[]
    for mode,control,state,channel in[(0,1,16,0),(0,1,16,1),(0,1,16,14),(2,1,16,1),(0,0,17,1),(2,0,17,1)]:
        case=dict(entry=0x027ef548,mode=mode,contextOffset=0,irq=0xffffffff,control=control,state=state,channel=channel);cpu,meta,args=native.prepare(main,wram,case,len(rows));result=error=None
        try:result=native.context.base.call(cpu,case['entry'],[args['arg0'],args['arg1']],budget=200000)
        except Exception as failure:error=type(failure).__name__+':'+str(failure)
        row=dict(case=case,actualOriginalOwnReturn=bool(result and result['actualReturn']),entry=result,error=error,stopPc=hex(cpu.reg_read(UC_ARM_REG_PC)),actualSetupReturns=meta['prerequisiteReturns'],instructionCap=200000,providerReplacements=[],compiledSourceComparisonPerformed=False,currentThreeFunctionSourceContractBroadened=False,sourceCredit=0,postFaultStateCredit=0)
        if result:row['returningState']=dict(rawState=int.from_bytes(cpu.mem_read(meta['context']+0x34c,2),'little'),rawMode=int.from_bytes(cpu.mem_read(meta['context']+0x350,2),'little'),confirmationLength=int.from_bytes(cpu.mem_read(args['confirmation']+2,2),'little'))
        rows.append(row)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputModuleSha256=dict(main=hashlib.sha256(main).hexdigest(),wram=hashlib.sha256(wram).hexdigest()),cases=rows,actualOriginalOwnReturns=sum(r['actualOriginalOwnReturn']for r in rows),unsupportedFaultsOrExhaustions=sum(not r['actualOriginalOwnReturn']for r in rows),sourceCredit=0,physicalRadioAndRealSceneUnproved=True);path=ROOT/'evidence/attempts/arm7-sdk335-device-radio-context-limits-20261102.json';write_json(path,report);print(json.dumps(dict(originalReturns=report['actualOriginalOwnReturns'],unsupported=report['unsupportedFaultsOrExhaustions'],sha256=sha256(path))),flush=True)

if __name__=='__main__':main()
