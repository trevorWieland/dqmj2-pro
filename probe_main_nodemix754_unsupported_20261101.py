import copy
import gc
import main_nodemix754_machine_20261101 as M
import main_nodemix754_models_20261101 as P
from match_main_nodemix754_20261101 import compile_unit,SOURCE
from project import ROOT,sha256,write_json
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_SP

def execute():
    original=M.inputs();packet,body=compile_unit(SOURCE,'unsupported-positive');outcomes=[]
    for candidate in[False,True]:
        profile=copy.deepcopy(P.profiles()[0]);profile['status']=0x08000000;profile['name']='static-busy-no-coherence';machine=M.Machine(original,profile,body if candidate else None)
        try:machine.run(2000)
        except ValueError as error:failure=str(error)
        else:raise ValueError('754 static busy unexpectedly returned')
        outcomes.append(dict(candidate=candidate,budget=2000,actualTopReturns=0,pc=hex(machine.u.reg_read(UC_ARM_REG_PC)),sp=hex(machine.u.reg_read(UC_ARM_REG_SP)),frames=len(machine.frames),completedNativeReturnInstructions=len(machine.events),failure=failure));machine.u=None;gc.collect()
    profile=copy.deepcopy(P.profiles()[0]);profile['entries']=[];profile['name']='zero-count-original-only';machine=M.Machine(original,profile)
    try:machine.run(2000)
    except Exception as error:zero=dict(originalOnly=True,actualTopReturns=0,failureType=type(error).__name__,failure=str(error),pc=hex(machine.u.reg_read(UC_ARM_REG_PC)))
    else:zero=dict(originalOnly=True,actualTopReturns=1,pc='stop')
    machine.u=None;gc.collect()
    write_json(ROOT/'evidence/attempts/main-nodemix754-unsupported-native-boundaries-20261101.json',dict(schemaVersion=1,sourceCredit=0,positiveRegressionReturnCredit=0,sourceSha256=sha256(SOURCE),headerSha256=sha256(SOURCE.with_name('context.h')),staticBusy=outcomes,zeroCount=zero,limits=['Static busy shadow never changes; no top return is expected or credited. This is no hardware-coherence or device claim.','Zero count is original binary research only. Reconstructed C is not run because its postloop pY is undefined at zero.','Native return instructions inside these interrupted executions are retained only as diagnostic counts,never added to positive source proof.']))
    print(dict(staticBusyTopReturns=0,zeroCountOriginal=zero),flush=True)

if __name__=='__main__':execute()
