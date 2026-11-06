import json
import re
from pathlib import Path
import utility_code
from wave20261102_child_third_prepare import ROOT, LANE, WORK
from project import write_json, sha256


def main():
    specs = {hex(s['address']): s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main'}
    utility_code.WORK = WORK / 'self-mode-compiled'
    results, seen = [], set()
    for path in sorted((LANE / 'probes').glob('*.json')):
        report = json.loads(path.read_text())
        for entry in report.get('attempts', []):
            if not entry.get('name') or entry.get('exactAfterDeclaredRelocation') or entry.get('mode') != 'thumb':
                continue
            if not any(r['symbol'] == entry['name'] for r in entry.get('relocations', [])):
                continue
            identity = (entry['address'], entry['sourceSha256'])
            if identity in seen:
                continue
            seen.add(identity)
            spec = dict(specs[entry['address']], name='native_utility_child_arm9_thumb_%08x' % int(entry['address'], 0))
            directory = WORK / 'self-mode-sources' / ('%08x' % int(entry['address'], 0)) / entry['sourceSha256'][:12]
            directory.mkdir(parents=True, exist_ok=True)
            originals = [ROOT / entry['source'], *[ROOT / p['path'] for p in entry.get('sourceDependencies', [])]]
            copies = []
            for original in originals:
                text = re.sub(r'\b' + re.escape(entry['name']) + r'\b', spec['name'], original.read_text())
                destination = directory / original.name
                destination.write_text(text)
                copies.append(destination)
            flags = entry['compilerFlags']
            row, code = utility_code.compile_compare(copies[0], dict(spec, compilerPath=ROOT / entry['compiler']),
                flags[0][2:], flags[flags.index('-inline') + 1], 'speed' in flags)
            row.update(sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in copies[1:]],
                sourceReuseProvenance=entry.get('sourceReuseProvenance', []),
                normalizedFingerprint=entry.get('normalizedFingerprint'),
                sourceAdaptationMethod='measured Thumb recursive identity retained in actual C function symbol')
            results.append(row)
            if code is not None:
                write_json(LANE / 'candidates' / ('%08x-self-mode.json' % spec['address']), dict(match=row))
            print(dict(address=entry['address'], bytes=entry['bytes'], exact=code is not None), flush=True)
    write_json(LANE / 'self-mode-attempts.json', dict(attempts=results))


if __name__ == '__main__':
    main()
