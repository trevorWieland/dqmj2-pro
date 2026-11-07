import copy
import hashlib
import json
import re
import struct
import subprocess
from project import ROOT,read_json,write_json,sha256,now
import initialized_storage_protection_v3_20261106 as protection
import arm7_runtime
from wave20261106_arm7_sdk_next_switch_flow import analyze,controls as switch_controls
from wave20261106_arm7_wm_residual_next_third_boundary import certificate
REVISION='f3dd13d85469eee1b94cb083fb01849c29de911c'
CLOSURE='142f10ae8d094bf5ae27dc09a017b6ba3a19adeb'
NAMESPACE=('','arm7','arm7-wram')
LANE=ROOT/'evidence/lanes/parallel-wave20261106/arm7-sdk-next-proposal-v2'
ENTRIES=[0x038048e0,0x03804a20,0x03804b80,0x03804bc4,0x03804d40,0x03804fbc,0x0380516c,0x038052fc,0x0380532c,0x038053d0,0x03805418,0x03805784]
SDK='deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/'
def pin(p):return dict(path=p,sha256=sha256(ROOT/p))
def execute():
 if LANE.exists():raise ValueError('Fresh read-only SDK proposal evidence root required')
 intervals,pins=protection.protected(NAMESPACE,REVISION);inventory=read_json(ROOT/'evidence/arm7/ghidra-runtime-inventory.json');rom=(ROOT/'inputs/game.nds').read_bytes();header=struct.unpack_from('<4I',rom,0x30);raw=rom[header[0]:header[0]+header[3]];layout=arm7_runtime.derive(raw);module=next(m for m in layout['modules']if m['name']=='arm7-wram');image=raw[module['inputFileOffset']:module['inputFileOffset']+module['bytes']];base=int(module['base'],0)
 if hashlib.sha256(rom).hexdigest()!=read_json(ROOT/'project.json')['romSha256']or raw!=(ROOT/'extract/arm7/arm7.bin').read_bytes()or image!=(ROOT/module['binary']).read_bytes():raise ValueError('Original ROM/ARM7/autoload module lineage differs')
 rawLedger=subprocess.check_output(['git','show',REVISION+':ledger/functions.jsonl'],cwd=ROOT);ledger=[json.loads(line)for line in rawLedger.splitlines()];acquisition=read_json(ROOT/'evidence/tools/public-sdk-reference-acquisition-20261101.json');sdk=next(r for r in acquisition['references']if r['repository']=='ntrtwl/NitroSDK');primary=[]
 for name in ['pm/pm.c','pm/pm_pmic.c','pm/pm_selfBlink.c','pm/pm_send.c','pm/pm_sleep.c','pm/pm_utility.c','mic/mic.c','mic/mic_irq.c','mic/mic_sampling.c']:
  path=SDK+'libraries/spi/src/ARM7/'+name;expected=next(r for r in sdk['unmodifiedFiles']if r['path']==path);data=(ROOT/path).read_bytes()
  if hashlib.sha256(data).hexdigest()!=expected['sha256']or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=expected['gitBlobSha1']:raise ValueError('Primary complete PM source/blob changed')
  primary.append(expected)
 LANE.mkdir();rows=[]
 for entry in ENTRIES:
  original=next(r for r in ledger if(r.get('program')or'',r['processor'],r['module'],int(r['address'],0))==(*NAMESPACE,entry));ghidra=next(r for r in inventory['functions']if r['module']==NAMESPACE[2]and int(r['address'],0)==entry)
  if original['states']['functionMatched']or original['mode']!='arm'or any(a<=entry<b for a,b in intervals):raise ValueError('Candidate entry already accepted/reserved/protected or wrong mode')
  flow=analyze(image,base,entry);end=int(flow['computedEvidenceEndExclusive'],0);digest=hashlib.sha256(image[entry-base:end-base]).hexdigest();path=LANE/(format(entry,'08x')+'-flow.json');write_json(path,flow);overlaps=[dict(start=hex(max(a,entry)),endExclusive=hex(min(b,end)))for a,b in intervals if max(a,entry)<min(b,end)];foreign=[dict(address=r['address'],mode=r['mode'])for r in inventory['functions']if r['module']==NAMESPACE[2]and entry<int(r['address'],0)<end];proof=None;error=None;switchProofs=[switch_controls(image,base,int(s['dispatch'],0))for s in flow['boundedExecutableSwitches']]
  try:proof=certificate(flow,image,base,digest)
  except ValueError as problem:error=str(problem)
  eligible=proof is not None and not overlaps and not foreign and not flow['tailCalls']and not flow['indirectCalls']and not flow['addressOnlyReferences'];literals=sorted({r['value']for r in flow['literalReads']});row=dict(program='',processor='arm7',module='arm7-wram',mode='arm',architecture='ARMv4T',address=hex(entry),bytes=flow['computedEvidenceEnvelopeBytes'],endExclusive=hex(end),nativeSpanSha256=digest,entryReachableInstructionBytes=flow['reachableInstructionBytes'],actualLiteralReadBytes=flow['literalReadBytes'],originalGhidraBodyBytes=ghidra['bodyBytes'],originalGhidraRanges=ghidra['ranges'],flow=pin(path.relative_to(ROOT).as_posix()),completePerOriginCertificate=proof,certificateError=error,unresolved=flow['unresolved'],tailCalls=flow['tailCalls'],indirectCalls=flow['indirectCalls'],addressOnlyReferences=flow['addressOnlyReferences'],physicalProtectionIntersections=overlaps,foreignInteriorEntries=foreign,eligibleForIndependentBoundaryAdmission=eligible,literalValues=literals,sourceIdentity='MIC/timer3 family hypothesis from original0400010c/10e accesses and complete primary MIC code, no asserted per-entry names'if entry>=0x038053d0 else 'PM/SPI family hypothesis grounded by measured PM_SetLEDPattern0380528c calls, no asserted per-entry names',strictOriginalSwitchControls=switchProofs,sourceCredit=0,ownershipGranted=False);rows.append(row);print(row['address'],row['bytes'],eligible,error,len(overlaps),len(foreign),flush=True)
 finalIntervals,finalPins=protection.protected(NAMESPACE,REVISION)
 if finalPins!=pins or finalIntervals!=intervals:raise ValueError('Claim/spec/committed-protection epoch changed during read-only proposal; do not use this attempt')
 eligible=[r for r in rows if r['eligibleForIndependentBoundaryAdmission']];spans=sorted((int(r['address'],0),int(r['endExclusive'],0))for r in eligible);pairwise=[dict(first=hex(a),second=hex(c))for(a,b),(c,d)in zip(spans,spans[1:])if b>c]
 write_json(LANE/'proposal.json',dict(schemaVersion=1,createdUtc=now(),status='read-only-for-independent-admission',sourceCredit=0,sourceOwnershipGranted=False,sourceRevision=REVISION,committedClosure=CLOSURE,namespace=list(NAMESPACE),primaryFamilyHypothesis='NitroSDK ARM7 PM/SPI near qualified WM_End PM_SetLEDPattern import0380528c',candidates=rows,eligibleFunctions=len(eligible),eligibleBytes=sum(r['bytes']for r in eligible),pairwiseEligiblePhysicalOverlaps=pairwise,protectionEpochStable=True,protectionPins=pins,primaryC=dict(repository=sdk['repository'],revision=sdk['revision'],completeUnmodifiedFiles=primary,acquisition=pin('evidence/tools/public-sdk-reference-acquisition-20261101.json')),nativeLineage=dict(rom=pin('inputs/game.nds'),arm7HeaderWords=list(header),originalArm7Sha256=hashlib.sha256(raw).hexdigest(),autoloadModule=module,currentExtractMatchesOriginalRawROM=True),committedLedgerSha256=hashlib.sha256(rawLedger).hexdigest(),helper=pin('wave20261106_arm7_sdk_next_proposal_v2.py'),strictUnsignedSwitchHelper=pin('wave20261106_arm7_sdk_next_switch_flow.py'),limits=['All45 WM WL/MLME wrapper entries027e1a00..027e2a90 are already accepted at closed169; that lane has no new source opportunity.','No source authoring, compiler/linker invocation, ownership/registry/config/boundary/shared/index/Git or native mutation occurred.','Each entry is traversed independently with no neighbor-size input; every instruction/literal origin and exact physical coverage remains explicit. Full original incoming interior-reference review and Root integer-decoder/admission remain required.','Complete primary PM source is a grounded family reference, not exact original revision or per-entry source-name proof. Hardware primitives and any opaque/unproved boundaries remain uncredited; only Root may admit source scope.']))
 print('PROPOSAL',len(eligible),sum(r['bytes']for r in eligible),sha256(LANE/'proposal.json'),flush=True)
if __name__=='__main__':execute()
