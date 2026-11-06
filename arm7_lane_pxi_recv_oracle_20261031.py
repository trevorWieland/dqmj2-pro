import gzip
import hashlib
import json
import prove_arm7_lane_pxi_queue_v3_20261031 as fixture
import prove_arm7_lane_pxi_plain_20261031 as plain
from build_arm7_lane_pxi_recv_callback_v3_20261031 import build
from project import ROOT,sha256

ADDRESS,SIZE=0x037FE4A8,224


def oracle(original,rebuilt,address):
    if address!=ADDRESS or len(original)!=SIZE or original!=rebuilt:
        raise ValueError('Complete ordinary PXI receiver must genuinely link every original byte')
    probe=build()
    records=[]
    nested={}
    callbacks=0
    plain_returns=0
    queues=([],[0],[1],[0x21],[0xFFFFFFFF],[0xFFFFFFDF],[0,1,0x21,0xFFFFFFDF],[1,1,1,1],
        [1]*16,[(tag|(((tag*0x12345)&0x3FFFFFF)<<6)|((tag&1)<<5)) for tag in range(16)],
        [(tag|(((tag*0x12345)&0x3FFFFFF)<<6)|((tag&1)<<5)) for tag in range(16,32)])
    for words in queues:
        for full in (False,True):
            for mask in (0,0xFFFFFFFF,2,0x80000000):
                for error in (False,True):
                    for seed in range(4):
                        native=fixture.execute(original,words,full,seed,callback_mask=mask,initial_error=error,probe=probe)
                        source=fixture.execute(rebuilt,words,full,seed,callback_mask=mask,initial_error=error,probe=probe)
                        if native!=source or not native['actualReturn']:
                            raise ValueError('PXI source/native FIFO-contract returns/state/ordered effects differ')
                        records.append(dict(kind='synthetic-MMIO-FIFO-contract',record=native))
                        callbacks+=2*native['actualSyntheticCallbackReturns']
                        for entry,count in native['actualOriginalHelperReturns'].items():
                            nested[entry]=nested.get(entry,0)+2*count
    for control in (0x100,0x102,0x8100,0x8102):
        for seed in range(16):
            native=plain.execute(address,original,control,0,seed)
            source=plain.execute(address,rebuilt,control,0,seed)
            if native!=source or not native['actualReturn']:
                raise ValueError('PXI provider-free empty receive returns/state differ')
            records.append(dict(kind='static-mapped-register-empty',record=native))
            plain_returns+=2
            for entry,count in native['actualNativeIRQReturns'].items():
                nested[entry]=nested.get(entry,0)+2*count
    own=set(range(address,address+fixture.CODE,4))
    if {pc for row in records for pc in row['record']['visited']}!=own:
        raise ValueError('PXI receive corpus did not visit every own instruction')
    caps=[]
    for name,control,budget in (('prologue-cap',0x100,1),('static-RAM-error-does-not-recover',0x4100,1000)):
        native=plain.execute(address,original,control,0,91,budget)
        source=plain.execute(address,rebuilt,control,0,91,budget)
        if native!=source or native['actualReturn'] or native.get('postBoundaryStateExcluded') is not True:
            raise ValueError('PXI unsupported plain-RAM error/exhaustion gained return or state credit')
        caps.append(dict(kind=name,execution=native,returnCredit=0))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-pxi-recv224-final/supported-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),
        providerFreeOriginalAndCompiledReturns=plain_returns,syntheticMmioFifoContractOriginalAndCompiledReturns=2*len(records)-plain_returns,
        syntheticBiosContractOriginalAndCompiledReturns=0,actualSeparatelyObservedNestedReturns=nested,actualSyntheticCallbackReturns=callbacks,
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteWramMmioAndOrderedStoreModel=True,
        independentExactStoreAndProviderUpdateModels=True,independentThreeU32CallbackAndRawEchoModels=True,
        allOwnInstructionAddressesVisited=sorted(own),freshMachinePerScenario=True,persistentEntryCallsPerScenario=1,
        cpuModel='Unicorn TI925T ARMv4T surrogate',instructionLimit=20000,timeoutMicroseconds=500000,
        providerReplacements=[dict(kind='bounded-MMIO-FIFO-pop-empty-and-W1C-error-contract',maximumWords=16,physicalHardwareCredit=0),
            dict(kind='compiled-three-u32-callback-log-contract',physicalArgumentWords=3,originalCalleeCredit=0,sourceCredit=0)],
        syntheticCallbackProof=probe[1],originalBiosExecutionCredit=0,hardwareExecutionCredit=0,physicalIpcHardwareCredit=0,calleeSourceCredit=0,
        meaningfulReturnContract='Void receiver; actual return after empty FIFO, with incidental R0 compared without assigning a game result',
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=caps,unsupportedReturnCredit=0,functionMatchedBytes=224,moduleAdopted=False,
        limitations=['Provider-free empty mapped-register returns are separate from explicit FIFO pop/empty/error-ack contract returns and synthetic callback returns',
            'The original raw-word sender and IRQ helpers execute; original-source/calldata credit is0 for every dependency and every test callback',
            'Tag0 skip, callback-present arguments(tag,payload26,flag1), callback-absent flag1 skip, flag0 echo, send-full and synthetic error recovery have independent memory/store/provider/argument models',
            'Error acknowledgment clears bit14 only through an explicit deferred device contract; plain RAM errorbit14 remains set and the unsupported native path exhausts rather than receiving fabricated hardware success',
            'All mapped nonstack memory, exact CPU store multiplicity and exact provider update sequence are independently checked; all ordered accesses and stack bytes are original/source compared',
            'Only compiled ARM callback log contracts, at most16 FIFO words and deterministic status are supported; real/Thumb callbacks, asynchronous hardware, longer queues and enclosing application behavior remain unqualified'])
