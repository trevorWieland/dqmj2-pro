import gzip
import json
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261105_arm7_wm_port_next_build import SOURCE,LANE,WORK,build
from wave20261105_arm7_wm_port_next_models import fixtures
from wave20261105_arm7_wm_port_next_execution import run
from wave20261105_arm7_wm_port_next_controls import execute as controls


def negative_cases():
    allFixtures=fixtures()
    def select(entry,**fields):return [f for f in allFixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:3]
    return [
      (0x027e7c20,'return (u16)tmptt;','return (u16)(tmptt+1);',select(0x027e7c20)),
      (0x027e637c,'status->sendQueueFreeList.head = 0;','status->sendQueueFreeList.head = 1;',select(0x027e637c)),
      (0x027e637c,'i < 32 - 1','i < 31 - 1',select(0x027e637c)),
      (0x027e6434,'status->child_bitmap == 0','status->child_bitmap != 0',select(0x027e6434,branch='child-zero')),
      (0x027e6434,'status->VSyncFlag == 1','status->VSyncFlag == 0',select(0x027e6434,branch='packet',vsync=1)),
      (0x027e6434,'wlResult->resultCode != 0x08','wlResult->resultCode == 0x08',select(0x027e6434,branch='packet',code=5)),
      (0x027e692c,'status->mp_prevTxop = (u16)txop','status->mp_prevTxop = (u16)(txop+1)',select(0x027e692c,branch='ping')),
      (0x027e692c,'status->mp_pingFlag == 0','status->mp_pingFlag != 0',select(0x027e692c,branch='ping')),
      (0x027e72d4,'wmHeader &= ~0x8000','wmHeader &= ~0x4000',select(0x027e72d4,small=False,count=0,header=0x8001)),
      (0x027e73c4,'sendDataSize == 0','sendDataSize == 1',select(0x027e73c4,size=0,free='pair')),
      (0x027e73c4,'destBitmap & childBitmap','destBitmap | childBitmap',select(0x027e73c4,size=4,free='pair')),
      (0x027e74f8,'if (!timeout)','if (timeout)',select(0x027e74f8,kind='flush-one',timeout=0,state=9,rest=2)),
      (0x027e74f8,'data->retryCount--;','data->retryCount++;',select(0x027e74f8,kind='flush-one',timeout=1,port=8,retry=2)),
      (0x027e7828,'baseQueue = status->readyQueue;','baseQueue = status->sendQueue;',select(0x027e7828,ready=True,aidMask=3)),
      (0x027e7828,'data->restBitmap &= aidBitmapMask;','data->restBitmap |= aidBitmapMask;',select(0x027e7828,ready=True,aidMask=3)),
      (0x027e7a1c,'cb_Port->aid = aid;','cb_Port->aid = status->aid;',select(0x027e7a1c,kind='parse',myAid=0,port=0,dest=False)),
      (0x027e7a1c,'(u16)(currSeqNo - seqNo) < (128 << 1)','(u16)(currSeqNo - seqNo) > (128 << 1)',select(0x027e7a1c,kind='parse',port=8,fresh=False,dest=False)),
      ('WmspMakePortPacket','status->sendQueueInUse = 1','status->sendQueueInUse = 0',select(0x027e6434,branch='packet')+select(0x027e692c,branch='packet'))]


