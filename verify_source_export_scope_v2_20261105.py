import copy
import re
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
import build_modules
import source_export_scope_20261105 as original
import source_export_scope_v2_20261105 as qualified


def main():
    work = ROOT / 'work/weak-source-export-v2-seeded-integration-20261105'
    assert not work.exists()
    work.mkdir(parents=True)
    shared = ROOT / 'build/link-work'
    document = read_json(shared / 'source-units.json')
    names = set(qualified.APPROVED) | {'native_main_02000a78'}
    units = [r for r in document['units'] if r.get('function') in names]
    assert len(units) == 3
    report_path = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/varargs/packet/match.json'
    protected = [shared / 'linked.elf', shared / 'source-units.json', shared / 'config-arm9/symbols.txt', ROOT / 'config/arm9/symbols.txt', ROOT / 'build_modules.py', ROOT / original.WITNESS]
    before = {p.as_posix(): sha256(p) for p in protected}
    seed = work / 'seed.json'
    write_json(seed, dict(schemaVersion=1, units=[], nativeSymbols={}))
    with patch.object(build_modules, 'WORK', work):
        selected = build_modules.collect_units(seed, [report_path])
    addition = next(r for r in read_json(selected)['units'] if r.get('function') == 'native_main_0201a670')
    units.append(addition)
    protected += [ROOT / r['object'] for r in units] + [ROOT / r['source'] for r in units]
    before.update({p.as_posix(): sha256(p) for p in protected})
    specification = work / 'four-units.json'
    write_json(specification, dict(document, units=units))
    reports = {}
    for label, implementation in [('original', original), ('qualified', qualified)]:
        destination = work / label
        destination.mkdir()
        report = dict(sourceUnits=[])
        with patch.object(build_modules, 'WORK', destination), patch.object(build_modules, 'source_weak_export', implementation.source_weak_export):
            build_modules.prepare_units(specification, report)
        reports[label] = report
    assert {r['name'] for r in reports['original']['sourceExportScopes']} == set(original.APPROVED)
    assert {r['name'] for r in reports['qualified']['sourceExportScopes']} == set(qualified.APPROVED)
    for name in names:
        for label in ['original', 'qualified']:
            text = (work / label / 'config-arm9/symbols.txt').read_text()
            line = next(s for s in text.splitlines() if s.startswith(name + ' '))
            approved = set(original.APPROVED) if label == 'original' else set(qualified.APPROVED)
            assert bool(re.search(r'\bweak\b', line)) == (name in approved)
        assert sha256(work / 'original' / (name + '.o')) == sha256(work / 'qualified' / (name + '.o'))
    controls = []
    for field, value in [('module', 'ov001'), ('start', '0x0201a674'), ('end', '0x0201af68'), ('sourceSha256', '0' * 64), ('source', 'src/unknown.c')]:
        wrong = copy.deepcopy(addition)
        wrong[field] = value
        with (ROOT / addition['object']).open('rb') as stream:
            try:
                qualified.source_weak_export(wrong, ELFFile(stream))
            except AssertionError:
                controls.append(field)
            else:
                raise ValueError('Invalid SDK weak export accepted: ' + field)
    try:
        qualified.weak_record('kind:function(arm) addr:0x0201a670 local\n')
    except AssertionError:
        controls.append('local-scope')
    else:
        raise ValueError('Local source scope accepted')
    assert before == {p.as_posix(): sha256(p) for p in protected}
    write_json(ROOT / 'evidence/verification/source-export-scope-v2-integration-20261105.json', dict(
        passed=True, sourceCredit=0, qualifiedGeneratedWeakExports=reports['qualified']['sourceExportScopes'],
        originalTwoScopesPreserved=True, strongControlPreserved=True, byteIdenticalSplitObjects=4,
        originalSourceObjectsWitnessAndSharedBuilderUnchanged=True, rejectedControls=controls,
        unchangedStrictFullGlobalSymbolCheckStillRequired=True, fullGlobalPositiveNotClaimed=True,
        guardQualification='evidence/lanes/parallel-wave20261105/main-sdk-bulk/varargs/packet/weak-export-qualification.json',
        scopeCheckFeasibilityDiagnostic='evidence/lanes/parallel-wave20261105/main-sdk-bulk/varargs/packet/weak-scope-check.json',
        qualifierSha256=sha256(ROOT / 'source_export_scope_v2_20261105.py')))
    print(dict(passed=True, generatedWeakExports=3, byteIdenticalSplitObjects=4, rejectedControls=len(controls), fullGlobalCheckPending=True))


if __name__ == '__main__':
    main()
