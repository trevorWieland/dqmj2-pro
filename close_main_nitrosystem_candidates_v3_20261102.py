import concurrent.futures
import os
import subprocess
from pathlib import Path
import match_runtime as base
from project import ROOT,read_json,write_json,sha256
from slice_reference_sdk_entities_v3_20261102 import slice_closed

INPUT=ROOT/'work/main-nitrosystem-links-20261101/report.json'
WORK=ROOT/'work/main-nitrosystem-closed-v3-20261102'


def preprocess(unit):
    source,profile,flags,compiler=unit
    identity=source.removesuffix('.c').replace('/','-')+'-'+profile
    directory=WORK/'preprocess'/identity;directory.mkdir(parents=True,exist_ok=True)
    output=directory/'expanded.i';command=[str(ROOT/compiler),*flags,'-E',str(ROOT/source),'-o',str(output)]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120,
        env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    row=dict(source=source,sourceSha256=sha256(ROOT/source),profile=profile,command=command,
        compilerSha256=sha256(ROOT/compiler),exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr)
    if result.returncode==0:row.update(output=output.relative_to(ROOT).as_posix(),outputSha256=sha256(output))
    write_json(directory/'result.json',row)
    return(source,profile),row


def close(row,preprocessed):
    identity=row['identity'];label=identity['address'][2:]+'-'+row['profile']
    directory=WORK/'candidates'/label;directory.mkdir(parents=True,exist_ok=True)
    result=dict(referenceFunction=row['referenceFunction'],identity=identity,sourceCredit=0,
        fullSourceCallerTypeNativeProofStillRequired=True)
    try:
        context=preprocessed[(row['referenceSource'],row['profile'])]
        if context['exitCode']:raise ValueError('Original whole-source preprocessing refused')
        raw=ROOT/context['output'];assert sha256(raw)==context['outputSha256']
        text,selection=slice_closed(raw.read_text(encoding='utf-8'),[row['referenceFunction']])
        source=directory/'closed.c';source.write_text(text,encoding='utf-8')
        flags=[];original=row['entry']['compilerFlags'];index=0
        while index<len(original):
            if original[index]=='-i':index+=2;continue
            if original[index].startswith('-D'):index+=1;continue
            flags.append(original[index]);index+=1
        assert '#include'not in text
        obj=directory/'compiled.o';command=[str(ROOT/row['entry']['compiler']),*flags,'-c',str(source),'-o',str(obj)]
        process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120,
            env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        result.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),lines=len(text.splitlines()),
            selection=selection,compiler=row['entry']['compiler'],compilerFlags=flags,command=command,
            compilerSha256=sha256(ROOT/row['entry']['compiler']),exitCode=process.returncode,
            stdout=process.stdout,stderr=process.stderr,headerInputs=0,lexicalSelectionOnly=True)
        if process.returncode==0:result.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
    except Exception as error:result.update(errorType=type(error).__name__,refusal=str(error))
    write_json(directory/'result.json',result);return result


def main():
    records=read_json(INPUT)['results'];unique={}
    for row in records:
        if row['genuineLinkedExact']:unique.setdefault(row['identity']['address'],row)
    units={}
    for row in unique.values():
        entry=row['entry'];key=row['referenceSource'],row['profile']
        units[key]=(row['referenceSource'],row['profile'],entry['compilerFlags'],entry['compiler'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:preprocessed=dict(pool.map(preprocess,units.values()))
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        for index,result in enumerate(pool.map(lambda row:close(row,preprocessed),unique.values())):
            results.append(result)
            if(index+1)%8==0:print(dict(completed=index+1,total=len(unique),compiling=sum(row.get('exitCode')==0 for row in results)),flush=True)
    write_json(WORK/'report.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        inputSha256=sha256(INPUT),helper='slice_reference_sdk_entities_v3_20261102.py',
        helperSha256=sha256(ROOT/'slice_reference_sdk_entities_v3_20261102.py'),preprocessed=list(preprocessed.values()),
        results=results,sourceCredit=0,standaloneCompilerInputHypothesesOnly=True,
        newGenuineLinkCompleteTypeReviewAndNativeProofsRequired=True))
    print(dict(candidates=len(results),compiling=sum(row.get('exitCode')==0 for row in results),
        unresolvedLexicalEntities=sum(bool(row.get('selection',{}).get('forbiddenTokens'))for row in results),sourceCredit=0))


if __name__=='__main__':
    main()
