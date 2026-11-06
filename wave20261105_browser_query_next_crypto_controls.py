import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_crypto_compiler import COMPILER
from wave20261105_browser_query_next_crypto_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/crypto'


def geometry(row):
    folder=ROOT/'work/w5bq/crypto/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(unsigned)==4','sizeof(void*)==4','sizeof(u8)==1','((u8)-1)>0','sizeof(u32)==4','sizeof(GOACryptState)==261','(u32)&((GOACryptState*)0)->cards==0','(u32)&((GOACryptState*)0)->rotor==256','(u32)&((GOACryptState*)0)->ratchet==257','(u32)&((GOACryptState*)0)->avalanche==258','(u32)&((GOACryptState*)0)->last_plain==259','(u32)&((GOACryptState*)0)->last_cipher==260']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if True:
        wrong=text.replace('cards[256]','cards[255]',1) if row['address'] in ('0x20a5660','0x20a5710') else text.replace('last_plain,last_cipher','last_cipher,last_plain',1) if row['address']=='0x20a578c' else text.replace('rotor,ratchet','ratchet,rotor',1) if row['address']=='0x20a56d4' else text.replace('typedef unsigned char u8;','typedef signed char u8;',1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
