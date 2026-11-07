from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_ov000_controller_composite_next_first_paths import EVIDENCE,SOURCE,WORK,assert_owned
from wave20261106_ov000_controller_composite_next_first_packet import CONTRACT,source_policy

PREFIX='wave20261106_ov000_controller_composite_next_first'


def pin(path):
    value=Path(path)
    if value.is_absolute():value=value.relative_to(ROOT)
    name=value.as_posix()
    return dict(path=name,sha256=sha256(ROOT/name))


def main():
    assert_owned(EVIDENCE,SOURCE,WORK)
    if(EVIDENCE/'inputs.json').exists():raise ValueError('Immutable first input manifest already exists')
    report=read_json(WORK/'initial-genuine-links.json');rows=report['matches'];native=read_json(EVIDENCE/'native-inputs.json')
    if len(rows)!=2 or sum(r['bytes']for r in rows)!=744:raise ValueError('First coherent caller partition differs')
    claim=read_json(ROOT/native['claim']['path']);claimed={r['id']:r for r in claim['claimedFunctions']}
    interfaces=ROOT/'evidence/lanes/parallel-wave20261106/ov000-controller-followup-scout/accepted-main-interface-pins-v1.json';interface=read_json(interfaces)
    native_helpers=[]
    for helper in interface['helpers']:
        address=int(helper['address'],0);image=(ROOT/native['mainImage']['path']).read_bytes();body=image[address-0x2000000:address-0x2000000+helper['bytes']]
        import hashlib
        if hashlib.sha256(body).hexdigest()!=helper['originalBodySha256']:raise ValueError('Accepted helper full native extent changed')
        native_helpers.append(helper)
    derivation=dict(basis='measured-private-ROM-game-controller-C-reconstruction',publicPrimarySourceClaimed=False,claim=pin(ROOT/native['claim']['path']),coordinatorAdmission=pin(EVIDENCE.parent/'coordinator-admission.json'),actualNativeInputs=pin(EVIDENCE/'native-inputs.json'),correctedCFGAndLiteralCoverage='Root admission uses cfg_v2 with condition codes independent of instruction identifiers; earlier census unchanged.',profile=dict(compiler='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',optimization='O2',inline='off',speed=True,frontend='explicit-C99',profileGrid=False),acceptedHelperInterfaceEvidence=pin(interfaces),originalExecutedHelpers=native_helpers,consumedLayout=dict(entryBytes=8,slotStride=12,entryLink=0,entrySignedFields=[4,5,6],linkResource=4,resourceFlags=24,setupSignedTag=16,pointSignedHalfwords=[0,2],rendererWideBufferBytes=64,initializerPositionAccumulatorBits=32,fullNativeResourceAllocationProven=False),providerBoundary='Actual original c65812/c758200/main49ad020/main49be4172 bodies execute where called,with0extra credit. All deeper allocator/format/render providers are bounded supplied services with0executed body instructions.',portableInterfaceLimitations=['Private imported consumed-field views do not unify nominal interfaces across source files or prove native Windows object layout.','Source return words are bounded caller observations; no nominal whole-program portable interface or game-purpose meaning is claimed.','Imported BSS/global arrays carry no storage ownership or initialized-byte credit; declarations express only measured accesses.','No game-purpose/renderer/controller naming beyond measured field and call roles is claimed.'],preparedNewFunctions=2,preparedNewBytes=744,acceptedCredit=0,originalAssemblyBytes=0,unselectedAttemptInputs=False)
    derivation['nominalInterfaceDebt']=pin(EVIDENCE/'abi-view-debt.json')
    overlay=(ROOT/native['image']['path']).read_bytes()
    derivation['additionalOriginalExecutedHelpers']=[dict(address=hex(a),bytes=n,nativeSpanSha256=hashlib.sha256(overlay[a-0x21d7240:a-0x21d7240+n]).hexdigest(),extraSourceCredit=0)for a,n in[(0x221c658,12),(0x221c758,200)]]
    write_json(EVIDENCE/'derivation.json',derivation)
    external={p['path']for key,p in native.items()if isinstance(p,dict)and set(['path','sha256'])<=set(p)}
    external.add((EVIDENCE/'abi-view-debt.json').relative_to(ROOT).as_posix())
    external.update(['src/runtime/parallel_wave20261106/ov000-slot-controller-next/first/0221c758/0221c758.c','src/runtime/parallel_wave20261106/ov000-slot-controller-next/first/0221c758/context.h','src/transplants/ov000-reuse01/native_ov000_0221c658.c'])
    external.update(['project.json','provenance/seed-manifest.json',(EVIDENCE.parent/'coordinator-admission.json').relative_to(ROOT).as_posix(),(EVIDENCE/'native-inputs.json').relative_to(ROOT).as_posix(),(EVIDENCE/'scope-input.json').relative_to(ROOT).as_posix(),(EVIDENCE/'derivation.json').relative_to(ROOT).as_posix(),interfaces.relative_to(ROOT).as_posix()])
    for helper in native_helpers:
        for item in helper['selectedSourcePins']:
            if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Accepted helper source identity changed')
            external.add(item['path'])
            header=(ROOT/item['path']).parent/'context.h'
            if header.exists():external.add(header.relative_to(ROOT).as_posix())
    code=code_closure([PREFIX+'_packet.py',PREFIX+'_ready.py',Path(__file__).name,'replay_parallel_packet.py'])
    names=set(code)|external
    for row in rows:
        source_policy(row);identity=next(r for r in native['entries']if r['address']==row['address'])
        if identity['id']not in claimed or row['targetSha256']!=identity['targetSha256']:raise ValueError('Selected caller escaped admitted exact native identity')
        names.add(row['source']);names.update(p['path']for p in row['sourceDependencies'])
    tools=['tools/mwccarm/mwccarm/license.dat',*['tools/mwccarm/mwccarm/2.0/base/'+name for name in ['mwccarm.exe','mwldarm.exe','ELFIO.dll','MSL_All-DLL80_x86.dll','lmgr8c.dll']]]
    names.update(tools)
    names.update(p.relative_to(ROOT).as_posix()for p in(ROOT/'deps/native').rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix!='.pyc')
    if any(name.startswith('work/')or name.endswith(('.o','.elf','.bin'))and not name.startswith(('extract/','deps/'))for name in names):raise ValueError('Compiler experiments/build products entered frozen runtime closure')
    value=dict(schemaVersion=1,immutableInputManifest=True,mandatoryExternalInputs=[pin(name)for name in sorted(external)],files=[pin(name)for name in sorted(names)],generatorSources=[pin(name)for name in code],entries=[{key:row[key]for key in CONTRACT}for row in rows])
    write_json(EVIDENCE/'inputs.json',value)
    print(dict(inputs=(EVIDENCE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(EVIDENCE/'inputs.json'),pins=len(names),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)


if __name__=='__main__':main()
