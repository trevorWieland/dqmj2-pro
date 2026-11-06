import argparse
import json
from pathlib import Path
import match_arm7
import draft_arm7
from refine_utility import variants, stack_buffer_variant

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', required=True)
    parser.add_argument('--limit', type=int, default=180)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    path = ROOT / f'evidence/matches/arm7-{args.batch}.json'
    if args.verify:
        report = json.loads(path.read_text())
        matches = []
        for entry in report['matches']:
            source = ROOT / entry['source']
            if match_arm7.sha(source.read_bytes()) != entry['sourceSha256']:
                raise ValueError('Frozen ARM7 refined C changed')
            matches.append(draft_arm7.validate(entry, match_arm7.accepted_spec(entry), source))
        report.update(matches=matches)
        path.write_text(json.dumps(report, indent=2) + '\n')
        print({'verified': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})
        return
    if path.exists():
        raise ValueError('Choose a new ARM7 source refinement batch')
    accepted = {(entry['module'], int(entry['address'], 0)) for report in (ROOT / 'evidence/matches').glob('arm7-*.json') for entry in json.loads(report.read_text()).get('matches', [])}
    specs = {(spec['module'], spec['address']): spec for spec in match_arm7.candidates(10000)}
    pins = {tool.relative_to(ROOT).as_posix(): digest for tool, digest in match_arm7.tools()}
    rows = json.loads((ROOT / 'work/lowlevel-recovery/arm7-near-matches.json').read_text())
    rows = [row for row in rows if (row['module'], int(row['address'], 0)) not in accepted][args.offset:args.offset + args.limit]
    work = ROOT / 'work/lowlevel-recovery/arm7-refinements' / args.batch
    work.mkdir(parents=True, exist_ok=True)
    matches, attempts = [], []
    for row in rows:
        spec = specs[row['module'], int(row['address'], 0)]
        origin = ROOT / row['source']
        old = row['attempt']
        if match_arm7.sha(origin.read_bytes()) != old['sourceSha256']:
            raise ValueError('Content-addressed draft C changed during refinement')
        compiler = ROOT / old['compiler']
        digest = pins[old['compiler']]
        if match_arm7.sha(compiler.read_bytes()) != digest:
            raise ValueError('ARM7 refinement compiler changed')
        flags = old['compilerFlags']
        result = {'module': spec['module'], 'address': hex(spec['address']), 'attempts': []}
        for hypothesis, text in [*variants(origin.read_text()), *stack_buffer_variant(origin.read_text(), spec)]:
            if len(text.splitlines()) > 500:
                continue
            name = 'native_' + spec['module'].replace('-', '_') + f"_{spec['address']:08x}"
            source = work / (name + '-' + match_arm7.sha(text.encode())[:16] + '.c')
            source.write_text(text)
            entry, compiled = match_arm7.compare(source, spec, compiler, digest, int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
            entry['sourceHypothesis'] = hypothesis
            result['attempts'].append(entry)
            if compiled is None:
                continue
            frozen = ROOT / f'src/arm7/{args.batch}' / (name + '.c')
            frozen.parent.mkdir(parents=True, exist_ok=True)
            if frozen.exists():
                raise ValueError('Refusing to overwrite accepted ARM7 source')
            frozen.write_bytes(source.read_bytes())
            entry.update(source=frozen.relative_to(ROOT).as_posix(), sourceSha256=match_arm7.sha(frozen.read_bytes()))
            matches.append(draft_arm7.validate(entry, spec, frozen))
            result['accepted'] = True
            break
        attempts.append(result)
        (work / (name + '.json') if result['attempts'] else work / f"empty-{spec['address']:08x}.json").write_text(json.dumps(result, indent=2) + '\n')
        print({'module': spec['module'], 'address': hex(spec['address']), 'matched': result.get('accepted', False), 'attempts': len(result['attempts'])}, flush=True)
    report = {'schemaVersion': 1, 'romSha256': match_arm7.sha((ROOT / 'inputs/game.nds').read_bytes()), 'processor': 'arm7', 'runtimeMappingCanonical': True,
              'matches': matches, 'nativeSymbols': {rel['symbol']: rel['target'] for entry in matches for rel in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'limitations': ['Only full native spans with declared ELF relocation agreement are accepted; all edits are ordinary C type/layout hypotheses', 'Unsupported native effects and provisional semantic names remain explicit']}
    (ROOT / f'evidence/attempts/arm7-{args.batch}.json').write_text(json.dumps(attempts, indent=2) + '\n')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches)})


if __name__ == '__main__':
    main()
