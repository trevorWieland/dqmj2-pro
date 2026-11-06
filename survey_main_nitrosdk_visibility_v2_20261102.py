import concurrent.futures
import re
import subprocess
import os
from pathlib import Path
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json,write_json,sha256
from slice_reference_sdk_entities_v3_20261102 import functions,slice_closed
from link_runtime_unit import relocation_rows,measured_module
import close_main_nitrosystem_candidates_v3_20261102 as preprocessing
import link_main_nitrosdk_breadth_20261102 as linking
from externalize_sdk_storage_v1_20261102 import externalize

WORK=ROOT/'work/main-nitrosdk-visibility-v2-20261102'
INPUT=ROOT/'evidence/attempts/main-nitrosdk-masked-candidates-20261102.json'
SNAPSHOT=ROOT/'evidence/verification/accepted-cohort145-identities-v2-20261101.json'
RESERVED=[(0x0202BEDC,16),*[(a,n)for a,n in[(0x0202FB48,40),(0x0202FB70,40),(0x0202FD14,204),(0x02030268,176),(0x020303EC,160),(0x02031790,112)]]]


def prepare(job):
    index,row,contexts=job;identity=row['identity'];label=f'{index:04}-{int(identity["address"],0):08x}-{row["profile"]}'
    folder=WORK/'closed'/label;folder.mkdir(parents=True,exist_ok=True);result=dict(sourceCredit=0,identity=identity,referenceFunction=row['referenceFunction'],profile=row['profile'])
    try:
        context=contexts[(row['referenceSource'],row['profile'])];assert context['exitCode']==0
        original=ROOT/context['output'];assert sha256(original)==context['outputSha256'];text=original.read_text(encoding='utf-8')
        seed=row['referenceFunction'];declaration_count=0
        for record in sorted(functions(text),key=lambda r:r['start'],reverse=True):
            header=text[record['start']:record['opening']]
            if record['name']==seed or re.search(r'\binline\b',header):continue
            header=re.sub(r'\bstatic\s+','',header);text=text[:record['start']]+header.rstrip()+';\n'+text[record['end']:];declaration_count+=1
        text=re.sub(r'\bstatic\s+(?=[^;{}]*\b'+re.escape(seed)+r'\s*\()','',text)
        text,closure=slice_closed(text,[seed]);assert not closure['forbiddenTokens']
        text, storage = externalize(text)
        result['externalizedStorage'] = storage
        source=folder/'source.c';source.write_text(text,encoding='utf-8');flags=[];i=0
        while i<len(row['compilerFlags']):
            flag=row['compilerFlags'][i]
            if flag=='-i':i+=2;continue
            if flag.startswith('-D'):i+=1;continue
            flags.append(flag);i+=1
        obj=folder/'compiled.o';command=[str(ROOT/row['compiler']),*flags,'-c',str(source),'-o',str(obj)]
        process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        result.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),lines=len(text.splitlines()),lexicalSelection=closure,
         otherDefinitionsBecameDeclarations=declaration_count,command=command,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr)
        if process.returncode:return result
        relocations=relocation_rows(obj,seed)
        with obj.open('rb')as stream:
            elf=ELFFile(stream);symbols={s.name:s for s in elf.get_section_by_name('.symtab').iter_symbols()};symbol=symbols[seed]
            result['compiledBytes']=symbol['st_size']
            for relocation in relocations:
                s=symbols[relocation['symbol']];relocation.update(sourceSymbolType=s['st_info']['type'],sourceSymbolBinding=s['st_info']['bind'],sourceSymbolSection=s['st_shndx'])
        candidate=dict(row,referenceSource=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),compilerFlags=flags,relocations=relocations)
        result['candidate']=candidate
    except Exception as error:result.update(errorType=type(error).__name__,refusal=str(error))
    return result


def main():
    assert not (WORK/'report.json').exists(),'Preserve prior campaign'
    snapshot=read_json(SNAPSHOT);intervals=[(r['address'],r['address']+r['bytes'])for r in snapshot['functions']if r['module']=='main']
    intervals += [(a,a+n)for a,n in RESERVED]
    for name in ['cohort146-vram-gecom-sound-recruitment-and-abi-20261102-specification.json','cohort147-arm7-cam-bootstrap-and-native-constructor-20261102-specification.json','cohort148-nitrosdk-breadth-and-coherent-scene-20261102-specification.json']:
        intervals += [(int(r['address'],0), int(r['address'],0)+r['bytes']) for r in read_json(ROOT/name)['expectedAdditions'] if r['module']=='main']
    intervals += [(int(r['address'],0), int(r['address'],0)+r['bytes']) for r in read_json(ROOT/'evidence/inputs/main-sdk1188-source-units-20261102.json')['sourceUnits']]
    queue=[];seen=set()
    for row in read_json(INPUT)['candidates']:
        identity=row['identity'];address=int(identity['address'],0);key=address,row['profile'],row['referenceFunction']
        if row['sourceOwner']!='root'or key in seen or any(address<end and begin<address+identity['bytes']for begin,end in intervals):continue
        seen.add(key);queue.append(row)
    units={(r['referenceSource'],r['profile']):(r['referenceSource'],r['profile'],r['compilerFlags'],r['compiler'])for r in queue}
    preprocessing.WORK=WORK
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:contexts=dict(pool.map(preprocessing.preprocess,units.values()))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:closed=list(pool.map(prepare,[(i,r,contexts)for i,r in enumerate(queue)]))
    write_json(WORK/'compilation.json',dict(sourceCredit=0,results=closed))
    linking.WORK=WORK/'links';namespace=linking.namespace();metadata,image,_=measured_module('main')
    jobs=[(i,r['candidate'],namespace,image)for i,r in enumerate(closed)if r.get('candidate')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:linked=list(pool.map(linking.link,jobs))
    exact={r['identity']['address']:r for r in linked if r['genuineLinkedExact']}
    report=dict(sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),inputSha256=sha256(INPUT),
     excludedAcceptedSnapshot=SNAPSHOT.relative_to(ROOT).as_posix(),snapshotSha256=sha256(SNAPSHOT),reservedRanges=RESERVED,
     storageExternalizerSha256=sha256(ROOT/'externalize_sdk_storage_v1_20261102.py'), originalMainSha256=metadata['sha256'],preprocessed=list(contexts.values()),compilation=closed,linkResults=linked,
     unacceptedUniqueGenuineFunctions=len(exact),unacceptedUniqueGenuineBytes=sum(r['identity']['bytes']for r in exact.values()),
     allOutputsHypotheses=True,sourceInterfacesDataBindingsNativeProofAndModuleAcceptanceStillRequired=True)
    write_json(WORK/'report.json',report);write_json(ROOT/'evidence/attempts/main-nitrosdk-visibility-v2-breadth-20261102.json',report)
    print(dict(candidates=len(queue),compiling=len(jobs),genuineUnique=len(exact),genuineCandidateBytes=report['unacceptedUniqueGenuineBytes'],sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
