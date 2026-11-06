import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import crossreuse_utility_c as cross
import reuse_utility_c as reuse
import utility_code
import match_lowlevel
from wave20261102_child_third_prepare import ROOT, LANE, WORK
from wave20261102_child_third_adapt import validate_candidate, closure
from project import write_json, sha256

SPECS = []


def probe(origin):
    key = utility_code.utility_runtime.sha((origin['source'] + origin['name']).encode())[:16]
    result_path = LANE / 'probes' / (key + '.json')
    if result_path.exists():
        return json.loads(result_path.read_text())
    result = dict(source=origin['source'], sourceSha256=origin['sourceSha256'], name=origin['name'], attempts=[], matches=[])
    try:
        paths, unused = closure(ROOT / origin['source'])
        result['originIncludeClosure'] = [dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in paths]
    except Exception as error:
        result['failure'] = str(error)
        write_json(result_path, result)
        return result
    by_size = defaultdict(list)
    for spec in SPECS:
        by_size[spec['bytes']].append(spec)
    for profile, optimization, speed, inline in [('1.2/sp4', '4,p', False, 'on,noauto'), ('1.2/base', 2, False, 'off')]:
        compiler = ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')
        flags = match_lowlevel.FLAGS[:]
        flags[0] = '-O' + str(optimization)
        flags[flags.index('-inline') + 1] = inline
        flags.append('-thumb')
        directory = WORK / 'origin-probes' / key / profile.replace('/', '_')
        directory.mkdir(parents=True, exist_ok=True)
        try:
            attempt, compiled = cross.compile_origin(origin, compiler, flags, directory)
            result['attempts'].append(attempt)
            if compiled is None:
                continue
            derived, offsets, payload = compiled
            fingerprint = reuse.normalized(payload, offsets)
            for spec in by_size.get(len(payload), []):
                if spec['mode'] != 'thumb':
                    continue
                binary = (ROOT / spec['binary']).read_bytes()
                first = spec['address'] - spec['base']
                native = binary[first:first + spec['bytes']]
                if reuse.normalized(native, offsets) != fingerprint:
                    continue
                tag = key + '-' + profile.replace('/', '_')
                try:
                    row, code = validate_candidate(derived, spec, native, tag)
                    row['normalizedFingerprint'] = fingerprint
                    row['originProbe'] = dict(object=derived['probeObject'], objectSha256=derived['probeObjectSha256'],
                        source=origin['source'], sourceSha256=origin['sourceSha256'], compiler=derived['compiler'],
                        compilerSha256=derived['compilerSha256'], compilerFlags=derived['compilerFlags'])
                    result['attempts'].append(row)
                    if code is not None:
                        result['matches'].append(row)
                        write_json(LANE / 'candidates' / ('%08x-%s.json' % (spec['address'], key)),
                            dict(match=row, bytes=spec['bytes'], address=hex(spec['address']),
                                 sourceAdaptationOnly=True, acceptedSourceCredit=0))
                        print(dict(address=hex(spec['address']), bytes=spec['bytes'], exact=True,
                                   origin=origin['source'], profile=profile), flush=True)
                except Exception as error:
                    result['attempts'].append(dict(address=hex(spec['address']), fingerprintMatched=True, failure=str(error)))
        except Exception as error:
            result['attempts'].append(dict(profile=profile, failure=str(error)))
    write_json(result_path, result)
    return result


def main():
    global SPECS
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--all-origins', action='store_true')
    args = parser.parse_args()
    wanted = {int(e['address'], 0) for e in json.loads((LANE / 'claim.json').read_text())['functions']}
    SPECS = [s for s in utility_code.candidates() if s['module'] == 'utility-child-arm9-main' and s['address'] in wanted]
    utility_code.WORK = WORK / 'adapted-compiled'
    for profile in ['1.2/sp4', '1.2/base']:
        compiler = ROOT / ('tools/mwccarm/mwccarm/' + profile + '/mwccarm.exe')
        if sha256(compiler) != utility_code.compiler_pins().get(compiler.relative_to(ROOT).as_posix()):
            raise ValueError('Cross-compiler pin differs')
    origins = json.loads((LANE / 'origin-catalog.json').read_text())['origins']
    selected, normalized = [], set()
    for origin in sorted(origins, key=lambda e: (-e.get('bytes', e.get('size', 0)), e['source'])):
        if not origin.get('name'):
            continue
        if not args.all_origins and (origin.get('module') != 'main' or not 0x02000000 <= int(origin['address'], 0) < 0x02040000):
            continue
        text = (ROOT / origin['source']).read_text()
        pattern = re.sub(r'\b[A-Za-z_][A-Za-z_0-9]*_[0-9a-f]{8}\b', 'relocated', text)
        identity = utility_code.utility_runtime.sha(re.sub(r'\s+', ' ', pattern).encode())
        if identity in normalized:
            continue
        normalized.add(identity)
        selected.append(origin)
    if args.limit:
        selected = selected[:args.limit]
    suffix = '-all' if args.all_origins else ''
    write_json(LANE / ('crosscompile-selection' + suffix + '.json'), dict(origins=len(selected), targetFunctions=len(SPECS),
        largerUnitsFirst=True, compilerProfiles=['1.2/sp4 -O4,p', '1.2/base -O2'],
        sourcePins=[dict(path=e['source'], sha256=e['sourceSha256']) for e in selected]))
    print(dict(selectedOrigins=len(selected), targets=len(SPECS)), flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(probe, selected))
    found = {e['address']: e for result in results for e in result['matches']}
    write_json(LANE / ('crosscompile-summary' + suffix + '.json'), dict(origins=len(results), exactFunctions=len(found),
        exactBytes=sum(e['bytes'] for e in found.values()), acceptedSourceCredit=0))
    print(dict(origins=len(results), exactFunctions=len(found), exactBytes=sum(e['bytes'] for e in found.values())))


if __name__ == '__main__':
    main()
