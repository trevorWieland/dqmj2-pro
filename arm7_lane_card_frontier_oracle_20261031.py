import gzip
import hashlib
import json
import arm7_lane_card_frontier_service_oracle_20261031 as service
import arm7_lane_card_frontier_init_oracle_20261031 as initialization
import arm7_lane_card_frontier_callbacks_oracle_20261031 as callbacks
import arm7_lane_card_frontier_pages_oracle_20261031 as pages
import arm7_lane_card_frontier_commands_native_20261031 as commands
import arm7_lane_card_frontier_end_native_20261031 as completion
import arm7_lane_card_frontier_worker_native_20261031 as worker
from project import ROOT,sha256


def oracle(original,rebuilt,address):
    if address==0x03802624:return initialization.oracle(original,rebuilt,address)
    if address in (0x038028e4,0x03802924,0x03802974):return callbacks.oracle(original,rebuilt,address)
    if address in (0x03802b70,0x03802c28):return pages.oracle(original,rebuilt,address)
    if address in (0x0380272c,0x03802860,0x03802d70):return service.oracle(original,rebuilt,address)
    fixture=worker if address==worker.ADDRESS else completion if address==completion.ADDRESS else commands
    if original!=rebuilt or len(original)!=commands.engine.SIZES[address]:raise ValueError('Complete frontier body is not genuine linked original bytes')
    records=[];nested={};visited=set();providerfree=0;sleeps=0;transfers=0;saves=0;outer=0;prerequisites=0
    nonreturning=fixture is worker
    for index,case in enumerate(fixture.cases(address)):
        for flags in range(4):
            seed=index*4+flags
            native=fixture.execute(address,original,case,seed);source=fixture.execute(address,rebuilt,case,seed)
            returned=native['actualResumedOuterSleepReturn'] if nonreturning else native['actualReturn']
            if native!=source or not returned:raise ValueError('Fresh original/compiled frontier CPU/flags/memory/access/termination model differs')
            if nonreturning:
                outer+=2;transfers+=2*native['actualNonlocalContextTransfers'];saves+=2*native['ordinarySaveReturns']
            for entry,count in native.get('actualNestedReturns',{}).items():nested[entry]=nested.get(entry,0)+2*count
            prerequisites+=2*len(native.get('originalPrerequisites',[]))
            providerfree+=2*bool(native.get('staticMappedMmioOnly',fixture is completion))
            sleeps+=2*len(native.get('actualSleepProviderCalls',[]));visited.update(native['ownVisited'])
            records.append(dict(case=case,seed=seed,state=native))
    cap=fixture.execute(address,original,fixture.cases(address)[0],0,budget=1)
    if cap.get('actualReturn') or cap.get('actualResumedOuterSleepReturn'):raise ValueError('Bounded frontier cap gained actual return')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/f'work/arm7-bulk-20261030/lane-card-frontier2240-final/{address:08x}-records.json.gz'
    product.parent.mkdir(parents=True,exist_ok=True);product.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    return dict(supported=True,verifiedReturn=not nonreturning,verifiedNonreturningContextFlow=nonreturning,
        vectors=len(records),actualOriginalAndCompiledReturns=0 if nonreturning else 2*len(records),
        actualOwnedNormalReturns=0 if nonreturning else 2*len(records),actualResumedOuterSleepReturns=outer,
        actualNonlocalContextTransfers=transfers,ordinarySaveContextReturns=saves,ordinaryLoadContextReturns=0,
        actualSeparatelyObservedNestedReturns=nested,separatelyScopedOriginalPrerequisiteReturns=prerequisites,
        providerFreeOriginalAndCompiledReturns=providerfree,syntheticBiosContractOriginalAndCompiledReturns=0,
        actualSleepProviderCalls=sleeps,originalSleepFunctionExecutionCredit=0,
        fullRegistersFlagsStackAndMemoryCompared=True,independentCompleteMappedMemoryModel=fixture is completion,
        independentOwnOrderedStoreAndBranchModel=True,independentNativeContextAbiModel=nonreturning,
        allOwnInstructionAddressesVisited=sorted(visited),freshMachinePerScenario=True,
        instructionLimit=60000 if nonreturning else 30000 if fixture is completion else 20000,timeoutMicroseconds=500000,
        compiledShiftRequestDomain=[0,31] if nonreturning else None,
        originalBiosExecutionCredit=0,hardwareExecutionCredit=0,nativeCalleeSourceCredit=0,
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),compressedSha256=sha256(product),compressedBytes=product.stat().st_size,
            rawSha256=hashlib.sha256(raw).hexdigest(),rawBytes=len(raw),records=len(records),gzipMtime=0),
        unsupportedControls=[dict(kind='prologue-cap',execution=cap,returnCredit=0)],unsupportedReturnCredit=0,
        limitations=['Worker has zero owned normal returns; actual scheduler saves/loads and resumed sleeping-parent returns are separate',
            'Worker source shift is qualified only for request0..31; original receiver/protocol does not prove a global invariant or malformed-word equivalence',
            'Full source closure link equality covers own code/pools; original native callees remain zero-credit dependencies in unit execution',
            'Worker dispatch/physical arguments/own stores/context ABI are independent models; complete helper/stack memory semantics are compared original/source without a complete independent model',
            'Actual original kernel/CARD prerequisites execute; tick-sleep is an explicit bounded lower provider and MMIO is static synthetic backing',
            'Worker cartridge tests use a synthetic RAM header control word00800000 and static received wordDEADBEEF; these are not measured physical cartridge settings',
            'Worker positive entries begin with receive10 or task0C flags. Waiting/busy without a task, asynchronous flag producers, FIFO-full retries and physical data-ready timing remain unsupported',
            'Completion uses a READY native thread under disabled scheduling and actual original byte callbacks; no asynchronous/concurrent ownership claim',
            'No physical storage, hardware timing, BIOS, game-save, entitlement, scene reachability or renewal meaning is inferred'])
