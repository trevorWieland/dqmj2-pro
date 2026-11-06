import gzip
import hashlib
import json
import arm7_lane_alarm_registration_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or len(original)!=fixture.SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary periodic registration C must genuinely link every original byte')
    records=[]
    nested={}
    for index,case in enumerate(fixture.cases(address)):
        for flags in range(4):
            seed=index*4+flags
            native=fixture.execute(fixture.setup(address,original,case,seed))
            source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
            if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
                raise ValueError('Original/source registration BOOL/clock ABI/memory/actual returns differ')
            records.append(native)
            for state in native['states']:
                for entry,count in state['actualOriginalHelperReturns'].items():
                    nested[entry]=nested.get(entry,0)+2*count
    own=set(range(address,address+fixture.CODE,4))
    if {pc for row in records for pc in row['visited']}!=own:
        raise ValueError('Registration corpus did not visit every own instruction')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],91),budget=1)
    if cap['states'][0]['actualReturn']:
        raise ValueError('Registration bounded exhaustion gained return credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-alarm-registration156-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=4*len(records),
        providerFreeOriginalAndCompiledReturns=4*len(records),syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=nested,separatelyScopedOriginalPrerequisiteReturns=2*sum(len(row['originalPrerequisites']) for row in records),
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=False,
        independentCompleteMappedMemoryModel=True,independentBooleanAndSevenPhysicalWord64BitClockModel=True,
        independentExactStoreFootprintModel=False,allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[],registeredCallbackExecutions=0,originalTimerInterruptHandlerExecutions=0,
        meaningfulReturnContract='BOOL1 only after both availability checks pass and initially-zero flag permits registration; unavailable/already-enabled/reentry returns0',
        actualPeriodicAlarmPhysicalWords=7,rawPeriod=0x82E,registeredCallback='arm7:arm7-wram:ARM037FE65C',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,functionMatchedBytes=156,moduleAdopted=False,
        limitations=['Original tick/alarm initialization, availability accessors, alarm create, GetTick, periodic insertion, timer IRQ registration and IRQ helpers execute without providers',
            'The input alarm44 bytes are randomized; independent memory models check create/reset/register fields, global queue/head/tail, timer callback/armed words, mapped timer/IRQ registers and every other mapped nonstack byte',
            'The callback argument is measured at alarm+4 and CreateAlarm clears+8; an initial model omission was caught by randomized alarm input and corrected from nativeSTR at037FD5A8',
            'All seven physical periodic-call words and unsigned64-bit current/start arithmetic are independently checked across counter/halfword-timer/pending-request inputs; queue starts empty and start-time wrap is not claimed',
            'Exact redundant-store multiplicity and execution-stack bytes are not independently prescribed; original/source ordered accesses, all stack bytes and full CPU records are compared',
            'Registered callback and timer interrupt handlers are forbidden from executing; no period-to-physical-time, FIFO purpose, asynchronous hardware, nonempty existing alarm queue or enclosing-scene claim'])
