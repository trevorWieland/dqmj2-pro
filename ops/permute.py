"""Deterministic allocation-form permuter for parked decompilation rows.

The hand-matching loop in this project stalls on one class of row: the C is
reachable and the function compiles to the exact ledger size, but mwcc `-O2`
chooses a different register, a different stack slot or a different branch form.
Those choices are driven by a small set of source-level shapes that we already
know matter (the "levers" recorded in the packet comments). This tool searches
that shape space deterministically and accepts only one outcome: byte-and-
relocation exactness against the overlay image.

The search is a fixed, ordered list of single-step text mutations applied to a
parked source file. Every mutant is compiled with the pinned compiler and compared
with the same code path the packet verifiers use, so a hit is a real hit. Nothing
about the target is stored: the expected bytes are read from the overlay image at
run time, so a candidate file carries no evidence artifact.

Decomp-permuter (`tools/decomp-permuter-8556c81d80d1c1af98a858c8f4dc951357f29139`,
pinned commit `8556c81d80d1c1af98a858c8f4dc951357f29139`) is the intended engine
once the search space needs randomisation and AST-level mutations. The loop here
is the deterministic subset that needs no external state and can run inside the
packet harness unchanged; its mutation list is the same allocation-sensitive set.

Usage
-----
    python ops/permute.py --candidate ops/candidates/ov001_021d8ff8.json
    python ops/permute.py --module ov001 --address 0x021d8ff8 --size 0x78 \\
        --symbol native_ov001_021d8ff8 --source work/p2/cd/f8ff8.c
    python ops/permute.py --candidate <json> --budget 120 --limit 400

Exit status is 0 when at least one candidate reaches exactness, 1 otherwise.

Candidate file (JSON)
---------------------
    {
      "module": "ov001",
      "address": "0x021d8ff8",
      "size": 120,
      "symbol": "native_ov001_021d8ff8",
      "source": "work/p2/cd/f8ff8.c"
    }

`compiler` and `flags` are optional; they default to the pinned packet compiler
and flags. The module selects the overlay image and base address, exactly as
`P2_MODULE` does for the packet verifiers.
"""
import argparse
import itertools
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'work/p2'))

PERMUTER_PIN = '8556c81d80d1c1af98a858c8f4dc951357f29139'

DECL = re.compile(r'^(?P<indent>[ \t]+)(?P<type>[A-Za-z_][A-Za-z0-9_]*)[ \t]+(?P<rest>[*A-Za-z_][^;]*);[ \t]*$')
HEX = re.compile(r'\b0[xX][0-9A-Fa-f]+\b')


def load_module(module):
    """Import the packet harness configured for `module`."""
    os.environ['P2_MODULE'] = module
    import importlib
    import check
    importlib.reload(check)
    return check


def split_lines(text):
    return text.split('\n')


def declarations(lines):
    """Indices of simple local declaration lines."""
    return [i for i, line in enumerate(lines) if DECL.match(line)]


def mutations(text):
    """Yield (name, mutated_text) in a deterministic order."""
    lines = split_lines(text)
    decls = declarations(lines)

    # 1. Adjacent declaration swaps: the cheapest known lever for register order.
    for a, b in zip(decls, decls[1:]):
        if b != a + 1:
            continue
        swapped = list(lines)
        swapped[a], swapped[b] = swapped[b], swapped[a]
        yield f'swap-decl:{a + 1}/{b + 1}', '\n'.join(swapped)

    # 2. Declaration moved to the top of the local block.
    if decls:
        top = decls[0]
        for index in decls[1:]:
            moved = list(lines)
            line = moved.pop(index)
            moved.insert(top, line)
            yield f'hoist-decl:{index + 1}->{top + 1}', '\n'.join(moved)

    # 3. Signedness flip on a declaration.
    for index in decls:
        match = DECL.match(lines[index])
        kind = match.group('type')
        other = {'s32': 'u32', 'u32': 's32', 's8': 'u8', 'u8': 's8',
                 's16': 'u16', 'u16': 's16'}.get(kind)
        if other is None:
            continue
        flipped = list(lines)
        flipped[index] = lines[index].replace(kind, other, 1)
        yield f'type:{index + 1}:{kind}->{other}', '\n'.join(flipped)

    # 4. Pointer form vs index form for a single subscript use.
    for match in re.finditer(r'\b([A-Za-z_][A-Za-z0-9_]*)\[([^\[\]]+)\]', text):
        base, subscript = match.group(1), match.group(2)
        replacement = f'*({base} + {subscript})'
        mutated = text[:match.start()] + replacement + text[match.end():]
        yield f'index->pointer:{base}[{subscript}]', mutated

    # 5. Hex literal held in a local instead of inline (the reciprocal-multiply
    #    lesson: a literal can be folded while a local cannot).
    body_start = text.find('{')
    if body_start >= 0:
        for match in HEX.finditer(text, body_start):
            literal = match.group(0)
            mutated = (text[:body_start + 1] + f'\n    s32 local_{literal[2:]} = {literal};'
                       + text[body_start + 1:match.start()]
                       + f'local_{literal[2:]}' + text[match.end():])
            yield f'literal->local:{literal}', mutated

    # 6. Result-variable form vs early return for a two-branch tail.
    if 'return 0;' in text and 'return 1;' in text:
        swapped = text.replace('return 0;', 'return 2;').replace('return 1;', 'return 0;')
        swapped = swapped.replace('return 2;', 'return 1;')
        yield 'swap-return-constants', swapped

    # 7. All declaration pairs, not just adjacent ones: the allocator's order is
    #    not always the textual order, so the wider permutation matters.
    for a, b in itertools.combinations(decls, 2):
        swapped = list(lines)
        swapped[a], swapped[b] = swapped[b], swapped[a]
        yield f'swap-any-decl:{a + 1}/{b + 1}', '\n'.join(swapped)

    # 8. A call result compared inline becomes a named local, and the reverse.
    #    This is the lever for the `mov r3, r0; cmp r3, ...` tail shape.
    call_compare = re.compile(
        r'if \((?P<call>[A-Za-z_][A-Za-z0-9_]*\([^()]*\))\s*(?P<op><=|>=|==|!=|<|>)\s*'
        r'(?P<const>[^)]+)\)')
    for index, match in enumerate(call_compare.finditer(text)):
        name = f'permuted_{index}'
        replacement = (f'size_probe_ = {match.group("call")};\n    '
                       f'if (size_probe_ {match.group("op")} {match.group("const")})')
        mutated = (text[:match.start()] + replacement + text[match.end():])
        mutated = mutated.replace('{', '{\n    u32 size_probe_;', 1)
        yield f'split-call-result:{match.group("call")}', mutated


