from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    base = ROOT / 'audit_child_third_eligibility_parallel_wave20261102.py'
    if sha256(base) != '3f6024b5307cb26658ea20a22c517cd51da3f623af00104e0a2dd61e70f4d9cf':
        raise ValueError('Frozen child-third auditor changed')
    text = base.read_text()
    text = text.replace('utility-child-third', 'utility-child-fourth')
    text = text.replace("'arm9'", "'arm7'")
    text = text.replace('== 36 and ready[\'bytes\']', "== 19 and ready['bytes']")
    text = text.replace('== 4458', '== 7104').replace('sealed36/4458', 'sealed19/7104')
    text = text.replace('functions=36, bytes=4458', 'functions=19, bytes=7104')
    text = text.replace("['ov006', 'main-sdk-next', 'main-sdk-second']", "['ov006', 'main-sdk-next', 'main-sdk-second', 'main-sdk-third', 'utility-child-third']")
    start = text.index("    controls = read_json(lane / 'native-callee-binding-controls.json')")
    end = text.index('    reserved_map = ', start)
    controls = '''    controls = read_json(lane / 'whole-c-controls.json')
    wrong = ROOT / controls['wrongSource']
    wrong_body = ROOT / 'work/parallel-wave20261102/utility-child-fourth/controls-wrong-link/caller.bin'
    check(controls['positiveWholeCExact'] and controls['positiveRealLink']['exactCallerBytes'], 'Positive whole-C genuine link control')
    check(sha256(wrong) == controls['wrongSourceSha256'] and controls['wrongCompilerResult']['compiledBytes'] == controls['wrongGenuinelyLinkedBytes'] == 48 and controls['wrongRealLinkAttempt']['exitCode'] == 0, 'Complete same-extent wrong-C compile and successful genuine linker')
    check(sha256(wrong_body) == controls['wrongLinkedSha256'] and controls['wrongLinkedSha256'] != controls['originalNativeSha256'] and controls['wrongLinkedMatchingBytes'] == 46 and controls['wholeCNegativeControlsRejected'] == 1, 'Typed size+2 to size+3 mutation rejected by full native equality')
    check(not copied['arm9InventoryPresent'] and not copied['arm9StartupReportPresent'] and copied['immutableExternalInputMutationRejected'] and copied['compilerObjectsUnchangedByRejectedInventory'], 'Cold copied-root absence of ARM9/startup and precompile wrong-inventory rejection')
'''
    text = text[:start] + controls + text[end:]
    start = text.index('    root_descriptor = ')
    end = text.index('    check(all(sha256(ROOT / name)', start)
    inputs = '''    descriptor = read_json(lane / 'canonical-packet.json')
    mandatory = inputs['mandatoryExternalInputs']
    inventory_inputs = [pin['path'] for pin in mandatory]
    check(set(inventory_inputs) == {'evidence/utility/ghidra-arm7.json', 'project.json'} and all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in mandatory), 'Exact immutable ARM7-only configuration inputs')
    check(not inputs['arm9StartupAssociationReportRequired'], 'No unnecessary ARM9 startup dependency')
    missing_inputs = []
'''
    text = text[:start] + inputs + text[end:]
    text = text.replace('wholeCWrongBodyControls=0', 'wholeCWrongBodyControls=1').replace('entryQualificationNegativeControls=5', 'entryQualificationNegativeControls=0')
    text = text.replace('noWholeCOrBehaviorControlClaim=True', 'independentBehaviorExecutionCredit=0')
    text = text.replace("producedReportDependency='evidence/matches/utility-arm9-startup01.json'", "producedReportDependency=None")
    text = text.replace("child-third-eligibility-", "child-fourth-eligibility-")
    exec(compile(text, str(base), 'exec'), dict(__name__='__main__', __file__=str(base)))
    output = ROOT / 'evidence/verification/parallel-wave20261102/child-fourth-eligibility-initial.json'
    result = read_json(output)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)), frozenBaseAuditorSha256=sha256(base),
        requiredNextRootDescriptorFrozenInputs=read_json(ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-fourth/packet-ready-inputs.json')['mandatoryExternalInputs'],
        arm9InventoryOrStartupDependencyRequired=False, sourceCredit=0)
    write_json(output, result)


if __name__ == '__main__':
    main()
