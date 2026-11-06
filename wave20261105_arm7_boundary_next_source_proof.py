import gzip
import json
import re
from pathlib import Path
from project import ROOT,read_json,sha256,write_json,configuration
import match_runtime as C
import unicorn
from wave20261102_host_arm7_sixth_slice import functions
from wave20261105_arm7_boundary_next_source_build import build,SOURCE,LANE,WORK
from wave20261105_arm7_boundary_next_source_models import fixtures
from wave20261105_arm7_boundary_next_source_execution import run
from wave20261105_arm7_boundary_next_source_controls import execute as controls


def chosen(maximum=4,**fields):return [f for f in fixtures() if all(f.get(k)==v for k,v in fields.items())][:maximum]


def negative_cases():
    return [
      ('wrong-receive-blocking','027e0898.c',None,'&msg, 1','&msg, 0',chosen(kind='null')),
      ('wrong-confirm-blocking','027e0898.c',None,'&(sys->confirmQ), msg, 1','&(sys->confirmQ), msg, 0',chosen(kind='confirm')),
      ('wrong-confirm-queue','027e0898.c',None,'&(sys->confirmQ)','&(sys->fromWLmsgQ)',chosen(kind='confirm')),
      ('wrong-group-mask','027e0898.c',None,'& 0xFF00','& 0xFFFF',chosen(kind='default')),
      ('lost-MA-group','027e0898.c',None,'case 0x0100 :','case 0x0200 :',chosen(kind='default',code=0x181)),
      ('wrong-indication-bit','027e0898.c',None,'cmd_id & 0x80','cmd_id & 0x40',chosen(kind='default')),
      ('lost-null-message-exit','027e0898.c',None,'if (msg == 0)','if (msg != 0)',chosen(kind='null')),
      ('empty-message-loop','027e0898.c',None,'while (1 )','while (0 )',chosen(kind='null')),
      ('wrong-WM-buffer-gate','context003.h','WmspIndicate','((void *)0) == WMSP_GetSystemWork()->wm7buf','((void *)0) != WMSP_GetSystemWork()->wm7buf',chosen(kind='drop',buf=False,state=0)),
      ('wrong-stop-state-gate','context003.h','WmspIndicate','WM_STATE_STOP == WMSP_GetStatusStructure()->state','WM_STATE_STOP != WMSP_GetStatusStructure()->state',chosen(kind='default',state=0)),
      ('wrong-freed-packet','context003.h','WmspIndicate','native_host_arm7_arm_027e1a08(req);','native_host_arm7_arm_027e1a08((WlCmdReq *)0);',chosen(kind='default')),
      ('wrong-beacon-zero-gate','context003.h','WmspIndicateMlmeBeaconSend','beaconIndicateFlag > 0','beaconIndicateFlag == 0',chosen(kind='beacon',beacon=0)),
      ('wrong-beacon-signedness','context003.h','WmspIndicateMlmeBeaconSend','WMSP_GetStatusStructure()->beaconIndicateFlag > 0','(s16)WMSP_GetStatusStructure()->beaconIndicateFlag > 0',chosen(kind='beacon',beacon=32768)),
      ('wrong-beacon-api','context003.h','WmspIndicateMlmeBeaconSend','callback->apiid = WM_APIID_START_PARENT','callback->apiid = WM_APIID_START_PARENT+1',chosen(kind='beacon',beacon=1)),
      ('wrong-beacon-error','context003.h','WmspIndicateMlmeBeaconSend','callback->errcode = WM_ERRCODE_SUCCESS','callback->errcode = WM_ERRCODE_FAILED',chosen(kind='beacon',beacon=1)),
      ('wrong-beacon-state','context003.h','WmspIndicateMlmeBeaconSend','callback->state = WM_STATECODE_BEACON_SENT','callback->state = WM_STATECODE_BEACON_SENT+1',chosen(kind='beacon',beacon=1))]


