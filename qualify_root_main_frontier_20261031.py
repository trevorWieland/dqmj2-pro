import hashlib
import re
from project import ROOT, read_json, write_json, sha256, configuration
import match_runtime as compiler
from link_runtime_unit import measured_module


def rows(value):
    pending = [value]
    skipped = {'instructions', 'reads', 'writes', 'registers', 'traces', 'cases', 'vectors', 'differential'}
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            if 'source' in item and 'sourceSha256' in item and 'compilerFlags' in item and 'address' in item:
                yield item
            pending.extend(v for k, v in item.items() if k not in skipped and isinstance(v, (dict, list)))
        elif isinstance(item, list):
            pending.extend(v for v in item if isinstance(v, (dict, list)))


def number(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, binary, symbols = measured_module('main')
    base = int(metadata['base'], 0)
    specs = {}
    for line in symbols.splitlines():
        found = re.search(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', line)
        if found:
            mode, size, address = found.groups()
            specs[(int(address, 16), mode)] = int(size, 16)
    accepted = read_json(ROOT / 'evidence/verification/accepted-cohort89-identities-v2-20261031.json')
    assert accepted['romSha256'] == config['romSha256']
    excluded = {(number(row['address']), row['mode']) for row in accepted['functions']
                if row['processor'] == 'arm9' and row['module'] == 'main' and not row.get('program')}
    excluded.add((0x0203B660, 'arm'))
    census = read_json(ROOT / 'evidence/attempts/main-near-frontier-census85-20261031.json')
    results, refusals = [], []
    seen = set()
    for candidate in census['candidates']:
        address = number(candidate['address'])
        if not (0x02000000 <= address < 0x02040000 or 0x020D0000 <= address < 0x02400000):
            continue
        if any((address, mode) in excluded for mode in ['arm', 'thumb']):
            continue
        report_path = ROOT / candidate['report']
        source = (ROOT / candidate['source']).resolve()
        if not source.is_relative_to(ROOT) or not source.is_file():
            refusals.append(dict(address=hex(address), reason='Missing/nonlocal historical source'))
            continue
        found = []
        for row in rows(read_json(report_path)):
            if number(row['address']) != address or row['source'].replace('\\', '/') != candidate['source'].replace('\\', '/'):
                continue
            if row.get('processor') != 'arm9' or row.get('module') != 'main' or row.get('program'):
                continue
            mode = row.get('mode')
            if (address, mode) not in specs or number(row['bytes']) != specs[(address, mode)]:
                continue
            size = specs[(address, mode)]
            target = binary[address - base:address - base + size]
            if row.get('targetSha256') != hashlib.sha256(target).hexdigest() or sha256(source) != row['sourceSha256']:
                continue
            if len(source.read_text(encoding='utf-8-sig').splitlines()) > 500:
                continue
            executable = row.get('compilerPath')
            if not executable:
                names = [p for p, digest in compiler.COMPILER_PINS.items() if digest == row.get('compilerSha256')]
                executable = names[0] if len(names) == 1 else None
            if executable not in compiler.COMPILER_PINS or sha256(ROOT / executable) != row['compilerSha256']:
                continue
            key = (address, mode, row['sourceSha256'], executable, tuple(row['compilerFlags']))
            if key in seen:
                continue
            seen.add(key)
            frozen = ROOT / f'nonmatching/main-runtime/20261031-qualified-main-frontier/{address:08x}-{row["sourceSha256"][:12]}/source.c'
            frozen.parent.mkdir(parents=True, exist_ok=True)
            data = source.read_bytes()
            assert not frozen.exists() or frozen.read_bytes() == data
            frozen.write_bytes(data)
            found.append(dict(romSha256=config['romSha256'], processor='arm9', program='', module='main',
                mode=mode, address=hex(address), bytes=size, source=frozen.relative_to(ROOT).as_posix(),
                sourceSha256=sha256(frozen), historicalSource=candidate['source'],
                historicalReport=candidate['report'], historicalReportSha256=sha256(report_path),
                compiler=executable, compilerSha256=row['compilerSha256'], compilerFlags=row['compilerFlags'],
                historicalCompiledBytes=row['compiledBytes'], historicalMatchingBytes=row['matchingBytes'],
                inputModuleSha256=metadata['sha256'], targetSha256=hashlib.sha256(target).hexdigest()))
        results.extend(found)
        if not found:
            refusals.append(dict(address=hex(address), reason='No current hashed/namespace-qualified/profile-pinned row'))
    results.sort(key=lambda row: (-row['historicalMatchingBytes'] / row['bytes'], -row['bytes']))
    write_json(ROOT / 'evidence/verification/root-main-qualified-frontier-20261031.json',
               dict(qualified=results, refusals=refusals, excludedAcceptedSnapshot=89,
                    pending416Excluded=True, sourceCredit=0, nativeExecutionCount=0,
                    limits=['Historical scores remain hypotheses; no fresh compilation or linking is claimed']))
    print(dict(qualifiedProfiles=len(results), identities=len({(r['address'], r['mode']) for r in results}),
               nativeBytes=sum(r['bytes'] for r in results), refused=len(refusals), sourceCredit=0))


if __name__ == '__main__':
    main()
