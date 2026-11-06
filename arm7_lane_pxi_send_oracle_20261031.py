import gzip
import hashlib
import json
import prove_arm7_lane_pxi_plain_20261031 as fixture
from project import ROOT,sha256

ADDRESS,SIZE=0x037FE448,96


def oracle(original,rebuilt,address):
    if address!=ADDRESS or len(original)!=SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary raw-word PXI sender must genuinely link every original byte')
    records=[]
    irq={hex(key):0 for key in fixture.IRQ}
    controls=(0,2,0x100,0x4000,0x4002,0xC000,0xFFFF,0x8000)
    for control in controls:
        for word in (0,1,0x12345678,0x80000000,0xFFFFFFFF):
            for seed in range(4):
                native=fixture.execute(address,original,control,word,seed)
                source=fixture.execute(address,rebuilt,control,word,seed)
                if not native['actualReturn'] or native!=source:
                    raise ValueError('Original/source PXI signed status, full word, memory/stores/CPU differ')
                records.append(native)
                for entry,count in native['actualNativeIRQReturns'].items():
                    irq[entry]+=2*count
    own=set(range(address,address+fixture.CODES[address],4))
    if {pc for row in records for pc in row['visited']}!=own:
        raise ValueError('Supported PXI sender corpus did not visit every own instruction')
    cap=fixture.execute(address,original,0,0,91,budget=1)
    if cap['actualReturn'] or cap.get('postBoundaryStateExcluded') is not True:
        raise ValueError('PXI sender exhaustion gained return/state credit')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-pxi-send96-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        providerFreeOriginalAndCompiledReturns=2*len(records),syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSeparatelyObservedNestedReturns=irq,fullRegistersFlagsStackAndMemoryCompared=True,
        independentCompleteWramMmioAndOrderedStoreModel=True,independentExactStoreFootprintModel=True,
        independentSigned32StatusAndFullWordSendModel=True,allOwnInstructionAddressesVisited=sorted(own),
        freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,cpuModel='Unicorn TI925T ARMv4T surrogate',
        instructionLimit=20000,timeoutMicroseconds=500000,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,calleeSourceCredit=0,
        providerReplacements=[],physicalIpcHardwareCredit=0,
        meaningfulReturnContract='Signed32 status: errorbit14 returns-1 with a halfword acknowledgment write; send-full bit1 returns-2; otherwise write full32-bit word and return0',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,functionMatchedBytes=96,moduleAdopted=False,
        limitations=['Mapped FIFO registers are static deterministic RAM inputs; CPU writes are measured without claiming physical FIFO or write-one-to-clear behavior',
            'Original IRQ disable/restore execute without providers and actual returns are tracked; errorbit14 bypasses those helpers',
            'All mapped nonstack memory and exact ordered nonstack store width/value/multiplicity, signed status and preserved CPU/stack ABI are independently modeled; all stack bytes and ordered reads are original/source compared',
            'Raw32-bit sender and a union for caller bitfield inspection preserve one consistent physical interface; receiver224 remains a separate source/proof backlog',
            'No received-message dispatch, asynchronous hardware, full26-bit payload API legality or enclosing scene claim; bounded exhaustion has no post-boundary data credit'])
