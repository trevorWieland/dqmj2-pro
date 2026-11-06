import gzip
import hashlib
import json
from pathlib import Path
import prove_arm7_host_irq_gap208_scope_20261101 as scope
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/attempts/arm7-host-irq-fixed-words-20261101.json'
REFERENCES=[
 ('evidence/research/20261031-arm7-lane-os-reference-source.json','arm7/lib/src/OS_irqTable.c','48b80fa750884c15c5779ab1bf7afc78a4e6492e40522b4f26327db2b0e531b0'),
 ('evidence/research/20261031-arm7-lane-os-reference-source.json','arm7/lib/include/OS_interrupt.h','880ed6ce8b9d1f48ba4a4b442ee761b222e4b71a2b21cf37af088bf3b3de3e4c'),
 ('evidence/research/20261031-arm7-lane-arena-reference-source.json','arm7/lib/include/mmap.h','76db5abd30647732b27bf22802594efd03557dc6b849edba7ca6b1da5b602572')]


def references():
    records=[]
    for manifest,name,expected in REFERENCES:
        proof=json.loads((ROOT/manifest).read_text())
        if proof['commit']!='b623abef1b4dfe204ca50aab42447ac00c134290' or not proof['referenceOnly']or proof['compilerInput']:
            raise ValueError('Pinned source-specific SDK reference provenance differs')
        record=next(row for row in proof['files']if row['upstreamPath']==name);path=ROOT/record['localPath'];raw=path.read_bytes()
        git=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if len(raw)!=record['bytes']or sha256(path)!=record['sha256']or sha256(path)!=expected or git!=record['gitBlobSha1']:
            raise ValueError('Pinned SDK reference bytes/Git identity differs')
        records.append(dict(**record,manifest=manifest,manifestSha256=sha256(ROOT/manifest),referenceOnly=True,
            sameHistoricalSdkRevisionProven=False,licenseQualification='Source-specific pokediamond reference; no CC0 assignment'))
    mmap=(ROOT/records[2]['localPath']).read_text()
    lines=['#define HW_PRV_WRAM                 0x03800000','#define HW_PRV_WRAM_END             0x03810000',
        '#define HW_PRV_WRAM_SYSRV_SIZE      0x40','#define HW_INTR_CHECK_BUF           (HW_PRV_WRAM_SYSRV + 0x38)',
        '#define HW_VBLANK_COUNT_BUF         (HW_MAIN_MEM + 0x007ffc3c)']
    if not all(line in mmap for line in lines):raise ValueError('Pinned reserved-word mapping expressions differ')
    return records


def characterize():
    witness=json.loads(scope.REPORT.read_text());qualified=scope.validate(witness)
    trace=witness['native']['trace'];records=json.loads(gzip.decompress((ROOT/trace['path']).read_bytes()))
    check_reads=check_writes=counter_reads=counter_writes=initializer_writes=callback_zero=callback_nonzero=0
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();base=scope.BASE
    for row in records:
        result=row['execution'];case=row['case'];writes=result['writes'];reads=result['reads']
        cr=[value for address,width,value in writes if address==0x0380FFF8 and width==4]
        expected=case['flag']|(1<<scope.native.BITS[case['index']])
        if cr!=[expected]or [width for address,width in reads if address==0x0380FFF8]!=[4]:
            raise ValueError('Original reserved IRQ-check word full-width RMW differs')
        check_reads+=1;check_writes+=1
        observed=[value for address,width,value in writes if address==0x027FFC3C and width==4]
        if case['index']==8:
            if observed!=[(case['counter']+1)&0xFFFFFFFF]or [width for address,width in reads if address==0x027FFC3C]!=[4]:
                raise ValueError('Original absolute counter full-width wrap/read differs')
            counter_reads+=1;counter_writes+=1
        elif observed or any(address==0x027FFC3C for address,width in reads):
            raise ValueError('Unrelated dispatcher body accessed the reserved counter word')
        for prefix in row['prefixes'][:1]:
            if [value for address,width,value in prefix['writes']if address==0x027FFC3C and width==4]!=[0]:
                raise ValueError('Actual original initializer did not clear exact counter word')
            initializer_writes+=1
        if case['index']<8 and case['callback']:
            reset=any(address==scope.native.TICK+4 for address,width,value in writes)
            callback_nonzero+=int(reset);callback_zero+=int(not reset)
    roles=[]
    for address,name,calls in[(0x0380FFF8,'reserved-interrupt-check-word',[(0x037FB63C,140),(0x037FB748,80)]),
        (0x027FFC3C,'reserved-main-RAM-VBlank-counter-word',[(0x037FB748,80),(0x037FB798,36)])]:
        roles.append(dict(address=hex(address),bytes=4,mode='data',program='',processor='arm7',
            role=name,initializedOrBssModuleOwnership=False,sourceDataExtentCredit=0,
            qualifiedOriginalCallers=[dict(address=hex(entry),bytes=size,mode='arm',module='arm7-wram',
                fullRangeSha256=scope.linker.digest(raw[entry-base:entry-base+size]))for entry,size in calls],
            originalDataGuardStillRefuses=True,sourceBindingPermissionGranted=False))
    return dict(program='',processor='arm7',words=roles,sourceCredit=0,dataCredit=0,initializedDenominatorDelta=0,
        inputScope=dict(path=scope.REPORT.relative_to(ROOT).as_posix(),sha256=sha256(scope.REPORT),qualification=qualified),
        references=references(),originalCheckWordReads=check_reads,originalCheckWordWrites=check_writes,
        originalCounterReads=counter_reads,originalCounterWrites=counter_writes,originalCounterInitializerWritesSeparate=initializer_writes,
        originalCallbackZeroResetReturnsSeparate=callback_zero,originalCallbackNonzeroResetReturnsSeparate=callback_nonzero,
        platformArithmetic=dict(privateWramStart='0x3800000',privateWramEnd='0x3810000',systemReservedBytes=64,
            checkOffset=56,computedCheckWord=hex(0x03810000-64+56),
            counterExpression='HW_MAIN_MEM + 0x007ffc3c',nativeMeasuredCounter='0x27ffc3c',
            referenceMainMemDefinitionClosureSupplied=False),
        memoryModelLimits=['Synthetic RAM/register-shadow backing includes both exact absolute words; no physical mirror/coherence/timing claim',
            'Native reads/writes and fixed ABI address roles are measured; source admission remains caller-specific and unapproved',
            'A reserved word is not module BSS or initialized source data, and this receipt grants no neighboring address',
            'Public reconstructed SDK revision equivalence and original assembly authorship remain unproved'])


def produce():
    return dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),**characterize())


def validate(report):
    expected=produce()
    if report!=expected:raise ValueError('Current fixed-word native/caller/reference/extent evidence differs')
    return dict(qualifiedAbsoluteWords=2,sourceCredit=0,dataCredit=0,callerSourceAdmissionGranted=False)


def main():
    report=produce();validate(report);write_json(REPORT,report)
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),validation=validate(report))),flush=True)


if __name__=='__main__':main()
