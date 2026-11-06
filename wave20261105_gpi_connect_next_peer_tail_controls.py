from wave20261105_gpi_connect_next_peer_tail_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import copy
import hashlib
import struct
from project import read_json
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peer_tail_compiler import COMPILER
from wave20261105_gpi_connect_next_peer_tail_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/peer-tail'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/peer-tail/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(GPIConnection)==0x600','(u32)&((GPIConnection*)0)->peerList==0x5d4','sizeof(GPIPeer)==80','(u32)&((GPIPeer*)0)->inputBuffer==28','(u32)&((GPIPeer*)0)->outputBuffer==44','(u32)&((GPIPeer*)0)->messages==60','sizeof(GPIMessage)==24']
    if int(row['address'],0)==0x20b0600:checks+=['sizeof(GPITransferID)==12','(u32)&((GPITransferID*)0)->profileid==0','(u32)&((GPITransferID*)0)->count==4','(u32)&((GPITransferID*)0)->time==8']
    if int(row['address'],0)==0x20b06d0:checks+=['GPI_READ_SIZE==2048']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('unsigned short port;','u32 wrongExtra;unsigned short port;',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def validate_growth(proof,row,image):
    if proof['caller']!=row['address'] or row['address']!='0x20b06d0' or proof['nativeSha256']!=row['targetSha256']:raise ValueError('Exact original growth caller/body identity differs')
    a=int(row['address'],0)-0x2000000
    if hashlib.sha256(image[a:a+row['bytes']]).hexdigest()!=row['targetSha256'] or (proof['value'],proof['start'])!=(2048,'0x20b0712'):raise ValueError('Original growth body/origin/value differs')
    raw=bytes.fromhex(proof['bytes'])
    if len(raw)!=4 or raw!=image[0xb0712:0xb0716]:raise ValueError('Actual original growth instructions differ')
    move,shift=struct.unpack('<HH',raw)
    if move!=0x2002 or shift!=0x0280 or (move&255)<<((shift>>6)&31)!=2048:raise ValueError('Native movsR0,2;lslsR0,R0,10 construction differs')
    return dict(status='passed',nativeOnlyProof=proof,payloadOrAllocatorExecutions=0,storageCredit=0)


def growth_controls(row):
    proof=read_json(LANE/'native-growth-proof.json');image=(ROOT/'extract/arm9/arm9.bin').read_bytes();positive=validate_growth(proof,row,image);negatives=[]
    for label,change in [('modern16384',lambda p:p.update(value=16384)),('wrong-origin',lambda p:p.update(start='0x20b0714')),('wrong-shift',lambda p:p.update(bytes='0220c002')),('wrong-caller',lambda p:p.update(caller='0x20b0600'))]:
        wrong=copy.deepcopy(proof);change(wrong)
        try:validate_growth(wrong,row,image)
        except ValueError as error:negatives.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong native growth proof accepted')
    return dict(status='passed',positive=positive,negativeControls=negatives)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeGrowth=growth_controls(next(r for r in rows if int(r['address'],0)==0x20b06d0)),nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
