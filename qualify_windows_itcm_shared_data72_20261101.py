import gzip
import hashlib
import json
import os
import struct
import subprocess
from pathlib import Path
import match_lowlevel as compiler
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
from inspect_windows_native_link_frontier111_20261101 import coff
from isolate_windows_selected_functions111_20261101 import bodies, flags
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA

WORK = ROOT / 'work/windows-itcm-shared-data72-20261101'
NAMES = ['src/itcm/translated03/native_itcm_01ffab90.c',
    'src/itcm/translated03/native_itcm_01ffac28.c']


def details(report):
    path = ROOT / report['details']['path']
    assert sha256(path) == report['details']['sha256']
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == report['details']['decodedSha256']
    return json.loads(raw)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    assert sha256(compiler.COMPILER) == '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
    before_path = ROOT / 'evidence/verification/cohort112-before-adoption-20261101.json'
    before = read_json(before_path)['selected']
    module, image, unused = measured_module('itcm')
    arm_proofs = []
    definition = b'u8 native_data_01fff960[0x48];'
    declaration = b'extern u8 native_data_01fff960[];'
    for index, name in enumerate(NAMES):
        source = ROOT / name
        selected = next(row for row in before if row['source'] == name)
        assert sha256(source) == selected['sourceSha256']
        assert source.read_bytes().count(definition) == source.read_bytes().count(declaration) == 1
        compiler.WORK = WORK / f'arm-{index}' / 'compile'
        rows, unused = compiler.compare(source, 'itcm', 2, 'off')
        assert len(rows) == 1 and not rows[0].get('compileFailed')
        row = rows[0]
        binding = qualified_bindings(row)['native_data_01fff960']
        assert binding == dict(processor='arm9', module='itcm', mode='data', kind='data', address='0x1fff960')
        references = [relocation for relocation in row['relocations'] if relocation['symbol'] == 'native_data_01fff960']
        assert references and all(reference['type'] == 2 for reference in references)
        for reference in references:
            offset = int(row['address'], 0) - int(module['base'], 0) + reference['offset']
            assert struct.unpack_from('<I', image, offset)[0] == 0x01FFF960
        proof = validate(row, qualified_bindings(row), WORK / f'arm-{index}' / 'link')
        arm_proofs.append(dict(compilation=row, genuineLinkComparison=freeze_link(proof),
            commonDataBinding=binding, nativeReferenceOffsets=[reference['offset'] for reference in references]))
    census_path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json'
    census = read_json(census_path)
    census_details = details(census)
    original = next(row for row in census_details['results'] if row['source'] == NAMES[1])
    clang = Path(original['command'][0])
    assert sha256(clang) == CLANG_SHA
    original_source = ROOT / NAMES[1]
    source_bytes = original_source.read_bytes()
    modified = source_bytes.replace(definition, b'')
    assert declaration in modified and len(source_bytes) - len(modified) == len(definition)
    candidate = ROOT / 'generated/portability/20261101-shared-data72/native_itcm_01ffac28.c'
    candidate.parent.mkdir(parents=True, exist_ok=True)
    if candidate.exists():
        assert candidate.read_bytes() == modified
    else:
        candidate.write_bytes(modified)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command, require_success=True):
        command = list(map(str, command))
        attempt = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=attempt.returncode,
            stdoutSha256=hashlib.sha256(attempt.stdout).hexdigest(), stderr=attempt.stderr.decode(errors='replace')))
        if require_success:
            assert attempt.returncode == 0, steps[-1]
        return attempt

    options = flags(original['command'])
    ast_before = json.loads(run([clang, *options, '-Xclang', '-ast-dump=json', '-fsyntax-only', original_source]).stdout)
    ast_after = json.loads(run([clang, *options, '-iquote', original_source.parent,
        '-Xclang', '-ast-dump=json', '-fsyntax-only', candidate]).stdout)
    first = bodies(ast_before, source_bytes)
    second = bodies(ast_after, modified)
    assert set(first) == set(second)
    assert all(first[name]['bodySha256'] == second[name]['bodySha256'] for name in first)
    obj = WORK / 'shared-reference.obj'
    run([clang, *options, '-iquote', original_source.parent, '-c', candidate, '-o', obj])
    parsed = coff(obj)
    symbol = '_native_data_01fff960'
    assert not any(row['name'] == symbol for row in parsed['definitions'])
    assert any(row['name'] == symbol for row in parsed['undefined'])
    frontier_path = ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-20261101.json'
    frontier = read_json(frontier_path)
    native = details(frontier)
    host = {}
    owner = None
    for row in native['objects']:
        if not any(processor == 'arm9' and not program for processor, program, module in row['scopes']):
            continue
        assert sha256(ROOT / row['object']) == row['objectSha256']
        if row['source'] == NAMES[0]:
            owner = row
        host[row['source']] = obj if row['source'] == NAMES[1] else ROOT / row['object']
    assert owner and any(row['name'] == symbol for row in coff(ROOT / owner['object'])['definitions'])
    owners = [name for name, path in host.items() if any(row['name'] == symbol for row in coff(path)['definitions'])]
    assert owners == [NAMES[0]], owners
    linker = clang.parent / 'ld.lld.exe'
    assert sha256(linker) == LINKER_SHA
    output = WORK / 'host-arm9-shared-data.dll'
    assert not output.exists()
    arguments = ['/dll', '/noentry', '/machine:x86', '/nodefaultlib', '/safeseh:no',
        '/timestamp:0', '/errorlimit:0', '/opt:noref', '/out:' + str(output),
        *[str(path) for name, path in sorted(host.items())]]
    response = WORK / 'host-arm9.rsp'
    response.write_text('\n'.join(subprocess.list2cmdline([value]) for value in arguments) + '\n', encoding='utf-8')
    attempt = run([linker, '-flavor', 'link', '@' + str(response)], require_success=False)
    diagnostic = attempt.stdout + attempt.stderr
    text = diagnostic.decode(errors='replace')
    undefined = text.count('undefined symbol:')
    duplicates = text.count('duplicate symbol:')
    assert attempt.returncode != 0 and not output.exists() and undefined > 0 and duplicates == 0
    log = ROOT / 'evidence/portability/windows-host-arm9-shared-data72-link-diagnostic-20261101.txt.gz'
    log.write_bytes(gzip.compress(diagnostic, mtime=0))
    steps[-1].pop('stderr')
    steps[-1]['diagnosticSha256'] = hashlib.sha256(diagnostic).hexdigest()
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        sourceCredit=0, acceptedArmSourceModified=False, nativeGameExecutionCount=0,
        originalModule=module, sharedDataAddress='0x01fff960', declaredByteExtent=72,
        armProofs=arm_proofs, windowsCanonicalDefinitionSource=NAMES[0],
        windowsReferenceVariant=dict(originalSource=NAMES[1], originalSourceSha256=sha256(original_source),
            source=candidate.relative_to(ROOT).as_posix(), sourceSha256=sha256(candidate),
            object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
            functionBodiesUnchanged=True, selectedBodyHashes={name: row['bodySha256'] for name, row in first.items()}),
        hostObjectUnits=len(host), dataDefinitionCount=len(owners),
        actualLinkExitCode=attempt.returncode, actualDuplicateSymbolDiagnostics=duplicates,
        actualUndefinedSymbolDiagnostics=undefined, outputProduced=False, fullWindowsGameProven=False,
        diagnostic=dict(path=log.relative_to(ROOT).as_posix(), sha256=sha256(log), decodedSha256=hashlib.sha256(diagnostic).hexdigest()),
        sourceSnapshot=dict(path=before_path.relative_to(ROOT).as_posix(), sha256=sha256(before_path)),
        originalFrontier=dict(path=frontier_path.relative_to(ROOT).as_posix(), sha256=sha256(frontier_path)), steps=steps,
        limitations=['Two identical C definitions refer to the same measured physical ITCM data identity; one definition and one extern reference are retained',
            'This is native link ownership, not source-byte credit or an original initialization-phase proof',
            'Neighbor data views, interior alias bindings and the separate12-byte/offset0x1C backing concern remain unqualified',
            'No game routine or diagnostic DLL is executed; unresolved functions/globals/platform interfaces remain hard link failures',
            'Windows source bodies remain text-identical but inlining/object layout and full native semantics are separate gates'])
    write_json(ROOT / 'evidence/portability/windows-itcm-shared-data72-20261101.json', report)
    print(dict(hostObjects=len(host), sharedDataDefinitions=1, duplicateDiagnostics=duplicates,
        undefinedDiagnostics=undefined, fullNativeGame=False, sourceCredit=0))


if __name__ == '__main__':
    main()
