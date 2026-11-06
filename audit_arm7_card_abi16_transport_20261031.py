import ast
import json
from pathlib import Path
import re
from project import ROOT,sha256,write_json
MANIFEST='provenance/arm7-lane-card-abi16-1252-handoff-20261031.json'
MANIFEST_SHA='8cbcfb9a89f66309b7ab3df7a5b9f25799f0047206e97c6aab51666c8f6e45c4'
OLD188_HELPERS=('arm7_lane_card_init_native_20261031.py','arm7_lane_card_init_oracle_20261031.py')


def imports(roots):
    files=set();pending=list(roots)
    while pending:
        name=pending.pop()
        if name in files:continue
        files.add(name)
        for node in ast.walk(ast.parse((ROOT/name).read_text(encoding='utf-8'))):
            modules=[a.name for a in node.names] if isinstance(node,ast.Import) else ([node.module] if isinstance(node,ast.ImportFrom) and node.module else [])
            for module in modules:
                relative=module.replace('.','/')+'.py'
                if (ROOT/relative).is_file() and relative not in files:pending.append(relative)
    return files


def includes(source):
    found=set();pending=[source]
    while pending:
        path=pending.pop()
        for name in re.findall(r'^#include "([^"<>]+)"',path.read_text(),re.M):
            target=(path.parent/name).resolve()
            if not target.is_relative_to((ROOT/'src/arm7/lane_20261031_card_abi16').resolve()):raise ValueError('Shared C include escaped explicit family')
            relative=target.relative_to(ROOT).as_posix()
            if relative not in found:found.add(relative);pending.append(target)
    return found


def main():
    if sha256(ROOT/MANIFEST)!=MANIFEST_SHA:raise ValueError('Original42-path transport manifest changed')
    publication=json.loads((ROOT/MANIFEST).read_text());published={r['path'] for r in publication['files']}
    profile=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final/closure.json').read_text())
    runtime_pins=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final/generator-pins.json').read_text())['files']
    required=imports(['match_arm7_lane_card_abi16_20261031.py','validate_arm7_lane_card_abi16_20261031.py','prove_arm7_card_shared_layout_20261031.py'])
    covered={r['path'] for r in runtime_pins}|published
    if required-covered:raise ValueError('Recursive Python dependency lacks declared pin/transport: '+str(sorted(required-covered)))
    for row in runtime_pins:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen recursive source dependency changed')
    cpp=[]
    for row in profile['matches']:
        actual=includes(ROOT/row['source']);declared={r['path'] for r in row['sourceDependencies']}
        if actual!=declared or not actual<=published:raise ValueError('Actual recursive C include transport differs')
        cpp.append(dict(address=row['address'],source=row['source'],sourceSha256=sha256(ROOT/row['source']),actualIncludes=sorted(actual),complete=True))
    static=set([MANIFEST,'provenance/arm7-lane-card-callback-scope-handoff-20261031.json',
        'provenance/arm7-lane-card-callback-scope-runtime-pins-20261031.json','evidence/arm7/lane-card-callback-scope-20261031.json',
        'evidence/arm7/ghidra-runtime-inventory.json','evidence/arm7/runtime-layout.json',
        'extract/arm7/arm7.bin','extract/arm7/runtime/arm7-wram.bin','extract/arm7/runtime/arm7-main.bin',
        'inputs/game.nds','tools/mwccarm/mwccarm/2.0/base/mwccarm.exe','tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'])
    static.update(r['path'] for row in profile['matches'] for r in row['sourceDependencies'])
    receiver=Path(r'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp')
    current=[]
    for name in sorted({r['path'] for r in runtime_pins}|required|static):
        if not (ROOT/name).is_file():raise ValueError('Explicit static/runtime dependency missing from lane: '+name)
        target=receiver/name
        current.append(dict(path=name,sha256=sha256(ROOT/name),receiverExists=target.is_file(),receiverMatches=target.is_file() and sha256(target)==sha256(ROOT/name),includedInOriginalPublication=name in published))
    if any(name in published for name in OLD188_HELPERS):raise ValueError('Supplement unexpectedly duplicates original publication payload')
    report=ROOT/'evidence/verification/arm7-card-abi16-transport-audit-20261031.json'
    write_json(report,dict(generator='audit_arm7_card_abi16_transport_20261031.py',generatorSha256=sha256(__file__),
        originalManifest=dict(path=MANIFEST,sha256=MANIFEST_SHA,payloadPaths=len(published),unchanged=True),
        initialObservedReceiverFailure='ModuleNotFoundError: arm7_lane_card_init_oracle_20261031, before compilation',
        missingOnlyOld188Supplement=[dict(path=name,sha256=sha256(ROOT/name)) for name in OLD188_HELPERS],
        recursivePythonFiles=sorted(required),pinnedRuntimePaths=len(runtime_pins),recursiveCUnits=cpp,staticAndRuntimeReceiverAudit=current,
        noRequiredScratchCompilerInput=True,originalExecutableCompilerInput=False,newSourceCredit=0,acceptedInputsChanged=False,
        limitations=['Receiver audit reflects current read-only state after coordinator began importing frozen old188 helpers; the initial failure is preserved separately',
            'Only two original188 Python helpers are added for receivers lacking that packet; old12-byte C/header sources are not transported or adopted by the supplement',
            'Private original images/compiler files and native packages remain explicitly configured existing inputs; generated Work products rebuild from source',
            'License-file setup remains repository-local and unchanged; contents are never included in transport or diagnostic output']))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),runtimePins=len(runtime_pins),recursivePythonFiles=len(required),cUnits=len(cpp),supplementFiles=2,receiverMissingOrDifferent=sum(not r['receiverMatches'] for r in current)))


if __name__=='__main__':main()
