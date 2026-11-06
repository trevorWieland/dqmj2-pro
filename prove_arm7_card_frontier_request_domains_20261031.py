import arm7_lane_card_frontier_worker_native_20261031 as fixture
from project import ROOT,sha256,write_json


def main():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=raw[fixture.ADDRESS-fixture.BASE:fixture.ADDRESS-fixture.BASE+fixture.SIZE]
    records=[]
    for request in (0,1,2,15,16,31,32,63,255,256,0xffffffff):
        for pending in (0,0x10):
            machine=fixture.setup(fixture.ADDRESS,body,dict(request=0,allowed=False,length=0,task=False),request&15)
            cpu=machine['cpu']
            def put(target,value):cpu.mem_write(target,value.to_bytes(4,'little'))
            put(fixture.COMMON+4,0);put(fixture.COMMON+8,0);put(fixture.COMMON+0xfc,pending)
            disabled=machine['invoke'](0x037fc558)
            result=machine['invoke'](0x038031d4,(11,request,1),True)
            if not disabled['actualReturn'] or not result['actualReturn']:raise ValueError('Original receiver did not actually return')
            current=int.from_bytes(cpu.mem_read(fixture.COMMON+4,4),'little')
            flags=int.from_bytes(cpu.mem_read(fixture.COMMON+0xfc,4),'little')
            phase=int.from_bytes(cpu.mem_read(fixture.COMMON+8,4),'little')
            expected=pending|(0x10 if 2<=request<=15 else 0)
            if (current,flags,phase)!=(request,expected,0 if expected&0x10 else 1):raise ValueError('Independent receiver command/pending/phase model differs')
            records.append(dict(request=hex(request),initialPending=hex(pending),actualReturn=True,execution=result,
                finalRequest=hex(current),finalFlags=hex(flags),finalPhase=phase,compiledWorkerExecuted=False,
                requestWithinCompiledShiftDomain=request<32,actualWorkerExecutionCredit=0,sourceCredit=0))
    report=ROOT/'evidence/arm7/lane-card-frontier-request-domains-20261031.json'
    write_json(report,dict(generator='prove_arm7_card_frontier_request_domains_20261031.py',generatorSha256=sha256(__file__),
        module='arm7-wram',moduleSha256=sha256(ROOT/'extract/arm7/runtime/arm7-wram.bin'),receiverAddress='0x038031d4',
        actualReceiverReturns=len(records),records=records,sourceCredit=0,workerSourceOrReturnCredit=0,
        conclusions=['Fresh no-pending receiver contexts set receive flag only for requests2..15 among tested words',
            'A preexisting pending receive flag survives malformed command32/63/255/256/FFFFFFFF and the raw request is overwritten',
            'No global request<=31 invariant is proved. Compiled C worker shift semantics remain restricted to supported request0..31; malformed protocol words are unresolved',
            'Original receiver executes with disabled scheduler and a READY original-created CARD thread; no concurrent IRQ producer or physical FIFO execution is claimed']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),actualOriginalReceiverReturns=len(records),workerCredit=0))


if __name__=='__main__':main()
