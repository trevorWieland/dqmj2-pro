import argparse
import ast
import concurrent.futures
import re
import shutil
import subprocess
import sys
from types import SimpleNamespace
from project import ROOT, read_json, write_json, sha256
from source_word_inputs_20261031 import apply_context
import draft_runtime as draft

BASE = ROOT / 'work/main-word-contexts270-20261031'
CATALOGUE = 'evidence/verification/source-word-inputs83-20261031.json'


def configure(mode):
    tree = ast.parse((ROOT / 'draft_runtime.py').read_text(encoding='utf-8-sig'))
    names = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute) and
        isinstance(node.value, ast.Name) and node.value.id == 'OPTIONS'}
    options = {name: False for name in names}
    options.update(module='main', word_args=True, stack_buffers=True, source_returns=False)
    draft.OPTIONS = SimpleNamespace(**options)
    draft.WORK = BASE / mode
    draft.matcher.WORK = BASE / mode / 'compile'
    draft.inputs()


def one(function, mode):
    configure(mode)
    assembly, context = draft.FUNCTION_INPUTS[function]
    edits = []
    if mode == 'seeded':
        context, edits = apply_context(context, read_json(ROOT / CATALOGUE))
    draft.FUNCTION_INPUTS[function] = assembly, context
    result = draft.one(function)
    result.update(mode=mode, edits=edits, sourceCredit=0, registered=False)
    if result.get('draftSource'):
        original = ROOT / result['draftSource']
        target = ROOT / f'nonmatching/main-runtime/20261031-word-inputs270/{mode}/{function}.c'
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
        result['retainedSource'] = dict(path=target.relative_to(ROOT).as_posix(), sha256=sha256(target))
    write_json(BASE / 'results' / f'{mode}-{function}.json', result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--one')
    parser.add_argument('--mode', choices=['weak', 'seeded'])
    args = parser.parse_args()
    if args.one:
        one(args.one, args.mode)
        return
    configure('selection')
    catalogue = read_json(ROOT / CATALOGUE)
    accepted = read_json(ROOT / 'evidence/verification/accepted-cohort83-identities-20261031.json')
    addresses = {row['address'] for row in accepted['functions'] if row['processor'] == 'arm9' and
        row['module'] == 'main' and row['mode'] == 'arm'}
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text()
    candidates = []
    for name, size, address in re.findall(r'^(\S+) kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', symbols, re.M):
        size, address = int(size, 0), int(address, 0)
        if address in addresses or not (address < 0x02040000 or address >= 0x020D0000):
            continue
        if not 512 <= size <= 1024 or name not in draft.FUNCTION_INPUTS:
            continue
        _, edits = apply_context(draft.FUNCTION_INPUTS[name][1], catalogue)
        if edits:
            candidates.append(dict(name=name, bytes=size, address=hex(address), proposedInputEdits=edits))
    candidates = sorted(candidates, key=lambda row: (-len(row['proposedInputEdits']), row['address']))[:12]
    plan = dict(candidates=candidates, catalogue=CATALOGUE, catalogueSha256=sha256(ROOT / CATALOGUE),
        acceptedSnapshotSha256=sha256(ROOT / 'evidence/verification/accepted-cohort83-identities-20261031.json'),
        modes=['weak', 'seeded'], workers=3, sourceCredit=0, ordinaryCandidateBytes=sum(row['bytes'] for row in candidates))
    write_json(ROOT / 'evidence/verification/main-word-contexts270-plan-20261031.json', plan)

    def run(item):
        mode, row = item
        log = BASE / 'logs' / f'{mode}-{row["name"]}.txt'
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('w', encoding='utf-8') as stream:
            process = subprocess.run([sys.executable, str(ROOT / 'trial_main_word_contexts270_20261031.py'),
                '--one', row['name'], '--mode', mode], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
        return dict(mode=mode, name=row['name'], exitCode=process.returncode, log=log.relative_to(ROOT).as_posix())

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        jobs = list(pool.map(run, [(mode, row) for mode in ['weak', 'seeded'] for row in candidates]))
    results = []
    for job in jobs:
        path = BASE / 'results' / f'{job["mode"]}-{job["name"]}.json'
        results.append(dict(**job, result=read_json(path) if path.is_file() else None))
    report = dict(plan=plan, results=results, sourceCredit=0, registered=False,
        limitations=['Bounded drafting comparison only; no complete source, native behavior or exact module acceptance',
            'Existing explicit contracts and accepted source are unchanged; current word views remain hypotheses'])
    write_json(ROOT / 'evidence/attempts/main-word-contexts270-20261031.json', report)
    print(dict(candidates=len(candidates), nativeCandidateBytes=plan['ordinaryCandidateBytes'],
        attempts=len(results), drafted=sum(bool(row['result'] and row['result'].get('draftSource')) for row in results),
        preliminaryExact=sum(bool(row['result'] and row['result'].get('match')) for row in results), sourceCredit=0))


if __name__ == '__main__':
    main()
