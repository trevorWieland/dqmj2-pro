from wave20261105_gpi_connect_next_disconnect_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import copy
import hashlib
from project import read_json
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_disconnect_compiler import COMPILER
from wave20261105_gpi_connect_next_disconnect_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/disconnect'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/disconnect/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(GPIConnection)==0x600','sizeof(GPIProfileList)==12','(u32)&((GPIConnection*)0)->peerList==0x5d4','(u32)&((GPIConnection*)0)->updateproBuffer==0x5e0','(u32)&((GPIConnection*)0)->updateuiBuffer==0x5f0','(u32)&((GPIConnection*)0)->connectState==0x1f4','(u32)&((GPIConnection*)0)->userid==0x19c','(u32)&((GPIConnection*)0)->profileid==0x1a0','(u32)&((GPIConnection*)0)->outputBuffer==0x210','sizeof(GPIPeer)==80','(u32)&((GPIPeer*)0)->pnext==76']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('callbackSlots[2]','callbackSlots[3]',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def validate_flow(proof,row,image):
    if proof['caller']!=row['address'] or row['address']!='0x20ade3c' or proof['nativeSha256']!=row['targetSha256']:raise ValueError('Exact disconnect flow caller differs')
    a=int(row['address'],0)-0x2000000
    if hashlib.sha256(image[a:a+row['bytes']]).hexdigest()!=row['targetSha256']:raise ValueError('Original disconnect body differs')
    if (proof['preUDPBlockStart'],proof['preUDPProvider'],proof['notConnectedBranchTarget'],proof['preUDPClearOffsets'])!=('0x20adec6','0x20a99c0','0x20adeda',[0x1f4,0x19c,0x1a0]):raise ValueError('Exact partial block/branch/field contract differs')
    expected=[0x20ade52,0x20adec6,0x20adecc,0x20aded4,0x20aded8,0x20adeda,0x20adf7a]
    if len(proof['instructions'])!=len(expected):raise ValueError('Exact flow instruction set differs')
    md=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for item,at in zip(proof['instructions'],expected):
        raw=bytes.fromhex(item['bytes']);decoded=list(md.disasm(raw,at))
        if int(item['address'],0)!=at or image[at-0x2000000:at-0x2000000+len(raw)]!=raw or len(decoded)!=1 or decoded[0].mnemonic+' '+decoded[0].op_str!=item['instruction']:raise ValueError('Original flow instruction/pool/target differs')
    if proof['instructions'][0]['instruction']!='beq #0x20adeda' or proof['instructions'][5]['instruction']!='bl #0x20a99c0' or proof['instructions'][6]['instruction']!='ldr r6, [r6, #0x4c]':raise ValueError('Actual original branch/provider/next-field differs')
    return dict(status='passed',proof=proof,internalBlockIsNotNewFunctionEntry=True,sourceCredit=0)


def flow_controls(row):
    proof=read_json(LANE/'native-flow-proof.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();positive=validate_flow(proof,row,image);negative=[]
    for label,change in [('wrong-caller',lambda x:x.update(caller='0x20ade40')),('wrong-block-start',lambda x:x.update(preUDPBlockStart='0x20adec8')),('wrong-branch',lambda x:x.update(notConnectedBranchTarget='0x20adf00')),('wrong-fields',lambda x:x.update(preUDPClearOffsets=[0x1f4,0x19c,0x1a4])),('wrong-instruction',lambda x:x['instructions'][0].update(bytes='0000'))]:
        bad=copy.deepcopy(proof);change(bad)
        try:validate_flow(bad,row,image)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original flow proof admitted')
    altered=bytearray(image);altered[0xadec6]^=1
    try:validate_flow(proof,row,bytes(altered))
    except ValueError as error:negative.append(dict(case='changed-native-body',rejected=True,reason=str(error)))
    else:raise ValueError('Changed original flow body admitted')
    return dict(status='passed',positive=positive,negativeControls=negative)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeFlow=flow_controls(rows[0]),nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
