import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import match_runtime
import crossreuse_utility_c
import link_arm7_bulk_20261030 as linker
from elftools.elf.elffile import ELFFile
from project import ROOT, sha256, write_json

PROFILE = ROOT / 'nonmatching/arm7-bulk/20261101/lane-child-callback16-c-v2/profile.json'
WORK = ROOT / 'work/arm7-bulk-20261030/lane-child-callback16-c-113'
PROFILES = [('1.2/sp2p3', 0, 'space'), ('2.0/base', 0, 'space')]


def worker(index):
    row = json.loads(PROFILE.read_text())['results'][index]
    if sha256(ROOT / row['source']) != row['sourceSha256']:
        raise ValueError('Typed full SPI source changed')
    original = (ROOT / row['binary']).read_bytes()
    offset = int(row['address'], 0) - row['base']
    native = original[offset:offset + row['bytes']]
    origin = {key: row[key] for key in ('source', 'sourceSha256', 'name')}
    results = []
    for version, optimization, goal in PROFILES:
        flags = match_runtime.FLAGS[:]
        flags[0] = '-O' + str(optimization)
        flags[flags.index('-proc') + 1] = 'arm7tdmi'
        flags[flags.index('-inline') + 1] = 'all'
        flags[flags.index('-sym') + 1] = 'off'
        flags += ['-lang', 'c99', '-opt', goal]
        compiler = ROOT / ('tools/mwccarm/mwccarm/' + version + '/mwccarm.exe')
        directory = WORK / row['address'][2:] / row['sourceSha256'][:12] / (version.replace('/', '-') + '-O' + str(optimization) + '-' + goal)
        directory.mkdir(parents=True, exist_ok=True)
        match_runtime.WORK = directory / 'isolated-runtime'
        attempt, compiled = crossreuse_utility_c.compile_origin(origin, compiler, flags, directory)
        result = {'compiler': compiler.relative_to(ROOT).as_posix(), 'compilerSha256': sha256(compiler), 'compilerFlags': flags, 'attempt': attempt}
        if compiled:
            derived, masks, body = compiled
            covered = {offset + i for offset, unused in masks for i in range(4)}
            matching = sum(a == b for i, (a, b) in enumerate(zip(native, body)) if i not in covered)
            comparable = len([i for i in range(min(len(native), len(body))) if i not in covered])
            result.update(compiledBytes=len(body), matchingOutsideRelocations=matching, comparableBytes=comparable, derived=derived)
            if len(body) == len(native) and matching == comparable:
                with (ROOT / derived['probeObject']).open('rb') as stream:
                    elf = ELFFile(stream)
                    symbol = next(item for item in elf.get_section_by_name('.symtab').iter_symbols() if item.name == row['name'])
                    section, section_offset = symbol['st_shndx'], symbol['st_value'] & ~1
                entry = dict(row, compiler=result['compiler'], compilerSha256=result['compilerSha256'], compilerFlags=flags,
                    targetSha256=linker.digest(native), object=derived['probeObject'], objectSha256=derived['probeObjectSha256'],
                    sectionIndex=section, sectionOffset=section_offset,
                    relocations=[dict(item, format='SHT_RELA', explicitAddend=item['addend'], originalEncodedWord=body[item['offset']:item['offset'] + 4].hex()) for item in derived['relocations']])
                result['entry'] = entry
                try:
                    result['realLink'] = linker.validate(entry, directory / 'real-link')
                except Exception as error:
                    result['linkFailure'] = str(error)
        results.append(result)
    output = WORK / row['address'][2:] / row['sourceSha256'][:12] / 'report.json'
    write_json(output, {'identity': {key: row[key] for key in ('program', 'processor', 'module', 'mode', 'address', 'bytes')},
        'source': origin, 'results': results, 'sourceCredit': 0})


def invoke(index, row):
    directory = WORK / row['address'][2:] / row['sourceSha256'][:12]
    directory.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(index)], cwd=ROOT,
        capture_output=True, text=True, timeout=300)
    (directory / 'stdout.txt').write_text(result.stdout)
    (directory / 'stderr.txt').write_text(result.stderr)
    if result.returncode:
        raise ValueError(result.stderr)
    return json.loads((directory / 'report.json').read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', type=int)
    args = parser.parse_args()
    if args.worker is not None:
        worker(args.worker)
        return
    if (WORK / 'results.json').exists():
        raise ValueError('Choose a fresh exclusive sweep output')
    rows = json.loads(PROFILE.read_text())['results']
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(invoke, index, row) for index, row in enumerate(rows)]
        results = [future.result() for future in futures]
    write_json(WORK / 'results.json', {'generator': Path(__file__).name, 'generatorSha256': sha256(__file__), 'results': results, 'sourceCredit': 0})
    for row in results:
        outcomes = [item for item in row['results'] if item.get('compiledBytes')]
        if not outcomes:
            print(json.dumps({'identity': row['identity'], 'compiled': False}), flush=True)
            continue
        near = max(outcomes, key=lambda item: item['matchingOutsideRelocations'])
        print(json.dumps({'identity': row['identity'], 'attempts': len(outcomes), 'closestSize': near['compiledBytes'],
            'closestEqualBytes': near['matchingOutsideRelocations'], 'closestComparable': near['comparableBytes'],
            'exactRealLinks': sum(item.get('realLink', {}).get('exactLinkedBytes', False) for item in outcomes)}), flush=True)


if __name__ == '__main__':
    main()
