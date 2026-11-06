import copy
import json
import re
import subprocess
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
sys.path.insert(0, str(ROOT / 'deps/native'))
from elftools.elf.elffile import ELFFile
import build_modules
import source_export_scope_20261105 as scope


def main():
    shared = ROOT / 'build/link-work'
    work = ROOT / 'work/weak-source-export-integration-20261105'
    assert not work.exists()
    work.mkdir(parents=True)
    names = set(scope.APPROVED) | {'native_main_02000a78'}
    document = read_json(shared / 'source-units.json')
    units = [r for r in document['units'] if r.get('function') in names]
    assert len(units) == 3
    protected = [shared / 'linked.elf', shared / 'config-arm9/symbols.txt', ROOT / 'config/arm9/symbols.txt']
    protected += [ROOT / r['object'] for r in units]
    before = {p.as_posix(): sha256(p) for p in protected}
    spec = work / 'selected-units.json'
    write_json(spec, dict(document, units=units))
    report = dict(sourceUnits=[])
    with patch.object(build_modules, 'WORK', work / 'generated'):
        (work / 'generated').mkdir()
        build_modules.prepare_units(spec, report)
    assert {r['name'] for r in report['sourceExportScopes']} == set(scope.APPROVED)
    generated = (work / 'generated/config-arm9/symbols.txt').read_text()
    for name in names:
        line = next(s for s in generated.splitlines() if s.startswith(name + ' '))
        assert bool(re.search(r'\bweak\b', line)) == (name in scope.APPROVED)
        unit = next(r for r in units if r['function'] == name)
        assert sha256(work / 'generated' / (name + '.o')) == sha256(shared / (name + '.o'))
    base = next(r for r in units if r['function'] == 'native_main_02000800')
    controls = []
    for field, value in [('module', 'ov001'), ('start', '0x02000804'), ('end', '0x02000938'),
                         ('sourceSha256', '0' * 64), ('source', 'src/unknown.c')]:
        wrong = copy.deepcopy(base)
        wrong[field] = value
        with (ROOT / base['object']).open('rb') as stream:
            try:
                scope.source_weak_export(wrong, ELFFile(stream))
            except AssertionError:
                controls.append(field)
            else:
                raise AssertionError(field)
    try:
        scope.weak_record('kind:function(arm) addr:0x02000800 local\n')
    except AssertionError:
        controls.append('local-scope')
    else:
        raise AssertionError('local scope was accepted')
    assert scope.weak_record('kind:function(arm) weak\n') == 'kind:function(arm) weak\n'
    full = (shared / 'config-arm9/symbols.txt').read_text()
    lines = []
    for line in full.splitlines(keepends=True):
        name, separator, rest = line.partition(' ')
        if name in scope.APPROVED:
            line = name + separator + scope.weak_record(rest)
        lines.append(line)
    symbols = work / 'symbols.txt'
    symbols.write_text(''.join(lines))
    config = work / 'config.yaml'
    original = (shared / 'config-arm9/symbols.txt').as_posix()
    text = (shared / 'config.yaml').read_text()
    assert text.count(original) == 1
    config.write_text(text.replace(original, symbols.as_posix()))
    command = [str(ROOT / 'tools/dsd.exe'), 'check', 'symbols', '--config-path', str(config),
               '--elf-path', str(shared / 'linked.elf'), '--fail']
    run = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=180)
    assert run.returncode == 0, run.stdout + run.stderr
    assert before == {p.as_posix(): sha256(p) for p in protected}
    output = 'evidence/verification/source-export-scope-integration-20261105.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, generatedWeakExports=report['sourceExportScopes'],
        strongControlPreserved=True, unchangedSplitObjectHashes=True, unchangedOriginalInputsAndSharedArtifacts=True,
        rejectedContractControls=controls, strictFullSymbolCommand=command, strictFullSymbolExitCode=run.returncode,
        stdout=run.stdout, stderr=run.stderr, originalPrivateScopeNegatives='evidence/lanes/parallel-wave20261105/weak-source-export-scope/receipt.json',
        consumerSha256=sha256(ROOT / 'build_modules.py'), qualifierSha256=sha256(ROOT / 'source_export_scope_20261105.py')))
    print(dict(passed=True, weakExports=2, strongControls=1, rejectedControls=len(controls), strictFullSymbolCheck=True))


if __name__ == '__main__':
    main()
