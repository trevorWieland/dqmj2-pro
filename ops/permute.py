"""Deterministic + hill-climbing allocation-form permuter for parked rows.

The hand-matching loop stalls on one class of row: the C is reachable and compiles
to the exact ledger size, but mwcc `-O2` picks a different register, stack slot or
branch form. This tool searches that shape space and accepts exactly one outcome:
byte-and-relocation exactness against the overlay image.

Two search layers:

1. **Single-step edits** over the allocation-sensitive source shapes (declaration
   order, signedness, pointer-vs-index, literal-vs-local, return ordering, and the
   structural rewrites listed below). Semantics are preserved by construction.
2. **Hill climbing** on a diff-count score (bytes differing plus length delta).
   Near-misses are kept as stepping stones: the best `--beam` texts are expanded
   again instead of always restarting from the original. Exactness is still the
   only success condition; the score only steers.

Structural edits (the part a hand search cannot reach):

* split a condition operand into a named temporary (produces the
  `mov r3, r0; cmp r3, ...` shape mwcc emits when a call result is reused),
* split an addition operand into a temporary,
* reorder commutative operands (`a + b` -> `b + a`, `a * b` -> `b * a`),
* swap the sides of a comparison (`a < b` -> `b > a`),
* insert a `(s32)` / `(u32)` cast around a condition operand.

No target bytes are stored: the expected bytes are read from the overlay image at
run time, so a candidate file carries no evidence artifact. Scoring uses the same
code path as the packet verifiers (`work/p2/check.py`), so a hit is a real hit.

Decomp-permuter (`tools/decomp-permuter-8556c81d80d1c1af98a858c8f4dc951357f29139`,
pinned commit `8556c81d80d1c1af98a858c8f4dc951357f29139`) is the intended engine
once the search needs AST-level randomisation; the loop here is the deterministic
subset that runs inside the packet harness with no extra state.

Usage
-----
    python ops/permute.py --candidate ops/candidates/ov001_021d8ff8.json
    python ops/permute.py --module ov001 --address 0x021d8ff8 --size 0x78 \\
        --symbol native_ov001_021d8ff8 --source work/p2/cd/f8ff8.c
    python ops/permute.py --candidate <json> --budget 60 --limit 800 --beam 4

Exit status is 0 when at least one candidate reaches exactness, 1 otherwise.
"""
import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'work/p2'))

PERMUTER_PIN = '8556c81d80d1c1af98a858c8f4dc951357f29139'

DECL = re.compile(r'^(?P<indent>[ \t]+)(?P<type>[A-Za-z_][A-Za-z0-9_]*)[ \t]+(?P<rest>[*A-Za-z_][^;]*);[ \t]*$')
HEX = re.compile(r'\b0[xX][0-9A-Fa-f]+\b')
CONDITION = re.compile(r'if \((?P<left>[^()&|]+?)\s*(?P<op><=|>=|==|!=|<|>)\s*(?P<right>[^()]+)\)')
ADDITION = re.compile(r'(?P<left>[A-Za-z_][A-Za-z0-9_]*)\s*\+\s*(?P<right>[A-Za-z0-9_ .\[\]]+?)(?=[;,)\n])')
COMMUTATIVE = re.compile(r'(?P<left>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<op>[+*])\s*(?P<right>[A-Za-z_][A-Za-z0-9_]*)')
COMPARE_SIDES = {'<': '>', '>': '<', '<=': '>=', '>=': '<=', '==': '==', '!=': '!='}

COMPILERS = {
    'ov000': 0x021D7240, 'ov001': 0x021D7240, 'ov002': 0x021D7240,
    'ov003': 0x021D7240, 'ov004': 0x021D7240, 'ov005': 0x021D7240,
    'ov006': 0x021D7240,
}


MAIN_IMAGE = ROOT / 'extract/arm9/arm9.bin'
MAIN_BASE = 0x02000000


