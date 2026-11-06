import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
import match_runtime as c
from project import ROOT,write_json,sha256,configuration
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
BASE=ROOT/'nonmatching/overlay-lane/20261101-signed-remainder565'
QUEUE=BASE/'queue.json'
SNAPSHOT=ROOT/'evidence/verification/accepted-cohort107-identities-v2-20261101.json'


def repaired(source):
    token='SECOND_REG(native_fn_02026144(';count=0
    while token in source:
        start=source.index(token);begin=start+len(token);depth=1;end=begin
        while depth:
            if source[end]=='(':depth+=1
            if source[end]==')':depth-=1
            end+=1
        if source[end]!=')':raise ValueError('565 pseudo-call nesting differs')
        arguments=source[begin:end-1];depth=0;separators=[]
        for i,char in enumerate(arguments):
            if char=='(':depth+=1
            if char==')':depth-=1
            if char==','and depth==0:separators.append(i)
        if len(separators)!=1:raise ValueError('565 measured two-word runtime input is missing; do not invent an argument')
        split=separators[0];left,right=arguments[:split].strip(),arguments[split+1:].strip();source=source[:start]+'((s32) ('+left+') % (s32) ('+right+'))'+source[end+1:];count+=1
    return source,count


def prepare():
    if QUEUE.exists():
        queue=json.loads(QUEUE.read_text())
        if sha256(ROOT/queue['snapshot']['path'])!=queue['snapshot']['sha256']or sha256(ROOT/queue['abiProof']['path'])!=queue['abiProof']['sha256']:raise ValueError('565 immutable catalogue input changed')
        for row in queue['drafts']:
            source=ROOT/row['source'];directory=source.parent
            for path,key in[(source,'sourceSha256'),(source.with_name('context.h'),'contextSha256'),(directory/'original-source.txt','originalSourceSha256'),(directory/'original-context.txt','originalContextSha256')]:
                if sha256(path)!=row[key]:raise ValueError('565 repository-local draft/input copy changed')
            metadata,binary,symbols=measured_module(row['module']);address=int(row['address'],0)-0x021D7240
            if metadata['sha256']!=row['moduleSha256']or c.sha(binary[address:address+row['bytes']])!=row['nativeSpanSha256']:raise ValueError('565 native input changed')
        return queue
    accepted=json.loads(SNAPSHOT.read_text())['functions'];paths=subprocess.check_output(['rg','-l','--no-ignore','-g','*.c','SECOND_REG\\(native_fn_02026144','nonmatching/overlay-lane'],cwd=ROOT).decode().splitlines();groups={}
    for path in paths:
        text=(ROOT/path).read_text(encoding='utf-8-sig');m=re.search(r'\bnative_(ov\d{3})_([0-9a-f]{8})\s*\(',text)
        if m:groups.setdefault((m[1],m[2]),[]).append(path)
    rows=[];excluded=[]
    for(module,address),files in sorted(groups.items()):
        address=int(address,16);metadata,binary,symbols=measured_module(module);match=re.search(r'kind:function\(arm,size=(0x[0-9a-f]+)\) addr:0x'+f'{address:08x}',symbols)
        if match is None:raise ValueError('565 canonical boundary absent')
        size=int(match[1],0);overlap=[r for r in accepted if r['processor']=='arm9'and not r.get('program')and r['module']==module and max(r['address'],address)<min(r['address']+r['bytes'],address+size)]
        if overlap:excluded.append(dict(module=module,address=hex(address),reason='accepted107 interval overlap'));continue
        preferred=next((f for f in files if'20261031-sweep276-seeded'in f),files[-1]);old=ROOT/preferred;directory=BASE/module/f'{address:08x}-arm';directory.mkdir(parents=True,exist_ok=True);source,count=repaired(old.read_text(encoding='utf-8-sig'));header=old.with_name('context.h').read_text(encoding='utf-8-sig');header=re.sub(r'extern\s+u32\s+native_fn_02026144\(\);','extern s32 native_fn_02026144(s32, s32);',header)
        for name,text in[('source.c',source),('context.h',header),('original-source.txt',old.read_text(encoding='utf-8-sig')),('original-context.txt',old.with_name('context.h').read_text(encoding='utf-8-sig'))]:
            path=directory/name
            if path.exists()and path.read_text()!=text:raise ValueError('565 refuses to alter an existing draft')
            if name=='original-source.txt':path.write_bytes(old.read_bytes())
            elif name=='original-context.txt':path.write_bytes(old.with_name('context.h').read_bytes())
            else:path.write_text(text)
        rows.append(dict(processor='arm9',program='',module=module,address=hex(address),mode='arm',bytes=size,moduleSha256=metadata['sha256'],nativeSpanSha256=c.sha(binary[address-0x021D7240:address-0x021D7240+size]),originalSource=preferred,originalSourceSha256=sha256(old),originalContextSha256=sha256(old.with_name('context.h')),source=(directory/'source.c').relative_to(ROOT).as_posix(),sourceSha256=sha256(directory/'source.c'),contextSha256=sha256(directory/'context.h'),measuredRemainderReplacements=count,remainingPseudoCalls=source.count('SECOND_REG(')))
    queue=dict(schemaVersion=1,romSha256=configuration()['romSha256'],sourceCredit=0,snapshot=dict(path=SNAPSHOT.relative_to(ROOT).as_posix(),sha256=sha256(SNAPSHOT)),abiProof=dict(path='evidence/verification/main-nav562-signed-division-abi-20261101.json',sha256=sha256(ROOT/'evidence/verification/main-nav562-signed-division-abi-20261101.json')),drafts=rows,excluded=excluded)
    if QUEUE.exists()and json.loads(QUEUE.read_text())!=queue:raise ValueError('565 queue identity changed')
    write_json(QUEUE,queue);return queue


