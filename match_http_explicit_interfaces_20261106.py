import importlib
import os
import shutil
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256


LAYOUT = 'evidence/lanes/parallel-wave20261106/http-explicit-interfaces/source-layout.json'
REPORT = 'evidence/matches/http-explicit-interfaces-20261106.json'
WORK = 'work/http-explicit-interfaces-20261106'


def extent(row):
    from elftools.elf.elffile import ELFFile
    with (ROOT / row['object']).open('rb') as stream:
        elf = ELFFile(stream)
        symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['name'])
        start = symbol['st_value'] & ~1
        return elf.get_section(symbol['st_shndx']).data()[start:start + symbol['st_size']], dict(
            binding=symbol['st_info']['bind'], type=symbol['st_info']['type'], bytes=symbol['st_size'])


def diagnostic_compile(row, source, obj, env):
    obj.parent.mkdir(parents=True, exist_ok=True)
    command = [str(ROOT / row['compiler']), *row['compilerFlags'], '-requireprotos', '-w', 'error',
               '-c', str(source), '-o', str(obj)]
    run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
    return run, command


def main():
    config = configuration()
    native_dependencies(config)
    import link_runtime_unit as linker
    from recover_linked_runtime import qualified_bindings
    from seal_recovery_evidence_20261031 import code_closure
    layout = read_json(ROOT / LAYOUT)
    assert layout['sourceCredit'] == layout['newByteCredit'] == 0
    assert sha256(ROOT / layout['ownershipClaim']) == layout['ownershipClaimSha256']
    assert sha256(ROOT / layout['qualifiedPrototypeProbe']) == layout['qualifiedPrototypeProbeSha256']
    assert sha256(ROOT / layout['debtReceipt']) == layout['debtReceiptSha256']
    assert len(layout['sources']) == 5
    assert {int(item['address'], 0) for item in layout['sources']} == {0x02099058, 0x020990f0, 0x02099dc8, 0x0209a008, 0x02099df4}
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    matches, proofs = [], []
    for item in layout['sources']:
        for pin in [item['oldSource'], *item['oldHeaders'], *item['headers']]:
            assert sha256(ROOT / pin['path']) == pin['sha256']
        source = ROOT / item['source']
        assert sha256(source) == item['sourceSha256'] == item['oldSource']['sha256']
        directory = ROOT / WORK / item['address']
        builder = importlib.import_module('wave20261105_dwc_http_next_' + item['packet'] + '_build').build
        old, old_body = builder(ROOT / item['oldSource']['path'], directory / 'previous-view')
        row, body = builder(source, directory / 'primary')
        assert old_body == body
        assert row['bytes'] == old['bytes'] and row['targetSha256'] == old['targetSha256']
        assert row['compilerSha256'] == old['compilerSha256'] and row['compilerFlags'] == old['compilerFlags']
        assert row['relocations'] == old['relocations'] and row['nativeSymbolEntries'] == old['nativeSymbolEntries']
        compiled, symbol = extent(row)
        previous, old_symbol = extent(old)
        assert compiled == previous and symbol == old_symbol and row['realLink']['exactCallerBytes']
        strict_obj = directory / 'strict' / 'caller.o'
        run, command = diagnostic_compile(row, source, strict_obj, env)
        assert run.returncode == 0, run.stdout + run.stderr
        strict_row = dict(row, object=strict_obj.relative_to(ROOT).as_posix(), objectSha256=sha256(strict_obj))
        strict_bytes, strict_symbol = extent(strict_row)
        assert strict_bytes == compiled and strict_symbol == symbol
        assert linker.relocation_rows(ROOT / row['object'], row['name']) == linker.relocation_rows(strict_obj, row['name'])
        strict_link = linker.validate(strict_row, qualified_bindings(row), directory / 'strict-link')
        assert strict_link['exactCallerBytes']
        negative = directory / 'missing-declaration'
        negative.mkdir(parents=True, exist_ok=True)
        negative_source = negative / source.name
        shutil.copyfile(source, negative_source)
        for pin in item['headers']:
            shutil.copyfile(ROOT / pin['path'], negative / (ROOT / pin['path']).name)
        header = negative / 'context.h'
        text = header.read_text()
        assert text.count(item['addedCalleeDeclaration']) == 1
        header.write_text(text.replace(item['addedCalleeDeclaration'], ''), encoding='utf-8')
        rejected_obj = negative / 'rejected.o'
        assert not rejected_obj.exists()
        rejected, rejected_command = diagnostic_compile(row, negative_source, rejected_obj, env)
        diagnostics = (rejected.stdout + rejected.stderr).decode('utf-8', errors='replace')
        (negative / 'compiler-diagnostic.txt').write_text(diagnostics, encoding='utf-8')
        assert rejected.returncode != 0 and not rejected_obj.exists()
        assert 'function has no prototype' in diagnostics
        proofs.append(dict(address=row['address'], packet=item['packet'], originalSource=item['oldSource'],
            originalHeaderPins=item['oldHeaders'], newHeaderPins=item['headers'], sourceBodyByteIdentical=True,
            primaryCompilerFlagsUnchanged=True, completeCompilerFunctionBytesIdentical=True,
            originalRelocationsBindingsAndNativeExtentIdentical=True, strictPrototypeCommand=command,
            strictObjectSha256=sha256(strict_obj), strictRealLink=strict_link,
            missingPrototypeRejected=True, negativeCommand=rejected_command, negativeDiagnostic=diagnostics,
            originalBoundedMachineModelsPreservedByCompleteCompilerBytesAndRelocationIdentity=True,
            newFunctionCredit=0, newByteCredit=0))
        row.update(sourceLanguage='C', ordinaryCBytes=row['bytes'], justifiedAssemblyBytes=0,
                   interfaceMigrationOnly=True, previousSource=item['oldSource'], newFunctionCredit=0, newByteCredit=0)
        matches.append(row)
    names = code_closure(['match_http_explicit_interfaces_20261106.py', *[
        'wave20261105_dwc_http_next_' + packet + '_build.py' for packet in ['fifth', 'sixth', 'seventh']]])
    write_json(ROOT / REPORT, dict(schemaVersion=1, romSha256=config['romSha256'], program='', processor='arm9',
        module='main', allPassed=True, matches=matches, matchedFunctions=5,
        matchedBytes=sum(row['bytes'] for row in matches), intendedUse='zero-byte-source-preference-migration-only',
        newFunctionCredit=0, newByteCredit=0, sourceCredit=0, ordinaryCBytes=sum(row['bytes'] for row in matches),
        justifiedAssemblyBytes=0, controls=proofs, layout=LAYOUT, layoutSha256=sha256(ROOT / LAYOUT),
        generatorSources=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)],
        limits=['No old selected caller, header, Ready, registry, policy or acceptance changed.',
                'Caller machine models are transferred by complete code/relocation/binding identity; they are not counted as new executions.',
                'Source generation, copied-root replay and full shared gates remain separate obligations.',
                'Imported source declarations are distinct from uniquely proven original formal types.']))
    print(dict(passed=True, migrationCallers=5, newFunctionCredit=0, newByteCredit=0))


if __name__ == '__main__':
    main()
