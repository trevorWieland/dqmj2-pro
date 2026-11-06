import gzip
import hashlib
import json
import arm7_lane_card_callbacks_native_20261031 as fixture
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if original!=rebuilt or len(original)!=fixture.SIZES[address]:raise ValueError('Source callback must genuinely link every original byte')
    records=[]
    for count in (0,1,2,0xffffffff):
        for flag in (0,1,0x80000000):
            for source,response in ((0,0),(1,1),(0x80,0xff80),(0xff,0xffff),(1,0)):
                for seed in (0,15):
                    case=dict(count=count,flag=flag,source=source,response=response)
                    native=fixture.execute(address,original,case,seed)
                    source_result=fixture.execute(address,rebuilt,case,seed)
                    if native!=source_result or not native['actualReturn']:raise ValueError('Source callback direct CPU/full-memory/return model differs')
                    records.append(dict(case=case,seed=seed,mediated=False,state=native))
    for source,response in ((0,0),(1,1),(0xff,0xffff),(1,0)):
        case=dict(count=1,flag=1,source=source,response=response)
        native=fixture.execute(address,original,case,0,True)
        source_result=fixture.execute(address,rebuilt,case,0,True)
        if native!=source_result or not native['actualReturn']:raise ValueError('Source callback actual original transfer-caller continuation differs')
        records.append(dict(case=case,seed=0,mediated=True,state=native))
    controls=[]
    for budget,busy,name in ((1,False,'prologue-cap'),(1000,True,'uncompleted-busy-wait')):
        value=fixture.execute(address,original,dict(count=1,flag=1,source=1,response=1),0,False,budget,busy)
        if value['actualReturn']:raise ValueError('Stopped/uncompleted callback gained return credit')
        controls.append(dict(kind=name,execution=value,returnCredit=0))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-card-frontier2240-final/{address:08x}-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=True,vectors=124,actualOriginalAndCompiledReturns=248,
        actualDirectOwnedEntryReturns=240,actualIndirectOwnedCallbackReturns=8,separateOriginalTransferCallerReturns=8,
        actualSeparatelyObservedNestedReturns={},providerFreeOriginalAndCompiledReturns=0,
        syntheticBiosContractOriginalAndCompiledReturns=0,originalBiosExecutionCredit=0,hardwareExecutionCredit=0,
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteMappedMemoryModel=True,
        explicitSyntheticSpiReadbackTransactions=248,actualOriginalTransferCallerSourceCredit=0,
        meaningfulReturnContract='void; incidental R0 is captured without source meaning',freshMachinePerScenario=True,
        instructionLimit=20000,timeoutMicroseconds=500000,unsupportedControls=controls,unsupportedReturnCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=124,gzipMtime=0),
        limitations=['All owned callbacks actually return directly or through original transfer caller; those caller returns are counted separately with zero caller-source credit',
            'SPI readback is an explicit synchronous synthetic peripheral contract; physical storage, busy completion, asynchronous hardware and game meanings are unproved',
            'Own code/pool boundaries come from the independent frozen hash-qualified canonical supplement; no legacy namespace or unknown-symbol guard is persistently changed',
            'Complete nonstack memory effects are independently modeled; full CPU/stack records are original/source compared',
            'Initial counts0/1/2/FFFFFFFF, state words0/1/80000000 and matching/mismatching low-byte readbacks are synthetic isolated contexts, not ordinary caller-reachability claims'])