def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;function='native_host_arm7_main_'+format(entry,'08x') if isinstance(entry,int) else entry;directory=WORK/'wrong-c'/str(ordinal)
    if not selected:raise ValueError('Meaningful wrong-C fixture selection empty')
    directory.mkdir(parents=True,exist_ok=True)
    for p in SOURCE.iterdir():
        if p.is_file():(directory/p.name).write_bytes(p.read_bytes())
    found=[]
    for path in directory.iterdir():
        if path.suffix not in ['.c','.h']:continue
        text=path.read_text()
        for f in functions(text):
            if f['name']==function:found.append((path,text,f))
    if len(found)!=1:raise ValueError('Wrong-C target function is not unique')
    path,text,fragment=found[0];start,end=fragment['start'],fragment['end'];part=text[start:end]
    if part.count(old)!=1:raise ValueError(('Meaningful ordinary-C mutation ambiguous',function,old,part.count(old)))
    path.write_text(text[:start]+part.replace(old,new)+text[end:]);affected={'native_host_arm7_main_'+format(f['entry'],'08x') for f in selected};rows,outputs=build(directory/'wm_port.c',directory/'build',affected,affected);by={int(r['address'],0):r for r in rows};reject=[]
    for n,f in enumerate(selected):
        row=by[f['entry']]
        try:
            result=run(row,outputs[row['name']],f,images,n)
            if not result['modelFailures']:raise ValueError(('Wrong-C failed to alter independently modeled behavior',function,old,n))
            reject.append(dict(ordinal=n,actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:reject.append(dict(ordinal=n,actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=function,old=old,new=new,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=reject,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-wm-port-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-wm-port-next' or WORK!=ROOT/'work/w5wp':raise ValueError('New WM port proof source/evidence/work scope changed')
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned actual native unit runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen actual WM port compiler/source/native/runtime input changed: '+p['path'])
    rows,outputs=build(SOURCE/'wm_port.c',WORK/'proof-positive');by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes()) for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set() for r in rows}
    for n,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,n);rebuilt=run(row,outputs[row['name']],f,images,n)
        if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=n,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete WM port caller/model mismatch')
        coverage[row['address']].update(a for a in original['pcs'] if f['entry']<=a<f['entry']+row['bytes']);traces.append(dict(ordinal=n,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes'] for r in rows)),flush=True);negative=[wrong_c(case,n,images) for n,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes']) for address,pcs in coverage.items()]
    limits=[
      'Nine complete admitted host ARM7-main ARMv4T functions:6476 whole bytes=6388 reached instruction+88 actual literal bytes. All57 original ELF relocations/addends genuinely link under measured2.0/sp1p5 O4,s/on,noauto/file-IPA/C99. Five readable owned C/header files preserve real WmspMakePortPacket file-IPA inlining and the original measured GetTmptt optimization pragma; no ordinary-logic ASM, object/binary/register/instruction patch, fake alias or native executable compiler input.',
      'Every production include is a closed quoted owned C/header. Pinned primary SDK comparison informed source/types but does not prove exact historical SDK revision/names or original storage allocations. Original native inputs serve only byte/reference/link/execution validation; compiler commands consume authored C/header inputs only. Imported anchors initialize0 code and gain0 callee/source/storage credit.',
      '355 original/source ARMv4T caller pairs require710 actual returns and independent state/return/import-word/ABI models, exact GPR/CPSR/SP/writes, full8MiB RAM+128KiB WRAM hashes. Fixtures cover timing/wrap/unsigned fields, queue init/allocation/full/error paths, retry/free/callback cleanup, receive size/aid/sequence/destination cases, ping/resume and send failure/empty/single-packet paths. Hardware VCOUNT/TSF reads are controlled words, not device emulation.',
      'All original imported bodies, including separately owned callers in this same packet, execute0 in caller fixtures. Mutex/IRQ/popcount/memory-copy/wireless-request/callback providers are explicit bounded modeled contracts; no real scheduler/radio/DS/game/Windows/Android execution claimed. Multi-packet fragmentation, most sequence/transmit and concurrency/hardware paths remain outside semantic fixtures, although their complete C code is genuinely byte-exact.',
      '18 genuinely linked wrong-C controls,627 exact original binding negatives,63 instruction/literal boundary negatives,3 geometry negatives,25 actual fresh ABI returns+4badABI and independent fresh C99 whole-function objects/relocations/genuine links are required. Aborted wrong-C runs are not actual caller returns. Callback words in queue/ABI fixtures are transferred only and never invoked.',
      'Minimal immutable boundary/native certificates and actual closed C/header/tool/native/runtime inputs are production dependencies. Historical claim/review/epoch-heavy proposal/atlas/dispatch and source materialization are admission/diagnostic provenance only. Old4464-byte ARM7 source and all historical READYs remain immutable. This packet has0 accepted source credit until shared coordinator gates and committed closure.']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes'] for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes'] for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
