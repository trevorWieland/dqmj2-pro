import ast
import hashlib
import json
import re
import struct
import subprocess
from project import ROOT, read_json, write_json, sha256


REVISION = 'af5a4bd4f100fe5a727824a00a21e0ae3442b1a6'
TYPES = {'u8': (1, False), 's8': (1, True), 'u16': (2, False), 's16': (2, True),
         'u32': (4, False), 's32': (4, True), 'fx16': (2, True), 'fx32': (4, True)}


def extent(expression):
    def number(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Mult):
            left, right = number(node.left), number(node.right)
            return left + right if isinstance(node.op, ast.Add) else left * right
        raise ValueError('Nonliteral array bound')
    return number(ast.parse(expression, mode='eval').body)


def arrays(text):
    text = re.sub(r'/\*[\s\S]*?\*/|//[^\n]*', '', text)
    pattern = r'\bconst\s+(' + '|'.join(TYPES) + r')\s+(\w+)\s*\[([^\]]*)\]\s*=\s*\{([^{}]*)\}\s*;'
    for match in re.finditer(pattern, text):
        type_name, symbol, count, body = match.groups()
        body = re.sub(r'\((?:' + '|'.join(TYPES) + r')\)', '', body)
        fields = body.strip().rstrip(',').split(',')
        if not fields or not all(re.fullmatch(r'\s*[+-]?(?:0[xX][0-9a-fA-F]+|\d+)[uUlL]*\s*', value) for value in fields):
            continue
        values = [int(re.sub(r'[uUlL]+$', '', value.strip()), 0) if 'x' in value.lower()
                  else int(re.sub(r'[uUlL]+$', '', value.strip()), 10) for value in fields]
        try:
            declared = extent(count) if count.strip() else len(values)
        except (ValueError, SyntaxError):
            continue
        if declared != len(values) or len(set(values)) < 8:
            continue
        width, signed = TYPES[type_name]
        if declared * width < 64:
            continue
        if any(not -(1 << (width * 8 - 1)) <= value < (1 << (width * 8)) for value in values):
            continue
        payload = b''.join((value & ((1 << (width * 8)) - 1)).to_bytes(width, 'little') for value in values)
        yield dict(symbol=symbol, type=type_name, declaredElements=declared, bytes=len(payload),
                   distinctValues=len(set(values)), initializerOffset=match.start()), payload


def main():
    manifest_raw = subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT)
    manifest = json.loads(manifest_raw)
    frontier_name = 'evidence/verification/source95-frontier-closed162-20261106.json'
    frontier = read_json(ROOT / frontier_name)
    assert frontier['sourceRevision'] == REVISION and frontier['sourceBytes'] == 1035817
    regions = [row for row in frontier['investigationProposals'] if row['knownGhidraBodyBytes'] == 0]
    inputs, modules = {}, []
    for row in manifest['modules']:
        path = ROOT / row['binary']
        assert sha256(path) == row['sha256']
        modules.append((row, path.read_bytes()))
    references = [ROOT / 'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840',
                  ROOT / 'deps/reference/nitro-10e447b8']
    candidates, exact, protected_hits = [], [], []
    for directory in references:
        for path in sorted(directory.rglob('*.c')):
            source = path.read_text(encoding='utf-8-sig', errors='strict')
            for descriptor, payload in arrays(source):
                inputs[path.relative_to(ROOT).as_posix()] = sha256(path)
                candidate = dict(descriptor, source=path.relative_to(ROOT).as_posix(), sourceSha256=sha256(path),
                                 initializerSha256=hashlib.sha256(payload).hexdigest())
                candidates.append(candidate)
                for module, image in modules:
                    start = 0
                    while True:
                        offset = image.find(payload, start)
                        if offset < 0:
                            break
                        start = offset + 1
                        address = int(module['base'], 0) + offset
                        scope = (module.get('program') or '', module['processor'], module['name'])
                        witnesses = [r for r in regions if (r['program'], r['processor'], r['module']) == scope
                                     and int(r['address'], 0) <= address and address + len(payload) <= int(r['endExclusive'], 0)]
                        row = dict(candidate, program=scope[0], processor=scope[1], module=scope[2],
                                   address=hex(address), endExclusive=hex(address + len(payload)), sourceCredit=0,
                                   sourceOwnershipGranted=False, moduleSha256=module['sha256'])
                        (exact if witnesses else protected_hits).append(row)
    assert all(sha256(ROOT / path) == digest for path, digest in inputs.items())
    unique = {}
    for row in exact:
        key = (row['program'], row['processor'], row['module'], row['address'], row['bytes'])
        if key not in unique:
            unique[key] = dict(row, additionalReferenceWitnesses=[])
        else:
            unique[key]['additionalReferenceWitnesses'].append(dict(source=row['source'], sourceSha256=row['sourceSha256'], symbol=row['symbol']))
    directory = ROOT / 'evidence/lanes/parallel-wave20261106/sdk-constant-arrays-inspection'
    write_json(directory / 'inventory.json', dict(passed=True, sourceCredit=0, sourceOwnershipGranted=False,
        sourceRevision=REVISION, sourceManifestSha256=hashlib.sha256(manifest_raw).hexdigest(),
        frontierSha256=sha256(ROOT / frontier_name), examinedModules=len(modules),
        examinedTypedInitializers=len(candidates), referenceInputs=inputs,
        unprotectedReadOnlyCandidates=exact, protectedOrUnqualifiedExtentHits=protected_hits,
        distinctCandidateSourceBytes=sum(r['bytes'] for r in unique.values()), uniquePhysicalCandidates=list(unique.values()),
        referenceMatchBytesIncludingDuplicates=sum(r['bytes'] for r in exact), generatorSha256=sha256(__file__),
        limitations=['Literal integer constant initializers only; preprocessor context and native consumers still require review.',
                    'No source ownership, compiler execution, source files, claims or accepted credit.',
                    'A full match must fit a zero-recorded-body inspection range excluding positive function/claim/admitted storage.',
                    'Identical bytes alone do not establish source provenance, complete data boundaries or interpretation.']))
    print(dict(initializers=len(candidates), unprotectedCandidates=len(exact),
               candidateBytes=sum(r['bytes'] for r in exact), protectedHits=len(protected_hits), sourceCredit=0))


if __name__ == '__main__':
    main()
