import gzip
import hashlib
import json
import arm7_lane_card_service_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or len(original)!=fixture.SIZES[address] or original!=rebuilt:
        raise ValueError('Complete CARD ordinary C must genuinely link every original byte')
    records=[];nested={};providers=0;providerfree=0;visited=set()
    for index,case in enumerate(fixture.cases(address)):
        for flags in range(4):
            seed=index*4+flags
            native=fixture.execute(address,original,case,seed)
            source=fixture.execute(address,rebuilt,case,seed)
            if native!=source or not native['actualReturn']:
                raise ValueError('Original/source CARD CPU/memory/access/actual returns differ')
            for key,count in native['actualNestedReturns'].items():nested[key]=nested.get(key,0)+2*count
            providers+=2*len(native['actualSleepProviderCalls'])
            if native['staticMappedMmioOnly']:providerfree+=2
            visited.update(native['ownVisited'])
            records.append(dict(case=case,seed=seed,state=native))
    cap=fixture.execute(address,original,fixture.cases(address)[0],0,1)
    if cap['actualReturn']:raise ValueError('Stopped CARD native run gained return')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-card-frontier2240-final/{address:08x}-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True);product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        actualSeparatelyObservedNestedReturns=nested,providerFreeOriginalAndCompiledReturns=providerfree,
        syntheticBiosContractOriginalAndCompiledReturns=0,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        actualSleepProviderCalls=providers,originalSleepFunctionExecutionCredit=0,
        fullRegistersFlagsStackAndMemoryCompared=True,independentOwnOrderedStoreDelayAndBranchModel=True,
        independentCompleteMappedMemoryModel=address==0x03802860,allOwnInstructionAddressesVisited=sorted(visited),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,nativeCalleeSourceCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,
        limitations=['Wait/erase have independent own ordered-write/branch/argument models; helper effect details are compared original/source without claiming an independent complete helper-memory model',
            'The132-byte transfer additionally has an independent complete nonstack mapped-memory model with real original byte-write callback',
            'Status getter, transfer and callback code execute originally; supplied SPI responses and skipped lower sleep function are explicit bounded contracts',
            'Static mapped-MMIO zero responses are counted separately from sleep/nonzero readback contracts; no physical hardware, timing, persistent storage or game-save claim',
            'Supported finite sector sizes1/4/256 and address widths1/2/3 do not prove zero/nonpower-of-two sectors, unsupported serializers, unbounded counts, asynchronous changes or global caller invariants',
            'Void ABI does not assign meaning to incidental R0; actual full CPU/stack/access/memory records nevertheless match original/source'])
