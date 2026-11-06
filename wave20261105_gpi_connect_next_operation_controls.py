from wave20261105_gpi_connect_next_operation_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256,read_json
import hashlib
import struct
import copy
from wave20261105_gpi_connect_next_operation_compiler import COMPILER
from wave20261105_gpi_connect_next_operation_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/operation'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/operation/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4',  'sizeof(GPIOperation)==36', '(u32)&((GPIOperation*)0)->type==0', '(u32)&((GPIOperation*)0)->result==28', '(u32)&((GPIConnection*)0)->connectState==0x1f4', '(u32)&((GPIConnection*)0)->firewall==0x10c', '(u32)&((GPIConnection*)0)->nick==0x110', '(u32)&((GPIConnection*)0)->password==0x177', 'sizeof(GPIConnectData)==776', '(u32)&((GPIConnectData*)0)->newuser==772', 'GPI_NOT_CONNECTED==0', 'GPI_DISCONNECTED==4', 'GS_WIRELESS_DEVICE==1']
    extended=row['address']=='0x20ad63c'
    checks+=['sizeof(GPIConnection)==0x610','(u32)&((GPIConnection*)0)->productID==0x608','(u32)&((GPIConnection*)0)->namespaceID==0x60c'] if extended else ['sizeof(GPIConnection)==0x5d8']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('opaqueSuffix[48]','opaqueSuffix[52]',1) if extended else text.replace('GPIBool blocking;','GPIBool wrongPrefix;GPIBool blocking;',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def validate_suffix(proof,image,row):
    if proof['caller']!=row['address'] or row['address']!='0x20ad63c' or (row.get('program') or '',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb'):raise ValueError('Scoped suffix caller namespace/mode differs')
    start=int(row['address'],0)-0x2000000
    if proof['nativeSha256']!=row['targetSha256'] or hashlib.sha256(image[start:start+row['bytes']]).hexdigest()!=row['targetSha256']:raise ValueError('Scoped suffix full native body differs')
    expected=[('productID',0x608,0x20ad800,0x20ad6cc,0x20ad6c6),('namespaceID',0x60c,0x20ad810,0x20ad706,0x20ad700)]
    if len(proof['fields'])!=2 or proof['minimumViewBytes']!=0x610:raise ValueError('Scoped suffix exact fieldset differs')
    for field,(name,offset,pool,load,origin) in zip(proof['fields'],expected):
        if (field['name'],field['offset'],int(field['offsetPool'],0),int(field['loadInstruction'],0),field['originalLoadBytes'])!=(name,offset,pool,load,'a258'):raise ValueError('Scoped suffix field/offset/instruction contract differs')
        encoded=struct.unpack('<H',image[origin-0x2000000:origin-0x2000000+2])[0]
        if encoded&0xf800!=0x4800 or (encoded>>8)&7!=2 or ((origin+4)&~3)+(encoded&255)*4!=pool or struct.unpack('<I',image[pool-0x2000000:pool-0x2000000+4])[0]!=offset or image[load-0x2000000:load-0x2000000+2].hex()!='a258':raise ValueError('Scoped suffix actual original constant-pool/load differs')
    return dict(status='passed',caller=row['address'],fields=proof['fields'],minimumViewBytes=0x610,objectStorageExtentAuthorshipCredit=0)


def suffix_controls(rows):
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();proof=read_json(LANE/'suffix-native-proof.json');row=next(r for r in rows if r['address']=='0x20ad63c');positive=validate_suffix(proof,image,row);negative=[]
    for label,change in [('wrong-field-offset',lambda p:p['fields'][0].update(offset=0x60c)),('wrong-field-origin',lambda p:p['fields'][0].update(offsetPool='0x20ad804')),('wrong-load-instruction',lambda p:p['fields'][1].update(originalLoadBytes='0000')),('wrong-caller',lambda p:p.update(caller='0x20ad144')),('wrong-view-extent',lambda p:p.update(minimumViewBytes=0x614))]:
        bad=copy.deepcopy(proof);change(bad)
        try:validate_suffix(bad,image,row)
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong native suffix proof accepted')
    return dict(status='passed',positive=positive,negativeControls=negative,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',nativeSuffix=suffix_controls(rows),actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
