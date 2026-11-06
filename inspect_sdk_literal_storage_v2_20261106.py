import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256
from inspect_sdk_constant_arrays_20261106 import TYPES, extent


REVISION = 'fa2ba9a799e1eed41c3bca98e4ffebb290ccca29'
REFERENCES = ['deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840',
              'deps/reference/nitro-10e447b8',
              'deps/reference/NitroSystem-d636fb5d2b212e8736f09859fff447be2bd0ac85']


def arrays(source):
    clean = re.sub(r'/\*[\s\S]*?\*/|//[^\n]*', '', source)
    pattern = r'\b(?:static\s+)?(?:const\s+)?(' + '|'.join(TYPES) + r')\s+(\w+)\s*\[([^\]]*)\]\s*=\s*\{([^{}]*)\}\s*;'
    for match in re.finditer(pattern, clean):
        kind, symbol, bound, body = match.groups()
        fields = body.strip().rstrip(',').split(',')
        if not fields or not all(re.fullmatch(r'\s*[+-]?(?:0[xX][0-9a-fA-F]+|\d+)[uUlL]*\s*', v) for v in fields):
            continue
        values = [int(re.sub(r'[uUlL]+$', '', v.strip()), 16 if 'x' in v.lower() else 10) for v in fields]
        try:
            count = extent(bound) if bound.strip() else len(values)
        except (ValueError, SyntaxError):
            continue
        width, signed = TYPES[kind]
        if count != len(values) or not 64 <= count * width <= 262144 or len(set(values)) < 8:
            continue
        if not all(-(1 << (width * 8 - 1)) <= v < (1 << (width * 8)) for v in values):
            continue
        payload = b''.join((v & ((1 << (width * 8)) - 1)).to_bytes(width, 'little') for v in values)
        yield dict(symbol=symbol, elementType=kind, elementCount=count, bytes=len(payload),
                   initializerOffsetInCommentStrippedSource=match.start()), payload


def main():
    raw = subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT)
    manifest = json.loads(raw)
    frontier_name = 'evidence/verification/source95-frontier-closed164-20261106.json'
    frontier = read_json(ROOT / frontier_name)
    assert frontier['sourceRevision'] == REVISION
    regions = [r for r in frontier['investigationProposals'] if r['knownGhidraBodyBytes'] == 0]
    modules = []
    for row in manifest['modules']:
        assert sha256(ROOT / row['binary']) == row['sha256']
        modules.append((row, (ROOT / row['binary']).read_bytes()))
    inputs, complete, qualified, missed = {}, [], [], []
    examined = 0
    for reference in REFERENCES:
        for path in sorted((ROOT / reference).rglob('*')):
            if path.suffix.lower() not in ('.c', '.h') or not path.is_file():
                continue
            try:
                source = path.read_text(encoding='utf-8-sig')
            except UnicodeDecodeError:
                continue
            candidates = list(arrays(source))
            if not candidates:
                continue
            name = path.relative_to(ROOT).as_posix()
            inputs[name] = sha256(path)
            for descriptor, payload in candidates:
                examined += 1
                found = False
                for module, image in modules:
                    offset = image.find(payload)
                    while offset >= 0:
                        found = True
                        address = int(module['base'], 0) + offset
                        namespace = (module.get('program') or '', module['processor'], module['name'])
                        witnesses = [r for r in regions if (r['program'], r['processor'], r['module']) == namespace
                                     and int(r['address'], 0) <= address
                                     and address + len(payload) <= int(r['endExclusive'], 0)]
                        hit = dict(descriptor, source=name, sourceSha256=inputs[name],
                                   payloadSha256=hashlib.sha256(payload).hexdigest(), program=namespace[0],
                                   processor=namespace[1], module=namespace[2], address=hex(address),
                                   moduleSha256=module['sha256'], fitsZeroRecordedBodyInspectionRange=bool(witnesses))
                        complete.append(hit)
                        if witnesses:
                            qualified.append(hit)
                        offset = image.find(payload, offset + 1)
                if not found:
                    missed.append(dict(descriptor, source=name, sourceSha256=inputs[name],
                                       payloadSha256=hashlib.sha256(payload).hexdigest()))
    assert all(sha256(ROOT / p) == h for p, h in inputs.items())
    unique = {(r['program'], r['processor'], r['module'], r['address'], r['bytes']): r for r in qualified}
    output = 'evidence/lanes/parallel-wave20261106/sdk-literal-storage-next/inventory.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, sourceOwnershipGranted=False,
        sourceRevision=REVISION, manifestSha256=hashlib.sha256(raw).hexdigest(),
        frontier=frontier_name, frontierSha256=sha256(ROOT / frontier_name), referenceInputs=inputs,
        nativeInputs=[dict(path=m['binary'], sha256=m['sha256']) for m, _ in modules],
        examinedLiteralArrays=examined, completeNativeHits=complete,
        uniquePhysicalCandidates=list(unique.values()),
        candidateBytes=sum(r['bytes'] for r in unique.values()), absentCompleteInitializers=missed,
        generatorSha256=sha256(__file__), limitations=[
            'Read-only literal integer initializer inspection; no preprocessor expansion or ownership.',
            'Header and non-const initializers are comparative witnesses, not formal native types.',
            'Complete payload identity is mandatory; no partial-array or zero-run source credit.',
            'Admission still requires current code/storage exclusion, independent ROM lineage and semantic/native-consumer review.']))
    print(dict(examined=examined, completeNativeHits=len(complete), candidates=len(unique),
               candidateBytes=sum(r['bytes'] for r in unique.values()), sourceCredit=0))


if __name__ == '__main__':
    main()
