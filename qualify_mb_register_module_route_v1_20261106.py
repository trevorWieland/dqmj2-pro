import copy
import hashlib
import struct
import sys
import uuid
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256, now
import build_modules as builder
import mb_register_module_route_v1_20261106 as context
from auth_context_route_v2_20261106 import module_route as auth_route


def controls(work):
    from elftools.elf.elffile import ELFFile
    report = read_json(ROOT / 'evidence/matches/mb-local-context-register-parallel-wave20261106.json')
    row, = report['matches']
    source = ROOT / row['object']
    positive = context.inspect_object(source)
    with source.open('rb') as stream:
        elf = ELFFile(stream)
        table = elf.get_section_by_name('.symtab')
        local_index = next(i for i, s in enumerate(table.iter_symbols()) if s.name == 'update$40')
        function_index = next(i for i, s in enumerate(table.iter_symbols()) if s.name == context.NAME)
        local_at = table['sh_offset'] + local_index * table['sh_entsize']
        function_at = table['sh_offset'] + function_index * table['sh_entsize']
        bss_at = elf['e_shoff'] + elf.get_section_index('.bss') * elf['e_shentsize']
        text = elf.get_section_by_name('.text')
        mutations = [('bss-file-backed', bss_at + 4, 1, 4), ('bss-size-two', bss_at + 20, 2, 4),
            ('bss-alignment-four', bss_at + 32, 4, 4), ('bss-not-allocated', bss_at + 8, 1, 4),
            ('local-object-globalized', local_at + 12, 0x11, 1), ('local-object-absolute', local_at + 14, 0xfff1, 2),
            ('local-object-size-two', local_at + 8, 2, 4), ('local-object-offset-one', local_at + 4, 1, 4),
            ('function-size-short', function_at + 8, 652, 4), ('stored-source-opcode-changed', text['sh_offset'], None, 1)]
    rejected = []
    for name, offset, value, width in mutations:
        data = bytearray(source.read_bytes())
        if value is None:
            data[offset] ^= 1
        else:
            data[offset:offset + width] = value.to_bytes(width, 'little')
        path = work / (name + '.o')
        path.write_bytes(data)
        try:
            context.inspect_object(path)
        except (AssertionError, ValueError, KeyError, OSError):
            rejected.append(name)
        else:
            raise AssertionError('Malformed source storage contract admitted: ' + name)
    assert len(rejected) == 10
    return dict(passed=True, rejectedActualElfMutations=rejected, genuineSourceObjectSha256=sha256(source),
        originalRelocations=len(positive['relocations']), initializedStorageCredit=0)


def main():
    work = ROOT / 'work/mb-register-module-route-controls' / uuid.uuid4().hex[:12]
    work.mkdir(parents=True)
    negative = controls(work)
    integration = read_json(ROOT / 'evidence/verification/integration.json')
    arguments = ROOT / integration['argumentFile']['path']
    assert sha256(arguments) == integration['argumentFile']['sha256']
    args = arguments.read_text().splitlines()
    assert '--source-matches' in args
    report_name = 'evidence/matches/mb-local-context-register-parallel-wave20261106.json'
    assert report_name not in args
    args.extend(['--source-matches', report_name])
    before = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', 'build_modules.py', 'elf_units.py']}
    write_json(work / 'state.json', dict(state='running', sourceCredit=0, createdUtc=now(), baselineIntegrationSha256=sha256(ROOT / 'evidence/verification/integration.json')))
    print(dict(started=True, output=work.relative_to(ROOT).as_posix(), actualElfNegatives=10), flush=True)
    with patch.object(builder, 'WORK', work / 'link-work'), patch.object(builder, 'EVIDENCE', work / 'evidence'), \
            auth_route(builder), context.module_route(builder), patch.object(sys, 'argv', [__file__, *args]):
        code = builder.main()
    assert before == {name: sha256(ROOT / name) for name in before}
    report = read_json(work / 'evidence/latest.json')
    result = dict(passed=code == 0, sourceCredit=0, exitCode=code, finishedUtc=now(), controls=negative,
        previousAcceptedCorpusIncluded=True, addedFunctionBytes=656, addedInitializedStorageBytes=0,
        newSourceLocalBssBytes=1, canonicalProductionInputsUnchanged=True, failure=report.get('failure'),
        allModuleBytesExact=report.get('allModuleBytesExact'), strictSymbolsPassed=report.get('symbolCheckPassed'),
        hostArm9ModuleComparisons=len(report['modules']), allOtherProcessorSharedGatesStillRequired=True,
        route=dict(path='mb_register_module_route_v1_20261106.py', sha256=sha256(ROOT / 'mb_register_module_route_v1_20261106.py')),
        privateBuildReport=dict(path=(work / 'evidence/latest.json').relative_to(ROOT).as_posix(), sha256=sha256(work / 'evidence/latest.json')),
        actualAcceptedRegistrySha256=before['recovery.json'], globalConsumerAdoptionProven=False,
        generatorSha256=sha256(__file__))
    write_json(work / 'state.json', result)
    write_json(ROOT / 'evidence/verification/mb-register-module-route-v1-qualification-20261106.json', result)
    print(dict(passed=result['passed'], failure=result['failure'], output=work.relative_to(ROOT).as_posix()), flush=True)
    raise SystemExit(code)


if __name__ == '__main__':
    main()
