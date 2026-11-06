import os
import re
import subprocess
from project import ROOT,read_json,write_json,sha256
from slice_reference_sdk_entities_v3_20261102 import functions,slice_closed
from wave20261102_child_fourth_types import write_closed,units

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later/more'
WORK=ROOT/'work/w5ml/more/closed'

def main():
    reports=read_json(LANE/'reference-probes.json')['results'];originals={int(m[1],16):m[2] for line in (ROOT/'config/arm9/relocs.txt').read_text().splitlines() if (m:=re.fullmatch(r'from:0x([0-9a-f]+) kind:arm_call to:0x([0-9a-f]+) module:main',line))};results=[]
    for probe in reports:
        matches=probe['normalizedMatches']
        if not matches:continue
        compiler=ROOT/probe['compiler'];directory=WORK/(ROOT/probe['referenceSource']).stem;directory.mkdir(parents=True,exist_ok=True);expanded=directory/'expanded.i';command=[str(compiler),*probe['compilerFlags'],'-E',str(ROOT/probe['referenceSource']),'-o',str(expanded)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if process.returncode:raise ValueError((process.stdout,process.stderr))
        original=expanded.read_text()
        for item in matches:
            name=item['referenceFunction'];address=int(item['address'],0);primary='native_main_'+format(address,'08x');text=original
            for fn in sorted(functions(text),key=lambda f:f['start'],reverse=True):
                header=text[fn['start']:fn['opening']]
                if fn['name']==name:text=text[:fn['start']]+re.sub(r'\bstatic\s+','',header)+text[fn['opening']:];continue
                if re.search(r'\binline\b',header):continue
                text=text[:fn['start']]+re.sub(r'\bstatic\s+','',header).rstrip()+';\n'+text[fn['end']:]
            text,selection=slice_closed(text,[name]);text=re.sub(r'\bstatic\s+(?=[^;{}]*\b'+re.escape(name)+r'\s*\()', '', text)
            replacements={rel['symbol']:'native_fn_'+originals[address+rel['offset']] for rel in item['relocations'] if rel['type']==1 and not rel['symbol'].startswith('_')}
            replacements.update(BeginSleep='native_fn_0203ba70',EndSleep='native_fn_0203babc',ResetTaskQueue_='native_fn_0203c388',sStrmChannel='native_data_020f5b4c',sStrmList='native_data_020f5b00',s_VramTransferManager='native_data_020f5bdc',bInitialized='native_data_020f5afc')
            declarations={'sStrmChannel':'extern NNSSndStrmChannel native_data_020f5b4c[16];','sStrmList':'extern NNSFndList native_data_020f5b00;','s_VramTransferManager':'extern NNSGfdVramTransferManager native_data_020f5bdc;'};pieces=[]
            for entity_name,entity in units(text):
                handled=False
                if entity_name is None:
                    for symbol,decl in declarations.items():
                        if re.search(r'\bstatic\b[\s\S]*\b'+symbol+r'\s*(?:\[|;|=)',entity):pieces.append(decl+'\n');handled=True;break
                if handled:continue
                if entity_name==name:
                    if 'bInitialized' in entity:pieces.append('extern BOOL native_data_020f5afc;\n');entity=re.sub(r'\bstatic\s+BOOL\s+bInitialized\s*=\s*(?:0|FALSE)\s*;','',entity)
                    if re.search(r'static\s+void\s*\*\s*buffer\s*\[',entity):pieces.append('extern void *native_data_020f5b0c[16];\n');entity=re.sub(r'static\s+void\s*\*\s*buffer\s*\[[^\]]+\]\s*;','',entity);entity=re.sub(r'(?<!\.)\bbuffer\b','native_data_020f5b0c',entity)
                entity=re.sub(r'\b'+re.escape(name)+r'\b',primary,entity);tokens={k:v for k,v in replacements.items() if k!=name};entity=re.sub(r'\b(?:'+'|'.join(re.escape(k) for k in sorted(tokens,key=len,reverse=True))+r')\b',lambda m:tokens[m[0]],entity);pieces.append(entity)
            path=directory/format(address,'08x')/(format(address,'08x')+'.c');headers=write_closed('\n'.join(pieces),primary,path)
            for header in headers:
                if len(header.read_text().splitlines())>500:header.write_text('\n'.join(line for line in header.read_text().splitlines() if line.strip())+'\n')
            results.append(dict(referenceFunction=name,address=item['address'],bytes=item['bytes'],source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in headers],referenceSource=probe['referenceSource'],selection=selection,sourceCredit=0));print(name,path.relative_to(ROOT),flush=True)
    write_json(LANE/'closed-source-inputs.json',dict(results=results,sourceCredit=0))

if __name__=='__main__':main()
