import gzip
import hashlib
import json
import arm7_lane_volume_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address!=fixture.ADDRESS or len(original)!=fixture.SIZE or original!=rebuilt:
        raise ValueError('Full ordinary volume C must genuinely link every original byte')
    records=[]
    total=0
    indices=set()
    for seed,case in enumerate(fixture.cases(address)):
        native=fixture.execute(fixture.setup(address,original,case,seed))
        source=fixture.execute(fixture.setup(address,rebuilt,case,seed))
        if native!=source or len(native['states'])!=case['passes'] or any(not row['actualReturn'] for row in native['states']):
            raise ValueError('Original/source packed volume returns/interworking/state differ')
        records.append(native)
        total+=2*len(native['states'])
        indices.update(row['syntheticBiosServices'][0][1] for row in native['states'])
    own=set(range(address,address+fixture.CODE,4))
    if {pc for row in records for pc in row['visited']}!=own or indices!=set(range(724)):
        raise ValueError('Volume instruction or complete normalized-index coverage differs')
    caps=[]
    for name,case,budget in (
        ('prologue-cap',fixture.cases(address)[0],1),
        ('original-BIOS-service-unavailable',dict(value=0,volume=None,passes=1),1000),
        ('out-of-contract-BIOS-result',dict(value=0,volume=128,passes=1),1000)):
        result=fixture.execute(fixture.setup(address,original,case,91),budget)
        if result['states'][0]['actualReturn'] or result['states'][0].get('postBoundaryStateExcluded') is not True:
            raise ValueError('Unsupported BIOS/exhaustion gained native return/state credit')
        caps.append(dict(kind=name,execution=result,returnCredit=0))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-volume116-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    binary=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    scopes=[dict(module='arm7-wram',processor='arm7',program='',mode=mode,address=hex(entry),bytes=size,
        sha256=hashlib.sha256(binary[entry-fixture.BASE:entry-fixture.BASE+size]).hexdigest(),sourceCredit=0)
        for entry,size,mode in ((fixture.VENEER,12,'arm'),(fixture.THUMB,4,'thumb'))]
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=total,
        providerFreeOriginalAndCompiledReturns=0,syntheticBiosContractOriginalAndCompiledReturns=total,
        actualSeparatelyObservedNestedReturns={hex(fixture.THUMB):total},actualArmVeneerTailTransfers=total,
        ordinaryArmVeneerReturnCredit=0,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentExactNonstackStoreFootprint=True,
        independentPackedUnsigned16ReturnModel=True,normalizedServiceIndexCoverage=list(range(724)),
        allOwnInstructionAddressesVisited=sorted(own),freshMachinePerScenario=True,
        persistentEntryCallsPerScenario='Two calls on13 signed clamp/divisor/extreme boundaries; one call elsewhere',
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=1000,timeoutMicroseconds=100000,
        providerReplacements=[dict(kind='explicit-synthetic-BIOS-SVC1C-contract',indexRange=[0,723],outputRange=[0,127],
            testedOutputs=[0,1,126,127],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,sourceCredit=0)],
        originalNativeHelperScopes=scopes,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        meaningfulReturnContract='Unsigned16 packed synthetic service output with divisor bits; all signed32 native inputs are modeled, clamped-index classes and boundary representatives are tested',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=caps,unsupportedReturnCredit=0,functionMatchedBytes=116,moduleAdopted=False,
        limitations=['The owned ARM routine, original ARM veneer and original Thumb SVC/BX-LR stub execute; only the BIOS service result is an explicit synthetic contract',
            'Every normalized index0..723 is tested with four allowed7-bit service outputs; clamp/divisor boundary and full-word signed extremes are included, without exhaustive2^32 input claims',
            'Original BX-IP interworking and Thumb BX-LR return are distinguished from an invented normal ARM-veneer return',
            'Nonstack memory and empty nonstack store footprint, u16 return and preserved CPU/stack ABI are independently checked; stack bytes and all ordered accesses are original/source compared',
            'No BIOS image/table is installed/read/reconstructed; no original-BIOS result, physical audio/peripheral behavior or original helper source credit is assigned',
            'Unavailable service, out-of-contract result and bounded exhaustion are failures with no post-boundary state or return credit'])
