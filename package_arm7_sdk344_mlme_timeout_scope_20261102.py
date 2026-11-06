import ast
import json
from pathlib import Path
import subprocess
from project import ROOT,sha256,write_json

def main():
    names={'prove_arm7_sdk340_mlme_timeout_callback_scope_20261102.py','validate_arm7_sdk341_mlme_timeout_scope_20261102.py','probe_arm7_sdk342_mlme_timeout_installation_20261102.py',Path(__file__).name,'evidence/attempts/arm7-sdk340-mlme-timeout-callback-scope-20261102.json','evidence/attempts/arm7-sdk342-mlme-timeout-installation-20261102.json','evidence/attempts/arm7-sdk342-initial-incomplete-request-context-20261102.json','evidence/attempts/arm7-sdk342-missing-original-heap-context-20261102.json','evidence/verification/arm7-sdk341-mlme-timeout-scope-controls-20261102.json','docs/2026-11-02-arm7-mlme-timeout-callback-scope.md'};pins={};todo=[n for n in names if n.endswith('.py')];seen=set()
    while todo:
        name=todo.pop()
        if name in seen:continue
        seen.add(name)
        for node in ast.walk(ast.parse((ROOT/name).read_text(encoding='utf-8-sig'))):
            modules=[a.name for a in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
            for module in modules:
                p=module.split('.')[0]+'.py'
                if(ROOT/p).is_file():
                    if p not in names:pins[p]=sha256(ROOT/p)
                    todo.append(p)
    for n in pins.copy():
        if subprocess.run(['git','cat-file','-e','HEAD:'+n],cwd=ROOT,capture_output=True).returncode:names.add(n);pins.pop(n)
    for n in ['project.json','inputs/game.nds','extract/arm7/arm7.bin','extract/arm7/runtime/arm7-main.bin','extract/arm7/runtime/arm7-wram.bin','evidence/arm7/ghidra-runtime-inventory.json']:
        if not(ROOT/n).is_file():
            if n=='inputs/game.nds':
                from project import configuration
                n=configuration()['rom'].relative_to(ROOT).as_posix()
            else:raise ValueError('Missing required scoped input:'+n)
        pins[n]=sha256(ROOT/n)
    prefix='deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/'
    for n in ['libraries/wl_arm7/src/MLME.c','libraries/wl_arm7/src/WlNic.c','libraries/wl_arm7/include/WlNic.h']:pins[prefix+n]=sha256(ROOT/(prefix+n))
    for n in names:
        if n.startswith('work/')or not(ROOT/n).is_file():raise ValueError('Only source/docs/evidence in scope transport')
        pins.pop(n,None)
    report=json.loads((ROOT/'evidence/verification/arm7-sdk341-mlme-timeout-scope-controls-20261102.json').read_text())
    if report['negativeControlCount']!=32 or not report['allRejected']:raise ValueError('Complete controls required')
    output=ROOT/'provenance/arm7-sdk344-mlme-timeout-scope-handoff-20261102.json';write_json(output,dict(command='python validate_arm7_sdk341_mlme_timeout_scope_20261102.py',files=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],existingPins=[dict(path=n,sha256=h)for n,h in sorted(pins.items())],callbackScope=report['positive'],sourceCredit=0,initializedDenominatorIncrease=0,assemblyJustification=False,referenceCommit='ccbbcc8b6db4c4dbba3d503d2026978d78977840',referenceRevisionEquivalenceUnproved=True,defaultNamespaceAndDataGuardsChanged=False,isolatedParentCwdReportsSha256=['43b1318a7ba6a6f659053d26829434c2902fae9900a231bf804204774a5a443b','22b94b1a3daaca8adafc194a8adafdb485d55095f52ae6a812833e341fbc8ebb','201550901a426a06ff968ab31649889c3fe20e5c3a1cac0e4246a7359e0037c9'],allReportsRegenerateWithoutCachedProducts=True,sharedConfigurationRegistryLedgerOrPriorSourcesChanged=False));print(json.dumps(dict(path=output.relative_to(ROOT).as_posix(),sha256=sha256(output),files=len(names),pins=len(pins))),flush=True)

if __name__=='__main__':main()
