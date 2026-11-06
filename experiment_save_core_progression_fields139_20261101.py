import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'nonmatching/save-core/20261031-progression-controller-flat-shared'
OUT = ROOT / 'nonmatching/save-core/20261101-progression-fields139'
REPORT = ROOT / 'evidence/lanes/save-core/progression-fields139-20261101.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare(name):
    texts = {
        'native_main_020c61a4.c': (OLD / 'original_local_order.c').read_text(),
        'controller_phase_three.inc': (OLD / 'controller_phase_three.inc').read_text(),
    }
    header = (OLD / 'controller_declarations.h').read_text()
    globals_to_type = {
        'state': ['native_data_021d6384'],
        'context': ['native_data_021d63c8'],
        'both': ['native_data_021d6384', 'native_data_021d63c8'],
        'payload': [],
        'array': [],
        'array_case14': [],
        'scope': [],
        'scope_case14': [],
        'typed_skill': [],
        'typed_skill_scoped': [],
    }[name]
    combined = '\n'.join(texts.values())
    for symbol in globals_to_type:
        pattern = re.compile(r'M2C_FIELD\(' + symbol + r',\s*([^,]+),\s*(0x[0-9A-Fa-f]+|[0-9]+)\)')
        fields = {}
        for match in pattern.finditer(combined):
            offset, typ = int(match[2], 0), match[1].replace('*', '').strip()
            if offset in fields and fields[offset] != typ:
                raise ValueError((symbol, offset, fields[offset], typ))
            fields[offset] = typ
        struct_name = 'Observed_' + symbol
        lines, cursor = ['typedef struct {'], 0
        for offset, typ in sorted(fields.items()):
            if offset > cursor:
                lines.append(f'    u8 unknown_{cursor:x}[{offset - cursor}];')
            lines.append(f'    {typ} field_{offset:x};')
            cursor = offset + {'s8': 1, 'u8': 1, 's32': 4, 'u32': 4}[typ]
        lines.append(f'}} {struct_name};')
        declaration = re.compile(r'extern\s+[^;\n]*\b' + symbol + r'\b[^;\n]*;')
        header, count = declaration.subn('\n'.join(lines) + f'\nextern {struct_name} {symbol};', header)
        if count != 1:
            raise ValueError((symbol, count))
        for filename, text in texts.items():
            text = pattern.sub(lambda m: symbol + '.field_' + format(int(m[2], 0), 'x'), text)
            text = re.sub(r'\b' + symbol + r'\b(?!\.)', '(&' + symbol + ')', text)
            texts[filename] = text
    if name == 'payload':
        for filename, text in texts.items():
            text = text.replace('    s8 sp1;\n    s8 sp0;', '    struct { s8 first; s8 second; } payload;')
            text = re.sub(r'\bsp0\b', 'payload.first', text)
            text = re.sub(r'\bsp1\b', 'payload.second', text)
            texts[filename] = text
    if name in ['array', 'array_case14', 'scope', 'scope_case14', 'typed_skill', 'typed_skill_scoped']:
        for filename, text in texts.items():
            text = text.replace('    s8 sp1;\n    s8 sp0;', '    u8 payload[2];')
            text = re.sub(r'\bsp0\b', 'payload[0]', text)
            text = re.sub(r'\bsp1\b', 'payload[1]', text)
            texts[filename] = text
    if name in ['scope', 'scope_case14', 'typed_skill_scoped']:
        text = texts['native_main_020c61a4.c']
        declarations = ['u8 payload[2];', 's32 numeric_value;', 'u8 table_index;',
                        'u32 temp_r5;', 'u32 temp_r0_2;']
        for declaration in declarations:
            assert text.count('    ' + declaration + '\n') == 1
            text = text.replace('    ' + declaration + '\n', '')
        text = text.replace('    case 0:\n', '    case 0: {\n' + '\n'.join('        ' + d for d in declarations) + '\n', 1)
        boundary = '        native_data_020e2e50 = -1U;\n        break;\n    case 1:'
        assert text.count(boundary) == 1
        text = text.replace(boundary, '        native_data_020e2e50 = -1U;\n        break;\n    }\n    case 1:')
        texts['native_main_020c61a4.c'] = text
    if name.startswith('typed_skill'):
        header = header.replace('extern u32 native_fn_02062e44();',
                                'typedef struct { u8 skill; u8 allocated; } ObservedSavedSkill;\n'
                                'extern u32 native_fn_02062e44(u32, s32, const ObservedSavedSkill *);')
        assert 'const ObservedSavedSkill *' in header
        for filename, text in texts.items():
            text = text.replace('u8 payload[2];', 'ObservedSavedSkill payload;')
            text = text.replace('payload[0]', 'payload.skill').replace('payload[1]', 'payload.allocated')
            text = text.replace('&payload.skill', '&payload')
            texts[filename] = text
    if name.endswith('_case14'):
        text = texts['native_main_020c61a4.c']
        text = text.replace('    default:\n        break;', '    default:\n        break;\n    case 14:\n        break;', 1)
        texts['native_main_020c61a4.c'] = text
    directory = OUT / name
    directory.mkdir(parents=True, exist_ok=True)
    texts['controller_declarations.h'] = header
    for filename, text in texts.items():
        if len(text.splitlines()) > 500:
            raise ValueError(filename)
        (directory / filename).write_text(text, newline='\n')