def permute_candidate(spec, budget, limit, check, seed=0):
    source = ROOT / spec['source']
    text = source.read_text()
    address = int(spec['address'], 16) if isinstance(spec['address'], str) else spec['address']
    size = spec['size']
    symbol = spec['symbol']

    started = time.time()
    iterations = 0
    seen = {hash(text)}
    singles = list(mutations(text))

    # Deterministic composition pass: combinations of single-step shapes are the
    # part of the space a hand search cannot reach, and a fixed seed keeps a run
    # reproducible while making it wider than the single-step list.
    random_source = __import__('random').Random(seed)
    composed = []
    for _ in range(limit):
        first, second = random_source.randrange(len(singles)), random_source.randrange(len(singles))
        composed.append((f"{singles[first][0]}+{singles[second][0]}", first, second))

    def candidates():
        for name, mutated in singles:
            yield name, mutated
        for name, first, second in composed:
            mid = singles[first][1]
            base_text = text
            # Re-derive the second mutation against the intermediate text so the
            # composition never depends on stale offsets.
            for step_name, step in mutations(mid):
                if step_name == singles[second][0] and step != mid:
                    yield name, step
                    break

    for name, mutated in candidates():
        if iterations >= limit or time.time() - started > budget:
            break
        digest = hash(mutated)
        if digest in seen or mutated == text:
            continue
        seen.add(digest)
        iterations += 1
        mutant = source.with_name(f'{source.stem}__perm{iterations}{source.suffix}')
        try:
            mutant.write_text(mutated)
            outcome = check.check(str(mutant), symbol, address, size)
            if outcome.get('ok') is True:
                return {'iterations': iterations, 'seconds': round(time.time() - started, 1),
                        'exact': True, 'mutation': name, 'winner': mutant.read_text(),
                        'relocs': len(outcome.get('relocations') or [])}
        finally:
            try:
                mutant.unlink()
            except OSError:
                pass
    return {'iterations': iterations, 'seconds': round(time.time() - started, 1),
            'exact': False, 'mutation': None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--candidate', action='append', default=[],
                        help='candidate JSON file (repeatable)')
    parser.add_argument('--module')
    parser.add_argument('--address')
    parser.add_argument('--size', type=lambda v: int(v, 0))
    parser.add_argument('--symbol')
    parser.add_argument('--source')
    parser.add_argument('--budget', type=float, default=60.0,
                        help='seconds per candidate (default 60)')
    parser.add_argument('--limit', type=int, default=600,
                        help='max mutants per candidate (default 600)')
    parser.add_argument('--json', action='store_true', help='emit machine-readable results')
    parser.add_argument('--seed', type=int, default=0, help='composition seed (default 0)')
    args = parser.parse_args(argv)

    specs = []
    for name in args.candidate:
        specs.append(json.loads(Path(name).read_text()))
    if args.module:
        specs.append({'module': args.module, 'address': args.address, 'size': args.size,
                      'symbol': args.symbol, 'source': args.source})
    if not specs:
        parser.error('no candidate given')

    results = []
    for spec in specs:
        check = load_module(spec['module'])
        result = permute_candidate(spec, args.budget, args.limit, check, args.seed)
        result.update({'module': spec['module'], 'address': spec['address'],
                       'symbol': spec['symbol'], 'size': spec['size'],
                       'source': spec['source']})
        results.append(result)
        if not args.json:
            status = 'EXACT' if result['exact'] else 'no'
            print(f"{spec['module']:6s} {spec['address']:>10s} {spec['size']:4d} B  "
                  f"{result['iterations']:4d} mutants  {result['seconds']:6.1f} s  {status}"
                  + (f"  via {result['mutation']}" if result['exact'] else ''))

    if args.json:
        print(json.dumps(results, indent=2))
    return 0 if any(r['exact'] for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