def worker(index):
    queue=json.loads(QUEUE.read_text());row=queue['drafts'][index];source=ROOT/row['source'];previous=c.symbol_address;attempts=[]
    if sha256(source)!=row['sourceSha256']or sha256(source.with_name('context.h'))!=row['contextSha256']:raise ValueError('565 draft input changed')
    def resolver(name):
        if name=='_s32_div_f':return 0x02026144
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',name):raise RuntimeError('565 unqualified other compiler intrinsic; no native-site fallback: '+name)
        return previous(name)
    c.symbol_address=resolver
    for speed in[False,True]:
        work=ROOT/'work/ol565'/row['module']/row['address'][2:]/str(speed);c.WORK=work/'compile';attempt=dict(speed=speed)
        try:
            results,unused=c.compare(source,row['module'],'2','off',speed);attempt['compilerResult']=results
            for entry in results:
                if entry.get('compileFailed'):continue
                entry['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
                try:proof=validate(entry,qualified_bindings(entry),work/'link')
                except ValueError as error:
                    if not isinstance(error.args[0],dict):raise
                    proof=error.args[0]
                attempt['genuineLinkComparison']=proof;attempt['exactCandidate']=bool(proof.get('exactCallerBytes'))or(proof.get('linkedBytes')==row['bytes']and proof.get('matchingBytes')==row['bytes']);attempt['linkedBodySha256']=c.sha((work/'link/caller.bin').read_bytes())
        except Exception as error:attempt['failure']=str(error)
        attempt['compilerEmittedElf']=bool(list((work/'compile/objects').glob('*.o')));attempts.append(attempt)
    report=dict(identity=row,sourceCredit=0,attempts=attempts,semanticCases=0,limits=['Finite native signed-runtime contract is a drafting override only.','Zero denominator and signed overflow retain abstract-C qualification limits.','Other generated SECOND_REG uses, unproven intrinsics, signatures and surrounding logic remain unresolved.'])
    output=ROOT/'evidence/attempts/signed-remainder565'/f"{row['module']}-{row['address'][2:]}.json";write_json(output,report);print(json.dumps(dict(module=row['module'],address=row['address'],bytes=row['bytes'],compiled=any(a['compilerEmittedElf']for a in attempts),linked=any('genuineLinkComparison'in a for a in attempts),exact=any(a.get('exactCandidate')for a in attempts))),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--worker',type=int);args=parser.parse_args()
    if args.worker is not None:worker(args.worker);return
    queue=prepare()
    def invoke(index):
        command=[sys.executable,str(PathSelf),'--worker',str(index)];result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
        if result.returncode:raise ValueError(dict(index=index,stderr=result.stderr))
        print(result.stdout.strip(),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(invoke,range(len(queue['drafts']))))
    reports=[json.loads((ROOT/'evidence/attempts/signed-remainder565'/f"{r['module']}-{r['address'][2:]}.json").read_text())for r in queue['drafts']];compiled=[r for r in reports if any(a['compilerEmittedElf']for a in r['attempts'])];linked=[r for r in reports if any('genuineLinkComparison'in a for a in r['attempts'])];exact=[r for r in reports if any(a.get('exactCandidate')for a in r['attempts'])];summary=dict(schemaVersion=1,sourceCredit=0,queueSha256=sha256(QUEUE),globallyNewDraftedFunctions=0,globallyNewDraftedNativeBytes=0,reworkedFunctions=len(reports),uniqueDraftedFunctions=len(reports),uniqueDraftedNativeBytes=sum(r['identity']['bytes']for r in reports),compilerEmittedFunctions=len(compiled),compilerEmittedNativeBytes=sum(r['identity']['bytes']for r in compiled),genuineLinkedFunctions=len(linked),genuineLinkedNativeBytes=sum(r['identity']['bytes']for r in linked),exactHypothesisFunctions=len(exact),exactHypothesisNativeBytes=sum(r['identity']['bytes']for r in exact),semanticallyTestedFunctions=0,semanticallyTestedNativeBytes=0,acceptedFunctions=0,acceptedBytes=0,reports=[dict(path=f"evidence/attempts/signed-remainder565/{r['identity']['module']}-{r['identity']['address'][2:]}.json",sha256=sha256(ROOT/f"evidence/attempts/signed-remainder565/{r['identity']['module']}-{r['identity']['address'][2:]}.json"))for r in reports]);write_json(ROOT/'evidence/attempts/signed-remainder565-summary-20261101.json',summary);print(json.dumps(summary),flush=True)


PathSelf=__file__
if __name__=='__main__':main()
