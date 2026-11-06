import ast
import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256
from inspect_sdk_constant_arrays_20261106 import arrays, TYPES


REVISION = 'af5a4bd4f100fe5a727824a00a21e0ae3442b1a6'
SDK = 'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/'
SOURCE = SDK + 'libraries/snd/src/snd_util.c'
HEADER = SDK + 'include/nitro/snd/common/util.h'
OUTPUT = 'evidence/lanes/parallel-wave20261106/sdk-sound-constants-inspection/inventory.json'


def resolve(expression, definitions, active=()):
    def number(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.Name):
            assert node.id in definitions and node.id not in active
            return resolve(definitions[node.id], definitions, active + (node.id,))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = number(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.LShift)):
            left, right = number(node.left), number(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            assert 0 <= right <= 32
            return left << right
        raise ValueError('Unsupported SDK constant expression')
    return number(ast.parse(expression.strip(), mode='eval').body)


def candidates(source, header):
    definitions = dict(re.findall(r'^\s*#define\s+([A-Z][A-Z0-9_]+)\s+([^\r\n]+)', header, re.M))
    clean = re.sub(r'/\*[\s\S]*?\*/|//[^\n]*', '', source)
    pattern = r'\bconst\s+(' + '|'.join(TYPES) + r')\s+(\w+)\s*\[([^\]]+)\]\s*=\s*\{([^{}]*)\}\s*;'
    for match in re.finditer(pattern, clean):
        type_name, symbol, expression, body = match.groups()
        count = resolve(expression, definitions)
        assert 0 < count <= 65536
        rendered = f'const {type_name} {symbol}[{count}] = {{{body}}};'
        found = list(arrays(rendered))
        if found:
            assert len(found) == 1
            descriptor, payload = found[0]
            descriptor.update(declaredBound=expression, resolvedBound=count,
                              initializerOffsetInCommentStrippedSource=match.start())
            yield descriptor, payload


def main():
    source_pin, header_pin = sha256(ROOT / SOURCE), sha256(ROOT / HEADER)
    source = (ROOT / SOURCE).read_text(encoding='utf-8-sig')
    header = (ROOT / HEADER).read_text(encoding='utf-8-sig')
    assert '#include <nitro/snd/common/util.h>' in source
    manifest_raw = subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT)
    manifest = json.loads(manifest_raw)
    frontier = read_json(ROOT / 'evidence/verification/source95-frontier-closed162-20261106.json')
    assert frontier['sourceRevision'] == REVISION
    regions = [row for row in frontier['investigationProposals'] if row['knownGhidraBodyBytes'] == 0]
    tables = list(candidates(source, header))
    hits, native_inputs = [], []
    for module in manifest['modules']:
        path = ROOT / module['binary']
        assert sha256(path) == module['sha256']
        native_inputs.append(dict(path=module['binary'], sha256=module['sha256']))
        image = path.read_bytes()
        scope = (module.get('program') or '', module['processor'], module['name'])
        for descriptor, payload in tables:
            offset = image.find(payload)
            while offset >= 0:
                address = int(module['base'], 0) + offset
                witnesses = [r for r in regions if (r['program'], r['processor'], r['module']) == scope
                             and int(r['address'], 0) <= address and address + len(payload) <= int(r['endExclusive'], 0)]
                hits.append(dict(descriptor, program=scope[0], processor=scope[1], module=scope[2],
                                 address=hex(address), endExclusive=hex(address + len(payload)),
                                 payloadSha256=hashlib.sha256(payload).hexdigest(),
                                 fitsZeroRecordedBodyInspectionRange=bool(witnesses), sourceCredit=0))
                offset = image.find(payload, offset + 1)
    assert source_pin == sha256(ROOT / SOURCE) and header_pin == sha256(ROOT / HEADER)
    write_json(ROOT / OUTPUT, dict(passed=True, sourceCredit=0, sourceOwnershipGranted=False,
        sourceRevision=REVISION, source=SOURCE, sourceSha256=source_pin, header=HEADER,
        headerSha256=header_pin, nativeInputs=native_inputs, examinedModules=len(native_inputs),
        typedTables=[row for row, payload in tables], completeNativeHits=hits,
        candidateBytes=sum(r['bytes'] for r in hits if r['fitsZeroRecordedBodyInspectionRange']),
        generatorSha256=sha256(__file__), limitations=[
            'Header macro arithmetic is read-only inspection, not complete SDK preprocessing.',
            'No ownership, source generation, compiler execution or accepted credit.',
            'Current source, claims, data storage and native consumers require separate admission.']))
    print(dict(tables=len(tables), hits=len(hits), candidateBytes=sum(
        r['bytes'] for r in hits if r['fitsZeroRecordedBodyInspectionRange']), sourceCredit=0))


if __name__ == '__main__':
    main()
