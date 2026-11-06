import os
import re
import subprocess
from project import ROOT,read_json,write_json,sha256
from slice_reference_sdk_entities_v3_20261102 import functions,slice_closed
from wave20261102_child_fourth_types import write_closed

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/sdk'
WORK=ROOT/'work/w5ml/sdk/closed-v3'


def main():
    probe=next(r for r in read_json(LANE/'reference-probes.json')['results'] if r['profile']=='base4p');compiler=ROOT/probe['compiler'];reference=ROOT/probe['referenceSource'];WORK.mkdir(parents=True,exist_ok=True);expanded=WORK/'expanded.i'
    command=[str(compiler),*probe['compilerFlags'],'-E',str(reference),'-o',str(expanded)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Original read-only reference preprocessing failed',process.stdout,process.stderr))
    original=expanded.read_text();matches=[r for r in read_json(LANE/'normalized-reference-matches.json')['results'] if r['profile']=='base4p'];results=[]
    for row in matches:
        name=row['referenceFunction'];text=original
        for function in sorted(functions(text),key=lambda f:f['start'],reverse=True):
            header=text[function['start']:function['opening']]
            if function['name']==name:
                text=text[:function['start']]+re.sub(r'\bstatic\s+','',header)+text[function['opening']:]
                continue
            if re.search(r'\binline\b',header):continue
            text=text[:function['start']]+re.sub(r'\bstatic\s+','',header).rstrip()+';\n'+text[function['end']:]
        try:
            text,selection=slice_closed(text,[name]);text=re.sub(r'\bstatic\s+(?=[^;{}]*\b'+re.escape(name)+r'\s*\()', '', text);directory=WORK/name;path=directory/(name+'.c');headers=write_closed(text,name,path)
            flags=[];index=0
            while index<len(probe['compilerFlags']):
                token=probe['compilerFlags'][index]
                if token=='-i':index+=2;continue
                if token.startswith('-D'):index+=1;continue
                flags.append(token);index+=1
            obj=directory/'compiled.o';command=[str(compiler),*flags,'-c',str(path),'-o',str(obj)];compiled=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
            item=dict(referenceFunction=name,address=row['address'],bytes=row['bytes'],source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),headers=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in headers],selection=selection,compiler=probe['compiler'],compilerFlags=flags,command=command,exitCode=compiled.returncode,stdout=compiled.stdout,stderr=compiled.stderr,sourceCredit=0)
            if compiled.returncode==0:item.update(object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj))
            results.append(item);print(name,compiled.returncode,selection.get('forbiddenTokens'),flush=True)
        except Exception as error:results.append(dict(referenceFunction=name,address=row['address'],failure=str(error),sourceCredit=0));print(name,'ERROR',str(error),flush=True)
    write_json(LANE/'closed-reference-probes.json',dict(status='unadopted-closed-source-investigation',referenceOriginalSha256=sha256(reference),preprocessed=dict(path=expanded.relative_to(ROOT).as_posix(),sha256=sha256(expanded)),results=results,sourceCredit=0))


if __name__=='__main__':main()