def mutation(case,images):
    label,file,function,old,new,selected=case
    if not selected:raise ValueError('Empty meaningful ARM7 wrong-C fixture selection')
    directory=WORK/'proof'/label;directory.mkdir(parents=True,exist_ok=True)
    for p in SOURCE.iterdir():
        if p.is_file():(directory/p.name).write_bytes(p.read_bytes())
    target=directory/file;text=target.read_text();first,last=0,len(text)
    if function:
        record=next(r for r in functions(text) if r['name']==function);first,last=record['start'],record['end']
    fragment=text[first:last]
    if fragment.count(old)!=1:raise ValueError(('Whole ordinary-C mutation ambiguous',label,fragment.count(old)))
    target.write_text(text[:first]+fragment.replace(old,new)+text[last:]);row,body=build(directory/'027e0898.c',directory/'build',True);rejected=[]
    for n,f in enumerate(selected):
        try:
            result=run(row,body,f,images,n)
            if not result['modelFailures']:raise ValueError(('Wrong C model was not independently rejected',label,n))
            rejected.append(dict(ordinal=n,actualCallerReturn=result['actualTopReturn'],rejectedAtObservedProtocolBoundary=result['rejectedAtObservedProtocolBoundary'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejected.append(dict(ordinal=n,actualCallerReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=label,sourcePart=file,function=function,old=old,new=new,fixtures=selected,rejected=rejected,genuineLinkedWrongC=row,abortedNegativeRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-boundary-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next/source' or WORK!=ROOT/'work/w5ab-source':raise ValueError('New source/proof evidence/work materializer scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned native unit runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for p in inputs['files']:
        if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen actual ARM7 source/compiler/native input changed: '+p['path'])
    row,body=build(SOURCE/'027e0898.c',WORK/'proof/positive');layout=read_json(ROOT/'evidence/arm7/runtime-layout.json');images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes()) for m in layout['modules']];main=next(b for base,b in images if base==0x027e0000);native=main[0x898:0x1a08];traces=[]
    for n,f in enumerate(fixtures()):
        original=run(row,native,f,images,n);rebuilt=run(row,body,f,images,n)
        if original!=rebuilt or original['modelFailures'] or not original['actualTopReturn']:
            write_json(LANE/'fixture-failure.json',dict(ordinal=n,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent finite ARM7 caller/state protocol mismatch')
        traces.append(dict(ordinal=n,fixture=f,result=original))
    print('original/source ARM7 caller pairs',len(traces),flush=True);negatives=[mutation(case,images) for case in negative_cases()];controlled=controls(row);write_json(LANE/'binding-layout-controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));covered={pc for t in traces for pc in t['result']['pcs'] if 0x027e0898<=pc<0x027e1a08}
    limits=[
      'One complete4464B ordinary-C ARMv4T indication-thread function genuinely MW-links all4392 instruction+72 literal bytes under measured2.0/base O4,s/on,noauto/file-IPA/C99. All130 original relocations/addends preserved,33 mode-only anchors initialize0 callee bytes. No source/object/binary/register/instruction patch, ordinary-logic ASM, fabricated alias or canonical-tail substitution.',
      'Six owned closed readable C/type files have no ASM/comments/system/forced includes or binary compiler inputs. Public SDK comparison informed types/code but does not prove historical revision/full original declarations. All out-of-line imported definitions remain prototypes; private inline C belongs to the selected compiler-emitted whole function. No original data/storage extent credit.',
      '297 independent native/source ARMv4T caller fixture pairs require594 actual returning callers, exact registers/CPSR/SP/72B frame/writes/full8MiB RAM+128KiB WRAM and ordered imported words/modes. Finite0/1/3-message streams cover null message, nonindication confirm, null-WM/STOP drops, unsupported indication codes and beacon flag0/1/high16 cases, borrowed member guards and controlled provider changes.',
      'OS_ExitThread is an intercepted modeled boundary allowed to return solely to close the original explicit epilogue. This does not execute or claim real scheduler/thread-exit/network/game/Windows/Android behavior. Other complex indication arms are byte-exact C but remain outside these bounded semantic fixtures. All original imported bodies execute0 in caller fixtures; arbitrary queue convergence is unproved.',
      'Two exact original callable words027e1724 to 027e1ad4 and027e19fc to 027e1c00 bind their actual ARM entries. Strict original stub/pool/namespace/target proofs and24 negatives plus56 separate actual ARMv4T thunk-to-tail transfers check R0/IP/LR/SP/flags. Only these two tiny original thunk entries execute in separate controls; tail bodies execute0 and get0 source credit. Parent tail1ae8, child tail1c0c remain separate and are never substituted.',
      '1430 original binding/body/origin/addend/namespace negatives,3 compiler-geometry rejects,20 fresh unsigned-field/low16 ABI returns+3badABI and16 genuinely linked wrong-C controls are required. Aborted wrong-C memory/protocol tests are not actual caller returns.',
      'Only minimal immutable native/callable certificates and actual consumed C/header/runtime/tool/native inputs are production dependencies. Historical epoch-heavy claim/review/atlas/dispatch and independent coordinator module preflight are diagnostic/admission provenance. Source remains0 accepted credit until coordinator shared acceptance; old socket/ARM7 sources and all frozen proofs stay unchanged.']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm7',program='',module='arm7-main',allPassed=True,matches=[row],canonicalMatchedFunctions=1,canonicalMatchedBytes=4464,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,originalThunkEntriesExecutedInSeparateControls=2,originalTailBodiesExecuted=0,calleeSourceCredit=0,externalStorageCredit=0,fixtureCoveredOriginalInstructionBytes=4*len(covered),negativeEvidence=negatives,inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),bindingLayoutControls=dict(path=(LANE/'binding-layout-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-layout-controls.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=limits)
    write_json(LANE/'match.json',report);print(dict(functions=1,bytes=4464,cases=len(traces),boundedCoveredInstructionBytes=4*len(covered)),flush=True)


if __name__=='__main__':execute()
