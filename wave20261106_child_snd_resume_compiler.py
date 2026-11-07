from pathlib import Path
import utility_code
import match_lowlevel
from project import ROOT,read_json,sha256
from wave20261106_child_snd_resume_paths import SOURCE,EVIDENCE,WORK,assert_compile

COMPILER='tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_SHA='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
EXTRA=['-O4,p','-ipa','file','-inline','on,noauto','-lang','c99']


def specification():
    claim=read_json(EVIDENCE/'claim.json');entry=claim['claimedFunctions'][0]
    if len(claim['claimedFunctions'])!=1 or(entry['program'],entry['processor'],entry['module'],entry['mode'],entry['address'],entry['bytes'])!=('dwc/utility.bin/move/child.srl','arm9','utility-child-arm9-main','arm','0x2006eb8',196):raise ValueError('Exact admitted source identity differs')
    return dict(entry,address=int(entry['address'],0),base=int(entry['base']),name='native_utility_child_arm9_main_02006eb8',inputModuleSha256='af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0',compilerPath=COMPILER)


def compare(source,directory):
    source=Path(source);directory=Path(directory);assert_compile(source,directory)
    if sha256(ROOT/COMPILER)!=COMPILER_SHA:raise ValueError('Accepted source compiler changed')
    previous_work=utility_code.WORK;previous_flags=match_lowlevel.FLAGS
    try:
        utility_code.WORK=directory;match_lowlevel.FLAGS=[*previous_flags,*EXTRA]
        row,output=utility_code.compile_compare(source,specification(),2,'off',False)
    finally:utility_code.WORK=previous_work;match_lowlevel.FLAGS=previous_flags
    if row.get('compileFailed'):return row,output
    row.update(compilerPath=row['compiler'],sourceDependencies=[dict(path=(source.parent/'context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.parent/'context.h'))])
    return row,output
