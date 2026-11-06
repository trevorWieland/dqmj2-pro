import hashlib
import json
from pathlib import Path
import struct
import match_runtime
from unicorn import UC_HOOK_MEM_READ
import arm7_sdk306_task_command_context_20261102 as context
import arm7_sdk308_command_dispatch_native_20261102 as commands
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/attempts/arm7-sdk316-table-equality-native-20261102.json'

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();rows=[]
    for group,(table,count,low,minimum)in commands.TABLES.items():
        for state in(0,65535):
            for offset in(0,4):
                cpu,meta=context.setup(main,wram,len(rows),offset=offset,heap=True);base=meta['context'];allocated=context.base.call(cpu,0x037f886c,[base+512,384]);request=allocated['outgoingR0'];confirmation=request+16;code=group+count;adjacent=table+8*count;raw=main[adjacent-context.base.MAIN:adjacent-context.base.MAIN+8]
                if not request or not any(struct.unpack('<HH',raw[:4])):raise ValueError('Expected bounded real allocation and nonzero physical-adjacent minimum')
                cpu.mem_write(request+12,struct.pack('<HH',code,0));cpu.mem_write(confirmation,struct.pack('<HHH',code,0,0xa55a));cpu.mem_write(base+844,struct.pack('<H',state));cpu.mem_write(base+830,bytes(2));cpu.mem_write(base+1064,bytes(2));reads=[]
                def read(machine,access,address,width,value,user):
                    if adjacent<=address<adjacent+8:reads.append(dict(address=hex(address),width=width,raw=bytes(machine.mem_read(address,width)).hex()))
                hook=cpu.hook_add(UC_HOOK_MEM_READ,read);result=None;error=None
                try:result=context.base.call(cpu,commands.TOP,budget=200000)
                except Exception as failure:error=type(failure).__name__+':'+str(failure)
                finally:cpu.hook_del(hook)
                record=dict(code=hex(code),table=hex(table),declaredElements=count,physicalAdjacentAddress=hex(adjacent),physicalAdjacentRawData=raw.hex(),state=state,contextOffset=offset,actualOriginalEntryReturn=bool(result and result['actualReturn']),entry=result,error=error,physicalAdjacentReads=reads,originalSetupEntryReturns=meta['prerequisiteReturns']+[allocated],sourceDefinedBehaviorClaim=False,reconstructedTableExtentDelta=0,sourceCredit=0,compiledSourceComparisonPerformed=False,postFaultCredit=0)
                if result:
                    record.update(confirmationLength=int.from_bytes(cpu.mem_read(confirmation+2,2),'little'),confirmationResult=int.from_bytes(cpu.mem_read(confirmation+4,2),'little'))
                    if not reads or record['confirmationLength']!=1 or record['confirmationResult']!=4:raise ValueError('Measured original adjacent-record length failure changed')
                rows.append(record)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputModules=dict(main=hashlib.sha256(main).hexdigest(),wram=hashlib.sha256(wram).hexdigest()),cases=rows,actualOriginalEntryReturns=sum(r['actualOriginalEntryReturn']for r in rows),unsupportedFailures=sum(not r['actualOriginalEntryReturn']for r in rows),definedCAndCompiledSourceEquivalentCredit=0,tableExtentOrDataSourceCredit=0,initializedDenominatorDelta=0,malformedPhysicalBehaviorDoesNotBroadenFiveCallerSourceContract=True);write_json(REPORT,report);print(json.dumps(dict(returns=report['actualOriginalEntryReturns'],unsupported=report['unsupportedFailures'],sha256=sha256(REPORT))),flush=True)

if __name__=='__main__':main()