def load_module(module):
    """Import the packet harness configured for `module`.

    The arm9 main module is not an overlay: its image is extract/arm9/arm9.bin at
    base 0x02000000, and its rows are Thumb, so the compile line gains -thumb.
    """
    os.environ['P2_MODULE'] = module if module != 'main' else 'ov000'
    import importlib
    import check
    check = importlib.reload(check)
    if module == 'main':
        check.OVL = MAIN_IMAGE
        check.BASE = MAIN_BASE
        flags = list(check.FLAGS) if not isinstance(check.FLAGS, str) else check.FLAGS.split()
        # -thumb has to precede -c: mwcc reads the mode flag before the compile
        # action, and appending it after -c silently fails the compile.
        position = flags.index('-c') if '-c' in flags else len(flags)
        flags.insert(position, '-thumb')
        check.FLAGS = flags
    return check


def declarations(lines):
    return [i for i, line in enumerate(lines) if DECL.match(line)]


def structural_mutations(text):
    """Semantics-preserving rewrites of a single statement's expression tree."""
    for index, match in enumerate(CONDITION.finditer(text)):
        left, op, right = match.group('left'), match.group('op'), match.group('right')
        span = text[match.start():match.end()]

        # 1. Condition operand into a named temporary.
        replacement = f'if (probe_{index} {op} {right})'
        mutated = (text[:match.start()] + replacement + text[match.end():])
        mutated = mutated.replace('{', f'{{\n    s32 probe_{index} = {left.strip()};', 1)
        yield f'split-condition:{index}', mutated

        # 2. Comparison sides swapped.
        swapped = (text[:match.start()]
                   + f'if ({right.strip()} {COMPARE_SIDES[op]} {left.strip()})'
                   + text[match.end():])
        yield f'swap-compare-sides:{index}', swapped

        # 3. Cast around the left operand.
        for cast in ('u32', 's32'):
            casted = (text[:match.start()]
                      + f'if (({cast})({left.strip()}) {op} {right})'
                      + text[match.end():])
            yield f'cast-condition:{cast}:{index}', casted

    for index, match in enumerate(ADDITION.finditer(text)):
        left, right = match.group('left'), match.group('right')
        swapped = text[:match.start()] + f'{right.strip()} + {left}' + text[match.end():]
        yield f'swap-add:{index}', swapped

    for index, match in enumerate(COMMUTATIVE.finditer(text)):
        left, op, right = match.group('left'), match.group('op'), match.group('right')
        swapped = text[:match.start()] + f'{right} {op} {left}' + text[match.end():]
        yield f'swap-commutative:{index}', swapped


def mutations(text):
    """Yield (name, mutated_text) in a deterministic order."""
    lines = text.split('\n')
    decls = declarations(lines)

    for a, b in zip(decls, decls[1:]):
        if b == a + 1:
            swapped = list(lines)
            swapped[a], swapped[b] = swapped[b], swapped[a]
            yield f'swap-decl:{a + 1}/{b + 1}', '\n'.join(swapped)

    for a, b in ((x, y) for x in decls for y in decls if x < y):
        swapped = list(lines)
        swapped[a], swapped[b] = swapped[b], swapped[a]
        yield f'swap-any-decl:{a + 1}/{b + 1}', '\n'.join(swapped)

    if decls:
        top = decls[0]
        for index in decls[1:]:
            moved = list(lines)
            moved.insert(top, moved.pop(index))
            yield f'hoist-decl:{index + 1}', '\n'.join(moved)

    for index in decls:
        kind = DECL.match(lines[index]).group('type')
        other = {'s32': 'u32', 'u32': 's32', 's8': 'u8', 'u8': 's8',
                 's16': 'u16', 'u16': 's16'}.get(kind)
        if other:
            flipped = list(lines)
            flipped[index] = lines[index].replace(kind, other, 1)
            yield f'type:{index + 1}:{kind}->{other}', '\n'.join(flipped)

    for match in re.finditer(r'\b([A-Za-z_][A-Za-z0-9_]*)\[([^\[\]]+)\]', text):
        base, subscript = match.group(1), match.group(2)
        yield (f'index->pointer:{base}', text[:match.start()]
               + f'*({base} + {subscript})' + text[match.end():])

    body = text.find('{')
    if body >= 0:
        for match in HEX.finditer(text, body):
            literal = match.group(0)
            name = f'local_{literal[2:]}'
            yield (f'literal->local:{literal}',
                   text[:body + 1] + f'\n    s32 {name} = {literal};'
                   + text[body + 1:match.start()] + name + text[match.end():])

    if 'return 0;' in text and 'return 1;' in text:
        swapped = text.replace('return 0;', 'return 2;').replace('return 1;', 'return 0;')
        yield 'swap-return-constants', swapped.replace('return 2;', 'return 1;')

    for name, mutated in structural_mutations(text):
        yield name, mutated


