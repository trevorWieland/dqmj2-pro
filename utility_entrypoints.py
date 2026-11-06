import json
import struct
from pathlib import Path
import utility_runtime

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'evidence/utility/loader-entrypoints.json'


def derive(layout=None, files=None):
    if layout is None or files is None:
        layout, files = utility_runtime.derive()
    child = bytes(files[ROOT / 'extract/utility/child.srl'])
    callback = struct.unpack_from('<I', child, 0x70)[0]
    if callback != 0x02000AC4:
        raise ValueError('Measured embedded ARM9 autoload callback changed')
    module = next(module for module in layout['modules'] if module['id'] == 'utility-child-arm9-main')
    binary = bytes(files[ROOT / module['binary']])
    start, size = 0x02000A4C, 124
    offset = start - int(module['base'], 0)
    span = binary[offset:offset + size]
    if span[-4:] != bytes.fromhex('1eff2fe1'):
        raise ValueError('Embedded loader callback no longer has the measured ARM BX-LR body')
    report_path = ROOT / 'evidence/matches/utility-arm9-startup01.json'
    report = json.loads(report_path.read_text())
    parent = next(entry for entry in report['matches'] if int(entry['address'], 0) == start and entry['module'] == module['id'])
    if parent['bytes'] != size or parent['inputModuleSha256'] != module['sha256'] or parent['targetSha256'] != utility_runtime.sha(span):
        raise ValueError('Loader entry association is not inside the accepted native startup unit')
    if utility_runtime.sha((ROOT / parent['source']).read_bytes()) != parent['sourceSha256']:
        raise ValueError('Loader parent source identity changed')
    association = {'program': utility_runtime.PROGRAM, 'processor': 'arm9', 'module': module['id'], 'address': hex(callback), 'mode': 'arm',
                   'symbol': 'native_utility_child_arm9_arm_02000ac4', 'kind': 'interior-autoload-completion-callback', 'bytes': 4,
                   'headerReference': {'offset': '0x70', 'bytes': 4, 'value': hex(callback), 'childSha256': layout['child']['sha256']},
                   'parentUnit': {'address': hex(start), 'bytes': size, 'name': parent['name'], 'report': report_path.relative_to(ROOT).as_posix(),
                                  'targetSha256': parent['targetSha256'], 'source': parent['source'], 'sourceSha256': parent['sourceSha256']},
                   'inputModuleSha256': module['sha256'], 'nativeSpanSha256': utility_runtime.sha(span[-4:]), 'offsetWithinParent': callback - start,
                   'ordinaryFunctionCredit': 0, 'separateSourceByteCredit': 0, 'excludeFromOrdinaryFunctionBacklog': True,
                   'reason': 'The header-referenced callback is a globally named interior entry in the accepted 124-byte autoload unit; crediting another ordinary function would overlap that source span'}
    return {'schemaVersion': 1, 'romSha256': layout['romSha256'], 'program': utility_runtime.PROGRAM, 'entryPointAssociations': [association],
            'limitations': ['This is a measured entry association and overlap exclusion, not separate source or ordinary-function credit']}


def publish():
    report = derive()
    OUTPUT.write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    report = publish()
    print({'qualifiedInteriorEntries': len(report['entryPointAssociations']), 'ordinaryFunctionCredit': 0})
