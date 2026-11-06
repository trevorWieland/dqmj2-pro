import gzip
import json
import re
import match_runtime as c
from project import ROOT,sha256,write_json
from link_runtime_unit import measured_module

def execute():
    main,arm,unused=measured_module('main');module,overlay,unused=measured_module('ov000');source=ROOT/'evidence/matches/ov000-20261101-controller764-functional-near.json';report=json.loads(source.read_text());artifact=ROOT/report['generatedTrace']['path']
    if sha256(artifact)!=report['generatedTrace']['sha256']:raise ValueError('764 constructor trace hash differs')
    traces=json.loads(gzip.decompress(artifact.read_bytes()));calls=[]
    for row in traces['cases']:
        if 'original'not in row:continue
        for entry in row['original']['calls']:
            if entry['entry']==0x0205FC10:calls.append(dict(profile=row['original']['profile']['name'],preparedWords=entry['preparedWords'],actualNativeCaller=True,calleeExecution='supplied boundary'))
    expected=[0x02245F74,0x0221930C,0x0221938C,0,18,8192,2,0]
    if not calls or any(row['preparedWords']!=expected for row in calls):raise ValueError('764 original constructor word view differs')
    text=(ROOT/'config/arm9/symbols.txt').read_text();line=next(line for line in text.splitlines()if line.endswith('addr:0x0205fc10'));size=int(re.search(r'size=(0x[0-9a-f]+)',line)[1],0)
    write_json(ROOT/'evidence/abi/ov000-controller764-constructor-eight-word-chain-20261101.json',dict(schemaVersion=1,romSha256=report['romSha256'],caller=dict(processor='arm9',program='',module='ov000',moduleSha256=module['sha256'],address='0x02218D30',mode='arm',bytes=1500,callPc='0x02218DCC',condition='entry state byte03==0 and supplied02214FF0 raw return==1',preparationRange=dict(address='0x02218DA0',bytes=48,sha256=c.sha(overlay[0x02218DA0-0x021D7240:0x02218DD0-0x021D7240]))),callee=dict(processor='arm9',program='',module='main',moduleSha256=main['sha256'],address='0x0205FC10',mode='arm',bytes=size,spanSha256=c.sha(arm[0x5FC10:0x5FC10+size]),entryFrameBytes=32,measuredStaticReads=[dict(entryWord=3,pc='0x0205FC30',operation='incomingR3 retained inR5 and forwarded asR2 at0205FC98'),dict(entryWord=4,pc='0x0205FC90',operation='LDRB entrySP+0'),dict(entryWord=5,pc='0x0205FC34',operation='LDR entrySP+4'),dict(entryWord=6,pc='0x0205FC48',operation='LDRSB entrySP+8 on zero entry-word7 branch; also read at0205FC5C/0205FC80'),dict(entryWord=7,pc='0x0205FC3C',operation='LDR entrySP+12 controls allocator-flag branch')]),callerPreparedWordView=expected,originalCallerObservations=calls,reconstructionView='u32(u32,u32,u32,u32,u32,u32,s32,u32) used only as this caller drafting/ABI view',sourceReport=dict(path=source.relative_to(ROOT).as_posix(),sha256=sha256(source)),reproduction=['python prove_ov000_controller764_20261101.py','python derive_ov000_controller764_abi_20261101.py'],sourceCredit=0,limits=['Original caller instructions execute; constructor function itself is supplied in the functional oracle. Static callee reads and downstream transfers are separate byte-qualified facts.','Live/transferred words do not establish original formal types,count or complete transitive semantic consumption. No shared catalogue/preference or accepted primary changes.','Raw seven-word M2C draft omitted incomingR3=0 and shifted all4 stack roles. Returning seven-word control is independently rejected.','Callback addresses remain module-qualified ARM entries; their behavior/signatures/lifecycle are not qualified by this boundary.']))
    print(dict(originalConstructorCalls=len(calls),preparedWords=8,sourceCredit=0),flush=True)

if __name__=='__main__':execute()
