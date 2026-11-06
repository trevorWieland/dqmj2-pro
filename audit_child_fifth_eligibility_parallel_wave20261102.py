from pathlib import Path
import sys
sys.dont_write_bytecode = True
from project import ROOT, read_json, write_json, sha256
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile


def main():
    base = ROOT / 'audit_child_third_eligibility_parallel_wave20261102.py'
    assert sha256(base) == '3f6024b5307cb26658ea20a22c517cd51da3f623af00104e0a2dd61e70f4d9cf'
    text = base.read_text().replace('utility-child-third', 'utility-child-fifth').replace("'arm9'", "'arm7'")
    text = text.replace('== 36 and ready[\'bytes\']', "== 25 and ready['bytes']").replace('== 4458', '== 6724')
    text = text.replace('sealed36/4458', 'sealed25/6724').replace('functions=36, bytes=4458', 'functions=25, bytes=6724')
    text = text.replace("['ov006', 'main-sdk-next', 'main-sdk-second']", "['ov006', 'main-sdk-next', 'main-sdk-second', 'main-sdk-third', 'utility-child-third', 'utility-child-fourth']")
    start = text.index("    controls = read_json(lane / 'native-callee-binding-controls.json')")
    end = text.index('    reserved_map = ', start)
    controls = '''    controls = read_json(lane / 'whole-c-controls.json')
    wrong = ROOT / controls['wrongSource']
    wrong_body = ROOT / 'work/parallel-wave20261102/utility-child-fifth/controls-wrong-link/caller.bin'
    check(controls['positiveWholeCExact'] and controls['positiveRealLink']['exactCallerBytes'], 'Positive whole-C genuine link control')
    check(sha256(wrong) == controls['wrongSourceSha256'] and controls['wrongCompilerResult']['compiledBytes'] == controls['wrongGenuinelyLinkedBytes'] == 52 and controls['wrongRealLinkAttempt']['exitCode'] == 0, 'Complete same-extent wrong-C compile and genuine link')
    check(sha256(wrong_body) == controls['wrongLinkedSha256'] and controls['wrongLinkedSha256'] != controls['originalNativeSha256'] and controls['wrongLinkedMatchingBytes'] == 51 and controls['wholeCNegativeControlsRejected'] == 1, 'Typed BBP bit0 to bit1 mutation rejected by complete native equality')
    check(not copied['arm9InventoryPresent'] and not copied['arm9StartupReportPresent'] and copied['immutableExternalInputMutationRejected'] and copied['compilerObjectsUnchangedByRejectedInventory'], 'ARM9/startup absent; bad inventory rejected before compile')
'''
    text = text[:start] + controls + text[end:]
    start = text.index('    root_descriptor = ')
    end = text.index('    check(all(sha256(ROOT / name)', start)
    mandatory = '''    descriptor = read_json(lane / 'canonical-packet.json')
    mandatory = inputs['mandatoryExternalInputs']
    inventory_inputs = [pin['path'] for pin in mandatory]
    check(set(inventory_inputs) == {'evidence/utility/ghidra-arm7.json', 'project.json'} and all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in mandatory), 'Exact immutable ARM7-only external inputs')
    check(not inputs['arm9StartupAssociationReportRequired'], 'No ARM9 startup dependency')
    missing_inputs = []
'''
    text = text[:start] + mandatory + text[end:]
    text = text.replace('wholeCWrongBodyControls=0', 'wholeCWrongBodyControls=1').replace('entryQualificationNegativeControls=5', 'entryQualificationNegativeControls=0')
    text = text.replace('noWholeCOrBehaviorControlClaim=True', 'independentBehaviorExecutionCredit=0')
    text = text.replace("producedReportDependency='evidence/matches/utility-arm9-startup01.json'", 'producedReportDependency=None')
    text = text.replace('child-third-eligibility-', 'child-fifth-eligibility-')
    exec(compile(text, str(base), 'exec'), dict(__name__='__main__', __file__=str(base)))
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/utility-child-fifth'
    report = read_json(lane / 'packet-ready.json')
    headers, import_names = set(), []
    for row in report['matches']:
        assert not row['compilerGeneratedBindings']
        headers.update(pin['path'] for pin in row['sourceDependencies'])
        with (ROOT / row['object']).open('rb') as stream:
            symbols = ELFFile(stream).get_section_by_name('.symtab')
            import_names.extend(symbol.name for symbol in symbols.iter_symbols() if symbol['st_shndx'] == 'SHN_UNDEF' and symbol.name in {'_ll_udiv', '_s32_div_f'})
    assert not import_names and len(headers) == 66
    maximum = max(len((ROOT / name).read_text().splitlines()) for name in headers)
    assert maximum == 449
    excluded = read_json(lane / 'ready-exclusions.json')
    assert len(excluded['functions']) == 1 and excluded['functions'][0]['address'] == '0x37fb26c' and excluded['functions'][0]['bytes'] == 940
    output = ROOT / 'evidence/verification/parallel-wave20261102/child-fifth-eligibility-initial.json'
    result = read_json(output)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)), frozenBaseAuditorSha256=sha256(base),
        requiredNextRootDescriptorFrozenInputs=read_json(lane / 'packet-ready-inputs.json')['mandatoryExternalInputs'],
        arm9InventoryOrStartupDependencyRequired=False, typedHeaderFiles=66, maximumHeaderLines=maximum,
        actualGeneratedCompilerImports=0, refusedCallbackInitializerBytes=940,
        next150UnionFunctions=44, next150UnionBytes=13828, sourceCredit=0)
    write_json(output, result)
    print(dict(passed=result['passed'], functions=25, bytes=6724, typedHeaders=66, maxHeaderLines=maximum,
        generatedCompilerImports=0, unionFunctions=44, unionBytes=13828))


if __name__ == '__main__':
    main()
