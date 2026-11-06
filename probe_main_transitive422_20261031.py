import json
from pathlib import Path
import match_runtime as c
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
DEFINITIONS=ROOT/'evidence/attempts/main-transitive422-definitions-20261031.json'
CHECKS=[(0x0202A450,'mov','r5, r1'),(0x0202A454,'bl','#0x202a37c'),(0x0202A3BC,'ldr','r0, [r4, #0x10]'),(0x0202A3C0,'bl','#0x202b334'),(0x0202B344,'cmp','r2, #0'),(0x0202B34C,'blt','#0x202b358'),(0x0202B350,'bl','#0x202b044'),(0x0202B358,'rsb','r2, r2, #0'),(0x0202B35C,'bl','#0x202b0f8'),(0x02042FF0,'bl','#0x203cc2c'),(0x0203CC2C,'ldr','ip, [pc, #4]'),(0x0203CC30,'mov','r2, #0'),(0x0203CC34,'bx','ip'),(0x0203CB90,'mov','r5, r0'),(0x0203CB94,'mov','r4, r1'),(0x0203CBA0,'bl','#0x202a8e0'),(0x0203CBB0,'cmp','r4, r0'),(0x0203CBC8,'mov','r0, r4'),(0x0203CBD8,'bl','#0x202a37c')]


def run():
    definitions=json.loads(DEFINITIONS.read_text());metadata,image,symbols=measured_module('main')
    if metadata['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('Transitive422 measured build changed')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);checks=[]
    for address,mnemonic,operands in CHECKS:
        raw=image[address-0x02000000:address-0x02000000+4];instruction=next(decoder.disasm(raw,address))
        if(instruction.mnemonic,instruction.op_str)!=(mnemonic,operands):raise ValueError('Transitive422 instruction/edge check differs')
        checks.append(dict(address=hex(address),bytesHex=raw.hex(),mnemonic=mnemonic,operands=operands))
    if int.from_bytes(image[0x3CC38:0x3CC3C],'little')!=0x0203CB8C:raise ValueError('Transitive422 literal dispatch target differs')
    functions=[]
    for address in definitions['functionAddresses']:
        line=next(x for x in symbols.splitlines()if('addr:0x%08x'%address)in x.lower());size=int(line.split('size=')[1].split(')')[0],0)
        if 'function(arm,'not in line:raise ValueError('Transitive422 native mode differs')
        functions.append(dict(processor='arm9',program='',module='main',mode='arm',address=hex(address),bytes=size,nativeSpanSha256=c.sha(image[address-0x02000000:address-0x02000000+size])))
    caller=definitions['caller'];callerMeta,callerImage,unused=measured_module(caller['module']);offset=caller['address']-0x021D7240
    snapshot=ROOT/'evidence/verification/accepted-cohort95-identities-v2-20261031.json';selected=json.loads(snapshot.read_text())['functions']
    sourceviews=[row for row in selected if row['processor']=='arm9'and row['module']=='main'and row['address']in[0x0202A44C,0x02042FEC]]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],evidenceClass='native-static-transitive-input',sourceCredit=0,originalNativeExecutions=0,moduleSha256=metadata['sha256'],functions=functions,observedCaller=dict(processor='arm9',program='',module=caller['module'],mode='arm',address=hex(caller['address']),bytes=caller['bytes'],moduleSha256=callerMeta['sha256'],nativeSpanSha256=c.sha(callerImage[offset:offset+caller['bytes']])),chains=definitions['chains'],acceptedSourceViewsForProvenanceOnly=sourceviews,acceptedSnapshotSha256=sha256(snapshot),limits=definitions['limits'],checkedInstructions=checks,definitionsSha256=sha256(DEFINITIONS),generatorSha256=sha256(__file__),reproductionCommand='python probe_main_transitive422_20261031.py',negativeControls=[dict(name='different-tail-target',rejected=int.from_bytes(image[0x3CC38:0x3CC3C],'little')!=0x0203CB8D),dict(name='different-R2-condition',rejected=next(decoder.disasm(image[0x2B344:0x2B348],0x0202B344)).op_str!='r1, #0')])
    if not all(control['rejected']for control in report['negativeControls']):raise ValueError('Transitive422 static control failed')
    write_json(ROOT/'evidence/verification/main-transitive-inputs422-20261031.json',report)
    print(json.dumps(dict(chains=2,checkedInstructions=len(checks),nativeExecutions=0,sourceCredit=0)))

if __name__=='__main__':run()