def worker(name):
    module = load('historical_fields139', ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    baseline = json.loads((ROOT / 'evidence/lanes/save-core/progression-controller-flat-shared-20261031.json').read_text())
    module.MODULE, module.MODE = 'main', 'arm'
    module.ENTRY, module.LENGTH = 0x020C61A4, 3744
    module.NAME = 'native_main_020c61a4'
    module.SOURCE = (OUT / name / 'native_main_020c61a4.c').relative_to(ROOT).as_posix()
    module.WORK = 'work/save-core/progression-fields139/' + name
    module.COMPILER = baseline['compilerPath']
    module.COMPILER_HASH = baseline['compilerSha256']
    module.FLAGS = baseline['flags']
    entry_module = load('fields139_entries', ROOT / 'match_mechanics_save_20261031_lane_pointer_sequence.py')
    cache = {}
    entry = entry_module.native_entry('main', 0x020C61A4, cache)
    metadata, binary, _ = cache['main']
    start = 0x020C61A4 - int(metadata['base'], 0)
    native = binary[start:start + 3744]
    assert sha(native) == entry['nativeSpanSha256']
    try:
        row, body = module.build(native)
        result = {'variant': name, 'row': row, 'nativeSha256': sha(native), 'bodySha256': sha(body)}
    except Exception as exc:
        result = {'variant': name, 'error': str(exc), 'errorType': type(exc).__name__}
    (OUT / name / 'result.json').write_text(json.dumps(result, indent=2) + '\n')


def run():
    names = ['state', 'context', 'both', 'payload', 'array', 'array_case14', 'scope', 'scope_case14',
             'typed_skill', 'typed_skill_scoped']
    for name in names:
        prepare(name)
    def command(name):
        return subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', name], cwd=ROOT,
                              capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        outputs = list(pool.map(command, names))
    rows = []
    for name, output in zip(names, outputs):
        if output.returncode:
            rows.append({'variant': name, 'error': output.stderr, 'exitCode': output.returncode})
        else:
            rows.append(json.loads((OUT / name / 'result.json').read_text()))
    archive = ROOT / 'evidence/vectors/save-core-progression-fields139-20261101.json.gz'
    raw = (json.dumps({'schema': 1, 'rows': rows}, indent=2) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    archive.write_bytes(packed)
    compact = []
    for entry in rows:
        row = entry.get('row', {})
        compact.append(dict(variant=entry['variant'], error=entry.get('error'),
                            source=row.get('source'), sourceSha256=row.get('sourceSha256'),
                            compiledBytes=row.get('compiledBytes'), sameOffsetBytes=row.get('sameOffsetBytes'),
                            exactByteEqual=row.get('exactByteEqual'), objectSha256=row.get('objectSha256'),
                            linkedBinarySha256=row.get('linkedBinarySha256'), sourceCredit=0))
    REPORT.write_text(json.dumps({'schema': 1, 'scope': 'zero-credit ordinary-C field/layout hypotheses',
                                 'address': 0x020C61A4, 'nativeBytes': 3744, 'rows': compact,
                                 'fullProvenanceSidecar': dict(path=archive.relative_to(ROOT).as_posix(),
                                     sha256=sha(packed), compressedBytes=len(packed),
                                     uncompressedSha256=sha(raw), uncompressedBytes=len(raw), contexts=len(rows))}, indent=2) + '\n')
    for row in rows:
        value = row.get('row', {})
        print(json.dumps({'variant': row['variant'], 'error': row.get('error'),
                          'compiledBytes': value.get('compiledBytes'), 'matchingBytes': value.get('sameOffsetBytes'),
                          'exactBytes': value.get('exactByteEqual')}))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        worker(sys.argv[2])
    else:
        run()