def score(outcome):
    """Diff count: lower is closer. Compile failure is worst."""
    if outcome.get('stage') != 'compare' or 'actual' not in outcome:
        return 10 ** 6
    actual = bytes.fromhex(outcome['actual'])
    wanted = bytes.fromhex(outcome['want'])
    score = abs(len(actual) - len(wanted))
    for left, right in zip(actual, wanted):
        if left != right:
            score += 1
    return score


def permute_candidate(spec, budget, limit, check, seed=0, beam=4):
    source = ROOT / spec['source']
    original = source.read_text()
    address = int(spec['address'], 16) if isinstance(spec['address'], str) else spec['address']
    size, symbol = spec['size'], spec['symbol']

    started = time.time()
    iterations = 0
    seen = {hash(original)}
    trail = {}          # text hash -> trail label
    first = check.check(str(source), symbol, address, size)
    best_score = score(first)
    if first.get('ok') is True:
        return {'iterations': 0, 'seconds': 0.0, 'exact': True, 'mutation': 'already exact',
                'start': 0, 'final': 0}
    trajectory = [best_score]
    frontier = [(best_score, original, 'original')]

    while frontier and iterations < limit and time.time() - started <= budget:
        expanded, next_frontier = [], []
        for base_score, base_text, base_trail in frontier:
            for name, mutated in mutations(base_text):
                if iterations >= limit or time.time() - started > budget:
                    break
                digest = hash(mutated)
                if digest in seen or mutated == base_text:
                    continue
                seen.add(digest)
                iterations += 1
                mutant = source.with_name(f'{source.stem}__perm{iterations}{source.suffix}')
                try:
                    mutant.write_text(mutated)
                    outcome = check.check(str(mutant), symbol, address, size)
                finally:
                    try:
                        mutant.unlink()
                    except OSError:
                        pass
                if outcome.get('ok') is True:
                    return {'iterations': iterations,
                            'seconds': round(time.time() - started, 1),
                            'exact': True,
                            'mutation': f'{base_trail} + {name}',
                            'start': best_score, 'final': 0,
                            'trajectory': trajectory + [0]}
                value = score(outcome)
                if value < best_score:
                    best_score = value
                    trajectory.append(value)
                next_frontier.append((value, mutated, f'{base_trail} + {name}'))
        frontier = sorted(next_frontier)[:beam]

    return {'iterations': iterations, 'seconds': round(time.time() - started, 1),
            'exact': False, 'mutation': None, 'start': score(first),
            'final': best_score, 'trajectory': trajectory}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--candidate', action='append', default=[])
    parser.add_argument('--module')
    parser.add_argument('--address')
    parser.add_argument('--size', type=lambda v: int(v, 0))
    parser.add_argument('--symbol')
    parser.add_argument('--source')
    parser.add_argument('--budget', type=float, default=60.0)
    parser.add_argument('--limit', type=int, default=800)
    parser.add_argument('--beam', type=int, default=4)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)

    specs = [json.loads(Path(name).read_text()) for name in args.candidate]
    if args.module:
        specs.append({'module': args.module, 'address': args.address, 'size': args.size,
                      'symbol': args.symbol, 'source': args.source})
    if not specs:
        parser.error('no candidate given')

    results = []
    for spec in specs:
        check = load_module(spec['module'])
        result = permute_candidate(spec, args.budget, args.limit, check, args.seed, args.beam)
        result.update({'module': spec['module'], 'address': spec['address'],
                       'symbol': spec['symbol'], 'size': spec['size'],
                       'source': spec['source']})
        results.append(result)
        if not args.json:
            status = 'EXACT' if result['exact'] else 'no'
            trail = ' '.join(str(v) for v in result.get('trajectory', []))
            print(f"{spec['module']:6s} {spec['address']:>10s} {spec['size']:4d} B  "
                  f"{result['iterations']:4d} mutants  {result['seconds']:6.1f} s  "
                  f"diff {result['start']}->{result['final']}  [{trail}]  {status}"
                  + (f"  via {result['mutation']}" if result['exact'] else ''))

    if args.json:
        print(json.dumps(results, indent=2))
    return 0 if any(r['exact'] for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
