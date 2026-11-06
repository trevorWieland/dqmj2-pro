import copy
import hashlib
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from match_child_message_data_20261106 import inspect_object


def qualify(row):
    from elftools.elf.elffile import ELFFile
    assert row['kind'] == row['mode'] == 'data'
    assert row['ordinaryFunctionCredit'] == row['executableSectionBytes'] == row['allocatedZeroFillBytes'] == 0
    assert row['relocations'] == []
    assert row['bytes'] == row['size'] == row['compiledBytes'] == row['initializedBytes']
    assert sha256(ROOT / row['binary']) == row['inputModuleSha256']
    offset = int(row['address'], 0) - int(row['moduleBase'], 0)
    image = (ROOT / row['binary']).read_bytes()
    assert 0 <= offset and offset + row['bytes'] <= len(image)
    payload = image[offset:offset + row['bytes']]
    assert hashlib.sha256(payload).hexdigest() == row['targetSha256'] == row['outputSha256']
    assert sha256(ROOT / row['source']) == row['sourceSha256']
    assert sha256(ROOT / row['semanticSource']) == row['semanticSourceSha256']
    assert sha256(ROOT / row['object']) == row['objectSha256']
    assert sha256(ROOT / row['compiler']) == row['compilerSha256']
    section, _, _, _ = inspect_object(ROOT / row['object'], row['nativeSymbol'], payload)
    assert section == row['section']
    link = row['realLink']
    assert link['exactDataBytes'] and link['exactDataAddress'] and link['objectUnmodified']
    assert link['actualSymbolType'] == 'STT_OBJECT'
    assert link['linkedDataSha256'] == row['targetSha256']
    assert sha256(ROOT / link['linkedElf']) == link['linkedElfSha256']
    linked_directory = (ROOT / link['linkedElf']).parent
    assert sha256(linked_directory / 'input.o') == row['objectSha256']
    assert (linked_directory / 'data.bin').read_bytes() == payload
    with (ROOT / link['linkedElf']).open('rb') as stream:
        elf = ELFFile(stream)
        entries = [s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == row['nativeSymbol']]
        assert len(entries) == 1
        symbol = entries[0]
        assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_size'] == len(payload)
        assert symbol['st_value'] == int(row['address'], 0)
        target = elf.get_section(symbol['st_shndx'])
        if target['sh_size']:
            assert target['sh_flags'] & 2 and not target['sh_flags'] & 4
            start = symbol['st_value'] - target['sh_addr']
            assert target.data()[start:start + len(payload)] == payload
        else:
            assert target.name == 'DATA' and target['sh_type'] == 'SHT_PROGBITS'
            assert target['sh_flags'] == 0x10000000 and target['sh_addr'] == int(row['address'], 0)
    return dict(program=row['program'], processor=row['processor'], module=row['module'],
                address=row['address'], bytes=len(payload), targetSha256=row['targetSha256'],
                objectSha256=row['objectSha256'], linkedElfSha256=link['linkedElfSha256'])


def main():
    assert len(sys.argv) == 2
    native_dependencies(configuration())
    descriptor_name = sys.argv[1]
    descriptor = read_json(ROOT / descriptor_name)
    assert descriptor['sourceCredit'] == 0 and descriptor['registrationTransportOnly']
    old_name = descriptor['originalTransport']
    assert sha256(ROOT / old_name) == descriptor['originalTransportSha256']
    old = read_json(ROOT / old_name)
    command = [sys.executable, str(ROOT / 'replay_initialized_data_packet_20261106.py'), old_name]
    subprocess.run(command, cwd=ROOT, check=True)
    report = read_json(ROOT / old['output'])
    assert report['functionMatched'] == 0 and report['functionMatches'] == [] and not report.get('matches')
    assert len(report['dataMatches']) == descriptor['objects']
    assert report['dataMatchedBytes'] == descriptor['initializedBytes']
    before = copy.deepcopy(report['dataMatches'])
    evidence = []
    for row in report['dataMatches']:
        assert 'exactBytes' not in row and 'exactAfterDeclaredRelocation' not in row
        evidence.append(qualify(row))
        row['exactBytes'] = True
    assert [{k: v for k, v in r.items() if k != 'exactBytes'} for r in report['dataMatches']] == before
    pins = {p['path']: p['sha256'] for p in report['generatorSources']}
    for name in code_closure([Path(__file__).name]):
        assert name not in pins or pins[name] == sha256(ROOT / name)
        pins[name] = sha256(ROOT / name)
    report['generatorSources'] = [dict(path=p, sha256=h) for p, h in sorted(pins.items())]
    dependencies = {p['path']: p['sha256'] for p in report['replayDependencies']}
    dependencies[descriptor_name] = sha256(ROOT / descriptor_name)
    report['replayDependencies'] = [dict(path=p, sha256=h) for p, h in sorted(dependencies.items())]
    report['sdkDataRegistrationTransport'] = dict(sourceCredit=0, originalReport=old['output'],
        originalReportSha256=sha256(ROOT / old['output']), nativeDataAndFullObjectsIndependentlyRechecked=True,
        exactBytesMarkerDerivedOnlyFromCompleteObjectAndNativeAndGenuineLinkEquality=True,
        originalSourceObjectFlagsAndRelocationsUnchanged=True, evidence=evidence,
        generator=Path(__file__).name, generatorSha256=sha256(__file__))
    write_json(ROOT / descriptor['output'], report)
    print(dict(passed=True, objects=len(evidence), initializedBytes=report['dataMatchedBytes'], sourceCredit=0))


if __name__ == '__main__':
    main()
