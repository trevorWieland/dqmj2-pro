import hashlib
import json
import re
import subprocess
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from initialized_storage_protection_v2_20261106 import protected


REVISION = 'fa2ba9a799e1eed41c3bca98e4ffebb290ccca29'


def identity(row, parent=None):
    parent = parent or {}
    module = row.get('module', parent.get('module'))
    program = row.get('program', parent.get('program')) or ''
    return program, row.get('processor', parent.get('processor')), module, row['mode'], int(row['address'], 0)


def fingerprint(data, offsets):
    result = bytearray(data)
    for offset in offsets:
        assert 0 <= offset <= len(data) - 4
        result[offset:offset + 4] = bytes(4)
    return hashlib.sha256(result).hexdigest()


def main():
    native_dependencies(configuration())
    from elftools.elf.elffile import ELFFile
    raw = subprocess.check_output(['git', 'show', REVISION + ':ledger/functions.jsonl'], cwd=ROOT)
    functions = [json.loads(line) for line in raw.splitlines()]
    manifest_raw = subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT)
    manifest = json.loads(manifest_raw)
    modules = {}
    for row in manifest['modules']:
        if row['processor'] != 'arm7':
            continue
        assert sha256(ROOT / row['binary']) == row['sha256']
        namespace = (row.get('program') or '', row['processor'], row['name'])
        intervals, pins = protected(namespace, REVISION)
        modules[namespace] = dict(metadata=row, image=(ROOT / row['binary']).read_bytes(),
                                  intervals=intervals, protectionPins=pins)
    targets = [r for r in functions if r['processor'] == 'arm7' and not r['states']['functionMatched']]
    target_starts = {}
    for row in functions:
        if row['processor'] == 'arm7':
            key = identity(row)
            target_starts.setdefault(key[:3], set()).add(key[4])
    reports, origins, inputs, skipped, seen = {}, [], {}, {}, set()
    for row in functions:
        if row['processor'] != 'arm7' or not row['states']['functionMatched'] or not row['sourceUnit'].endswith('.c'):
            continue
        name = row['evidence']
        if name not in reports:
            reports[name] = read_json(ROOT / name)
            inputs[name] = sha256(ROOT / name)
        report = reports[name]
        selected = [r for r in report.get('matches', []) if identity(r, report) == identity(row)]
        if len(selected) != 1:
            skipped['ambiguous-report-row'] = skipped.get('ambiguous-report-row', 0) + 1
            continue
        entry = selected[0]
        size = row['bytes']
        if entry.get('ordinaryCBytes') != size or entry.get('justifiedAssemblyBytes') != 0:
            continue
        if not 24 <= size <= 8192 or not isinstance(entry.get('sectionIndex'), int):
            continue
        assert entry['source'] == row['sourceUnit'] and entry['object'] == row['object']
        assert sha256(ROOT / entry['source']) == entry['sourceSha256'] == row['sourceSha256']
        assert sha256(ROOT / entry['object']) == entry['objectSha256'] == row['objectSha256']
        if re.search(r'\b(?:asm|__asm|__asm__)\b', (ROOT / entry['source']).read_text(encoding='utf-8-sig')):
            continue
        relocations = entry.get('relocations', [])
        if any(r['type'] not in [1, 2, 10, 28, 29] for r in relocations):
            continue
        offsets = tuple(sorted({r['offset'] for r in relocations}))
        if size - len(offsets) * 4 < 12:
            continue
        with (ROOT / entry['object']).open('rb') as stream:
            elf = ELFFile(stream)
            section = elf.get_section(entry['sectionIndex']).data()
            start = entry.get('sectionOffset', 0)
            body = section[start:start + size]
        assert len(body) == size
        digest = fingerprint(body, offsets)
        key = (row['mode'], size, offsets, digest)
        if key in seen:
            continue
        seen.add(key)
        origins.append(dict(entry=entry, mode=row['mode'], bytes=size, offsets=offsets, fingerprint=digest))
    hits, rejected_inside = [], 0
    for row in targets:
        key = identity(row)
        module = modules[key[:3]]
        address = key[4]
        offset = address - int(module['metadata']['base'], 0)
        for origin in origins:
            size = origin['bytes']
            if row['mode'] != origin['mode'] or offset < 0 or offset + size > len(module['image']):
                continue
            if any(max(address, a) < min(address + size, b) for a, b in module['intervals']):
                continue
            if any(address < a < address + size for a in target_starts[key[:3]]):
                rejected_inside += 1
                continue
            native = module['image'][offset:offset + size]
            if fingerprint(native, origin['offsets']) != origin['fingerprint']:
                continue
            entry = origin['entry']
            hits.append(dict(program=key[0], processor=key[1], module=key[2], mode=key[3], address=hex(address),
                candidateBytes=size, targetSha256=hashlib.sha256(native).hexdigest(),
                originSource=entry['source'], originSourceSha256=entry['sourceSha256'],
                originObject=entry['object'], originObjectSha256=entry['objectSha256'],
                maskedRelocationOffsets=list(origin['offsets']), sourceCredit=0,
                boundaryProven=False, interfaceAndGenuineLinkProven=False))
    assert all(sha256(ROOT / p) == h for p, h in inputs.items())
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/arm7-source-reuse-next/inventory.json',
        dict(passed=True, sourceCredit=0, sourceOwnershipGranted=False, sourceRevision=REVISION,
             ledgerSha256=hashlib.sha256(raw).hexdigest(), manifestSha256=hashlib.sha256(manifest_raw).hexdigest(),
             pinnedReports=inputs, acceptedDistinctOrdinaryCObjectSpans=len(origins),
             unknownExtentStartsExamined=len(targets), skipped=skipped, knownInteriorEntryComparisonsRejected=rejected_inside,
             candidateMatches=hits, nativeInputs=[dict(path=v['metadata']['binary'], sha256=v['metadata']['sha256']) for v in modules.values()],
             protectionPins=[dict(namespace=list(k), pins=v['protectionPins']) for k, v in modules.items()],
             generatorSha256=sha256(__file__), limitations=[
                 'Read-only accepted ARM7 C object spans at recorded unaccepted heuristic entry points.',
                 'Only declared relocation words are ignored; no recompilation, ownership or source acceptance.',
                 'A candidate extent inherited from an origin is not a proven target function boundary.',
                 'Types, relocation targets, literal suffix, original ROM lineage, genuine links and copied-root controls remain required.']))
    print(dict(origins=len(origins), unknownExtentStarts=len(targets), candidates=len(hits), sourceCredit=0))


if __name__ == '__main__':
    main()
