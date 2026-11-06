import gzip
import json
import hashlib
import arm7_lane_channel_locks_native_20261031 as fixture
from build_arm7_lane_channel_lock_callback_20261031 import build
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address not in fixture.SIZES or len(original)!=fixture.SIZES[address] or original!=rebuilt:
        raise ValueError('Complete ordinary channel-lock C must genuinely link every original byte')
    probe=build()
    records=[]
    nested={}
    callbacks=0
    provider_free=0
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed,probe))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed,probe))
        if native!=source or len(native['states'])!=2 or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source channel lock actual returns, state, registers and ordered effects differ')
        records.append(native)
        for state in native['states']:
            count=state['actualNestedReturns'].get(hex(fixture.PROBE),0)
            callbacks+=2*count
            provider_free+=2*int(count==0)
            for helper,returns in state['actualNestedReturns'].items():
                if int(helper,0) in fixture.HELPERS:
                    nested[helper]=nested.get(helper,0)+2*returns
    own=set(range(address,address+fixture.CODES[address],4))
    if {pc for row in records for pc in row['visited']}!=own:
        raise ValueError('Supported channel-lock corpus did not visit every own instruction')
    cap=fixture.execute(fixture.setup(address,original,fixture.cases(address)[0],71,probe),budget=1)
    if cap['states'][0]['actualReturn'] or cap['states'][0].get('postBoundaryStateExcluded') is not True:
        raise ValueError('Channel-lock exhaustion gained return/state credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-channel-locks456-final/supported-{address:08x}.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    total=4*len(records)
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=total,
        providerFreeOriginalAndCompiledReturns=provider_free,syntheticCallbackContractOriginalAndCompiledReturns=total-provider_free,
        syntheticBiosContractOriginalAndCompiledReturns=0,actualSeparatelyObservedNestedReturns=nested,
        actualSyntheticCallbackReturns=callbacks,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentExactStoreFootprintModel=True,
        independentHelperAndThreeArgumentCallbackModel=True,allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=2,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[dict(kind='source-compiled-three-argument-channel-callback-contract',physicalArgumentWords=3,originalCalleeCredit=0,sourceCredit=0)],
        syntheticCallbackProof=probe[1],meaningfulReturnContract='Void function; incidental R0 is compared original/source without assigning an integer result',
        argumentDomain='Full32-bit mask and weak words; low16 mask bits select channels0..15, weak bit0 chooses the lock word; upper mask bits remain in full-word lock updates',
        nativeHelpers=[dict(address=hex(entry),codeBytes=size,originalCalleeCredit=0) for entry,size in fixture.HELPERS.items()],
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,
        functionMatchedBytes=len(original),moduleAdopted=False,
        limitations=['Full mapped memory, exact ordered nonstack store values/widths/multiplicity and real helper/callback arguments are independently modeled; all ordered accesses and stack bytes are compared original/source',
            'Original StopChannel and FreeExChannel execute without providers; synthetic callback code/log storage have zero original-callee/data/source credit',
            'Full-word masks include high-only and mixed high/low bits; lock gating reads only the strong word, while weak bit0 chooses which full word is updated',
            'Synthetic callback contracts preserve channel state except the explicit log; real game callbacks may modify broader state and remain unqualified',
            'Mapped MMIO effects preserve the old hold bit when hold0 and clear only enable bit31; this is a CPU/memory model, not physical audio/peripheral execution',
            'No enclosing scene/channel ownership, asynchronous callback/concurrency or malformed backing claim; bounded exhaustion has no post-boundary state credit'])
