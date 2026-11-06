from pathlib import Path
import sys
sys.dont_write_bytecode = True
from project import ROOT, read_json, write_json, sha256
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
import arm7_runtime


def main():
    base = ROOT / 'audit_child_third_eligibility_parallel_wave20261102.py'
    assert sha256(base) == '3f6024b5307cb26658ea20a22c517cd51da3f623af00104e0a2dd61e70f4d9cf'
    text = base.read_text().replace('utility-child-third', 'host-arm7-sixth').replace("'arm9'", "'arm7'")
    text = text.replace('import utility_runtime', 'import arm7_runtime\nimport hashlib')
    text = text.replace("== 36 and ready['bytes']", "== 35 and ready['bytes']").replace('== 4458', '== 8400')
    text = text.replace('sealed36/4458', 'sealed35/8400').replace('functions=36, bytes=4458', 'functions=35, bytes=8400')
    text = text.replace('    layout, derived = utility_runtime.derive()', "    image = (ROOT / 'extract/arm7/arm7.bin').read_bytes()\n    layout = arm7_runtime.derive(image)")
    text = text.replace("        data = bytes(derived[ROOT / module['binary']])", "        data = image[module['inputFileOffset']:module['inputFileOffset'] + module['bytes']]")
    text = text.replace("row['program'] == utility_runtime.PROGRAM", "row['program'] == ''")
    text = text.replace('utility_runtime.sha(native)', 'hashlib.sha256(native).hexdigest()')
    text = text.replace("proof['qualifiedAdditionalCalleeBindings']", "proof.get('qualifiedAdditionalCalleeBindings', [])")
    start = text.index("    controls = read_json(lane / 'native-callee-binding-controls.json')")
    end = text.index('    reserved_map = ', start)
    controls = '''    controls = read_json(lane / 'whole-c-controls.json')
    wrong = ROOT / controls['wrongSource']
    wrong_body = ROOT / 'work/parallel-wave20261102/host-arm7-sixth/controls-wrong-link/caller.bin'
    check(controls['positiveWholeCExact'] and controls['positiveRealLink']['exactCallerBytes'], 'Positive whole-C genuine link control')
    check(sha256(wrong) == controls['wrongSourceSha256'] and controls['wrongCompilerResult']['compiledBytes'] == controls['wrongGenuinelyLinkedBytes'] == 44 and controls['wrongRealLinkAttempt']['exitCode'] == 0, 'Complete same-extent wrong-C compile and genuine link')
    check(sha256(wrong_body) == controls['wrongLinkedSha256'] and controls['wrongLinkedSha256'] != controls['originalNativeSha256'] and controls['wrongLinkedMatchingBytes'] == 43 and controls['wholeCNegativeControlsRejected'] == 1, 'Both parentSize+4 to parentSize+5 mutations rejected by complete native equality')
    check(not copied['utilityArchivePresent'] and not copied['utilityInventoryPresent'] and copied['immutableExternalInputMutationRejected'] and copied['compilerObjectsUnchangedByRejectedInventory'], 'Child archive/inventory absent; wrong host inventory rejected before compile')
'''
    text = text[:start] + controls + text[end:]
    start = text.index('    reserved_map = ')
    end = text.index('    overlaps = ', start)
    reserved = '''    reserved_map = subprocess.run(['git', 'show', '7ee8e5e94f82ffee6ebd91fc3ec63339fb0204c1:source-map.json'], cwd=ROOT, capture_output=True, check=True).stdout
    reserved = [(identity(row), row['bytes']) for row in json.loads(reserved_map)['matchedFunctions']]
    for specification in ['cohort149-parallel-wave20261102-next-specification.json', 'cohort150-parallel-wave20261102-next-specification.json']:
        path = ROOT / specification
        if path.exists():
            reserved.extend((identity(row), row['bytes']) for row in read_json(path)['expectedAdditions'] if identity(row) not in {key for key, size in owned})
    for other in ['utility-child-fourth', 'utility-child-fifth']:
        document = read_json(ROOT / 'evidence/lanes/parallel-wave20261102' / other / 'ready.json')
        reserved.extend((identity(row), row['bytes']) for row in document['identities'])
'''
    text = text[:start] + reserved + text[end:]
    start = text.index('    root_descriptor = ')
    end = text.index('    check(all(sha256(ROOT / name)', start)
    mandatory = '''    descriptor = read_json(lane / 'canonical-packet.json')
    mandatory = inputs['mandatoryExternalInputs']
    inventory_inputs = [pin['path'] for pin in mandatory]
    check(set(inventory_inputs) == {'evidence/arm7/ghidra-runtime-inventory.json', 'project.json'} and all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in mandatory), 'Exact immutable host-only runtime inventory/configuration inputs')
    check(not inputs['arm9StartupAssociationReportRequired'], 'No ARM9 startup dependency')
    missing_inputs = []
'''
    text = text[:start] + mandatory + text[end:]
    text = text.replace('wholeCWrongBodyControls=0', 'wholeCWrongBodyControls=1').replace('entryQualificationNegativeControls=5', 'entryQualificationNegativeControls=0')
    text = text.replace('noWholeCOrBehaviorControlClaim=True', 'independentBehaviorExecutionCredit=0')
    text = text.replace("producedReportDependency='evidence/matches/utility-arm9-startup01.json'", 'producedReportDependency=None')
    text = text.replace('child-third-eligibility-', 'host-arm7-sixth-eligibility-')
    exec(compile(text, str(base), 'exec'), dict(__name__='__main__', __file__=str(base)))
    lane = ROOT / 'evidence/lanes/parallel-wave20261102/host-arm7-sixth'
    report = read_json(lane / 'packet-ready.json')
    image = (ROOT / 'extract/arm7/arm7.bin').read_bytes()
    modules = {r['id']: r for r in arm7_runtime.derive(image)['modules']}
    inventory = read_json(ROOT / 'evidence/arm7/ghidra-runtime-inventory.json')
    entries = {int(r['address'], 0): r for r in inventory['functions']}
    headers, aliases, generated = set(), [], []
    for row in report['matches']:
        assert row['program'] == '' and row['processor'] == 'arm7' and row['module'] == 'arm7-main' and row['mode'] == 'arm'
        assert not row['compilerGeneratedBindings']
        headers.update(pin['path'] for pin in row['sourceDependencies'])
        with (ROOT / row['object']).open('rb') as stream:
            generated.extend(s.name for s in ELFFile(stream).get_section_by_name('.symtab').iter_symbols() if s['st_shndx'] == 'SHN_UNDEF' and s.name.startswith(('_ll_', '_s32_div', '__aeabi')))
        for binding in row['realLink']['bindings']:
            assert binding['program'] == '' and binding['processor'] == 'arm7'
            if binding['kind'] != 'function':
                continue
            target = int(binding['address'], 0)
            original = entries[target]
            assert original['mode'] == binding['mode'] == 'arm' and original['module'] == binding['module'] and binding['module'] in modules
            target_module = modules[binding['module']]
            assert int(target_module['base'], 0) <= target < int(target_module['base'], 0) + target_module['bytes']
            with (ROOT / binding['anchorObject']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == binding['name'])
                assert symbol['st_info']['type'] == 'STT_FUNC' and symbol['st_size'] == symbol['st_value'] == 0 and elf.get_section(symbol['st_shndx'])['sh_type'] == 'SHT_NOBITS'
                assert any(s.name == '$a' and s['st_value'] == 0 for s in elf.get_section_by_name('.symtab').iter_symbols())
            aliases.append((binding['module'], binding['address'], binding['mode']))
    assert not generated
    assert all(r['program'] == '' and r['processor'] == 'arm7' and r['mode'] in ('arm', 'data') for r in report['nativeSymbolBindings'])
    assert len(report['nativeSymbolBindings']) == sum(len(r['relocations']) for r in report['matches']) == 265
    output = ROOT / 'evidence/verification/parallel-wave20261102/host-arm7-sixth-eligibility-initial.json'
    result = read_json(output)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)), frozenBaseAuditorSha256=sha256(base),
        requiredNextRootDescriptorFrozenInputs=read_json(lane / 'packet-ready-inputs.json')['mandatoryExternalInputs'],
        arm9OrChildInventoryOrStartupDependencyRequired=False, typedHeaderFiles=len(headers),
        maximumHeaderLines=max(len((ROOT / name).read_text().splitlines()) for name in headers),
        actualGeneratedCompilerImports=0, qualifiedArmCalleeAnchorRows=len(aliases),
        currentCrossModeCallerOrCalleeImports=0,
        globalHostArm7TypedBindingSchema='link_arm7 consumes flat nativeSymbols; informational nativeSymbolBindings is not a typed import interface',
        globalHostArm7WholeModuleLinkRequired=True, sourceCredit=0)
    write_json(output, result)
    print(dict(passed=result['passed'], functions=35, bytes=8400, typedHeaders=len(headers), anchors=len(aliases), sourceCredit=0))


if __name__ == '__main__':
    main()
