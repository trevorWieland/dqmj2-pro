import os
import re
import subprocess
from project import ROOT,write_json,sha256
import match_runtime as C
from slice_reference_sdk_entities_v3_20261102 import functions,slice_closed
from wave20261102_child_fourth_types import write_closed

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large'
WORK=ROOT/'work/w5mg/closed'
SELECTION={'strtoul.c':[0x201ed2c,0x201f114,0x201f1ac],'wformat.c':[0x201f838,0x2020120,0x2020244],'wide.c':[0x2021294],'wide-post.c':[0x20212c4]}

def main():
    rows=[];compiler=C.COMPILER;flags=[*C.FLAGS,'-O4,p','-ipa','file','-inline','on,noauto','-lang','c99'];WORK.mkdir(parents=True,exist_ok=True)
    for filename,addresses in SELECTION.items():
        source=ROOT/'work/w5mg/candidates'/filename;expanded=WORK/(source.stem+'.i');process=subprocess.run([str(compiler),*flags,'-E',str(source),'-o',str(expanded)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
        if process.returncode:raise ValueError((process.stdout,process.stderr))
        original=expanded.read_text()
        for address in addresses:
            name='native_main_'+format(address,'08x');text=original
            for f in sorted(functions(text),key=lambda f:f['start'],reverse=True):
                if f['name']==name or re.search(r'\binline\b',text[f['start']:f['opening']]):continue
                text=text[:f['start']]+re.sub(r'\bstatic\s+','',text[f['start']:f['opening']]).rstrip()+';\n'+text[f['end']:]
            text,closed=slice_closed(text,[name]);path=WORK/format(address,'08x')/(format(address,'08x')+'.c');headers=write_closed(text,name,path)
            for h in headers:
                if len(h.read_text().splitlines())>500:h.write_text('\n'.join(s for s in h.read_text().splitlines() if s.strip())+'\n')
            rows.append(dict(address=hex(address),source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in headers],closedSelection=closed,sourceCredit=0));print(hex(address),flush=True)
    write_json(LANE/'closed-source-inputs.json',dict(results=rows,sourceCredit=0))

if __name__=='__main__':main()
