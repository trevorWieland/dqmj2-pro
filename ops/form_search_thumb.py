"""Form search for main-module Thumb rows, with three idiom dimensions.

This is the batch-2 extension of :mod:`ops.form_search`.  The batch-1 tool
enumerates a literal grid of ``$NAME`` replacements over one C template.  The
197 remaining main-module Thumb rows are all 2-25 bytes away because three
*layout* idioms are outside that grid:

``WRITEBACK``
    The image writes a run of words as post-increment ``stm`` groups
    (``stm r0!, {r1, r2}``) while mwcc writes N separate ``str``.  The
    alternatives here are the source disciplines that make mwcc choose a
    writeback form: array indices, a pointer walk, a pointer walk whose
    advanced value stays live, a struct assignment from a local, and a
    fill loop.  Empirically mwcc only emits ``stm`` for a store whose
    destination pointer remains live after the store
    (``p[0] = v; p++; return p;`` -> ``stm r0!, {r1}``), or for a
    multi-word struct assignment (``*p = v`` -> ``ldm``/``stm``).

``HOIST``
    The image loads a literal-pool word *after* some argument shuffling that
    mwcc schedules before it.  The mechanism found in this batch is argument
    liveness: a third argument that is still live in r2 forces the pool word
    into r3 and delays its load, while a dead argument lets mwcc hoist the
    load and reuse r2.  The alternatives are source orderings of the store and
    call plus the call-arity hypotheses the row spec supplies.

``LOOP``
    The image uses a countdown ``do``/``while`` (or a pre-tested loop) where
    mwcc emits the other rotation.  The alternatives are ``for``, ``while``,
    ``do``/``while`` and ``goto`` spellings of the same loop.

The row spec names the row's address/size/module, points at a template file
and lists the alternatives for each dimension::

    {
      "address": "0x020b5890", "bytes": 12, "module": "main",
      "template": "020b5890.c",
      "dimensions": {
        "HOIST": ["native_fn_020b4108(a, p);",
                  "native_fn_020b4108(a, p, c);"]
      }
    }

A dimension may instead call one of the libraries with ``params``::

    {"library": "writeback", "params": {"values": ["a", "b"], "live_tail": "return p;"}}

The template uses :class:`string.Template` syntax, so C braces need no escaping.
Missing dimensions collapse to one empty alternative, which is the control:
the expanded source is byte-identical to the template with nothing substituted.

Usage::

    python ops/form_search_thumb.py --spec ops/form_specs/thumb/020b5890.json \
        --time-budget 300 --keep src/main/t1_main_thumb/native_main_020b5890.c
    python ops/form_search_thumb.py --rank --json build/thumb-form2/ranked.json
    python ops/form_search_thumb.py --spec ... --print-best
"""
import argparse
import fnmatch
import itertools
import json
import os
import re
import string
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402

DIMENSIONS = ('WRITEBACK', 'HOIST', 'LOOP')
LANE_GLOB = 'src/main/t1_main_thumb/**'


# ---------------------------------------------------------------------------
# Form libraries.  Each returns a list of (name, body) pairs; the body is
# substituted into the row template's $NAME placeholder.  ``decl`` names a
# companion placeholder (``$NAME_DECL``) for forms that need a type or macro.


def _declare_struct(count, type_name='u32', name='WB'):
    fields = ' '.join(f'{type_name} f{index};' for index in range(count))
    return f'typedef struct {{ {fields} }} {name};'


def writeback_forms(values, base='p', type_name='u32', live_tail=None,
                    loop_var='i'):
    """Return same-store alternatives that stress mwcc's writeback choice.

    ``values`` is the list of C expressions stored at consecutive words of
    ``base``.  Every form stores exactly those values in that order.  The
    interesting pair is ``array`` (indexed stores) versus ``ptr_walk_live``:
    the latter keeps the advanced pointer live, which is what makes mwcc fuse
    the store and the address increment into ``stm base!, {reg}``.
    """
    forms = [
        ('array', '\n'.join(f'{base}[{index}] = {value};'
                            for index, value in enumerate(values))),
        ('ptr_walk', '\n'.join(f'*{base}++ = {value};' for value in values)),
    ]
    if live_tail is not None:
        body = [f'{type_name} *q = {base};']
        body.extend(f'*q++ = {value};' for value in values)
        body.append(f'{base} = q;')
        body.append(live_tail)
        forms.append(('ptr_walk_live', '\n'.join(body)))
    fields = '\n'.join(f'    block.f{index} = {value};'
                       for index, value in enumerate(values))
    forms.append(('struct_fields',
                  _declare_struct(len(values), type_name) + '\n'
                  f'WB block;\n{fields}\n'
                  f'*(WB *){base} = block;'))
    return forms


def hoist_forms(store, call, named=None, volatile=False):
    """Return source orderings around one store and one call.

    ``store`` is one C statement writing the field/value that the image places
    before the pool load; ``call`` is the call statement.  ``named`` is an
    optional ``(declarations, statements)`` pair binding call arguments to
    named locals first.  The alternatives deliberately change *statement
    order only*; all of them compute the same store and call.
    """
    forms = [
        ('direct', store + '\n' + call),
        ('comma', store.rstrip(';') + ', ' + call),
    ]
    if named:
        declarations, statements = named
        forms.append(('named_temps',
                      declarations + '\n' + store + '\n' + statements + '\n' + call))
    if volatile:
        forms.append(('volatile_store',
                      store.replace('= ', '= (volatile u32)', 1) + '\n' + call))
    return forms


def loop_forms(body, count, init='n', direction='down', index='i'):
    """Return four spellings of the same constant-trip countdown loop.

    ``body`` is a C statement block that uses ``index`` as the loop variable.
    ``count`` is an expression for the trip count (usually ``init`` itself).
    The ``do`` form tests after the body; the ``for``/``while`` forms pre-test;
    the ``goto`` form spells the same pre-tested control flow out.  The ``do``
    form assumes the caller guarantees a non-zero count, which is exactly the
    contract the image rows encode when they contain no pre-test.
    """
    return [
        ('for', f'for ({index} = {init}; {index} != 0; {index}--) {{\n{body}\n}}'),
        ('while', f'{index} = {init};\nwhile ({index} != 0) {{\n{body}\n{index}--;\n}}'),
        ('do', f'{index} = {init};\ndo {{\n{body}\n}} while (--{index});'),
        ('goto', f'{index} = {init};\nif ({index} == 0) goto loop_end;\n'
                 f'loop_body:\n{body}\n{index}--;\n'
                 f'if ({index} != 0) goto loop_body;\nloop_end: ;'),
    ]


LIBRARIES = {
    'writeback': writeback_forms,
    'hoist': hoist_forms,
    'loop': loop_forms,
}


# ---------------------------------------------------------------------------
# Spec loading and expansion.


class SpecError(ValueError):
    """A row spec is malformed or names an unknown library/dimension."""


def load_spec(path):
    path = Path(path)
    document = json.loads(path.read_text(encoding='utf-8'))
    if 'address' not in document or 'bytes' not in document:
        raise SpecError(f'{path}: address and bytes are required')
    if 'template' not in document:
        raise SpecError(f'{path}: template is required')
    template = path.parent / document['template']
    if not template.is_file():
        raise SpecError(f'{path}: template {template} is missing')
    document['_path'] = str(path)
    document['_template'] = str(template)
    return document


def dimension_alternatives(spec, dimension):
    """Return ``[(name, text)]`` for one dimension of a spec.

    A dimension is absent/``null`` (one empty alternative: the control), a
    list of literal snippets, or a ``{"library": ..., "params": ...}`` call.
    """
    if dimension not in DIMENSIONS:
        raise SpecError(f'unknown dimension {dimension}')
    entry = spec.get('dimensions', {}).get(dimension)
    if entry is None:
        return [('none', '')]
    if isinstance(entry, list):
        if not entry:
            raise SpecError(f'{dimension}: empty alternative list')
        return [(f'literal{index}', str(value)) for index, value in enumerate(entry)]
    if not isinstance(entry, dict):
        raise SpecError(f'{dimension}: expected a list or a library object')
    library = entry.get('library')
    if library not in LIBRARIES:
        raise SpecError(f'{dimension}: unknown library {library!r}')
    params = entry.get('params', {})
    if not isinstance(params, dict):
        raise SpecError(f'{dimension}: params must be an object')
    forms = LIBRARIES[library](**params)
    names = [name for name, _body in forms]
    if len(names) != len(set(names)):
        raise SpecError(f'{dimension}: duplicate form names {names}')
    return forms


def expand(spec):
    """Return ``[(choices, source)]`` for the full product of the dimensions."""
    template = string.Template(Path(spec['_template']).read_text(encoding='utf-8'))
    lanes = []
    for dimension in DIMENSIONS:
        lanes.append([(dimension, name, text)
                      for name, text in dimension_alternatives(spec, dimension)])
    expanded = []
    for combination in itertools.product(*lanes):
        values = {dimension: text for dimension, _name, text in combination}
        # A dimension is also available as $NAME_DECL for companion
        # declarations; literal/library bodies that need a declaration put it
        # at the top of their own body instead, so this stays empty.
        for dimension in DIMENSIONS:
            values.setdefault(dimension + '_DECL', '')
        source = template.substitute(values)
        choices = {dimension: name for dimension, name, _text in combination
                   if name != 'none'}
        expanded.append((choices, source))
    return expanded


# ---------------------------------------------------------------------------
# Compile/score path.  The lane rule (module main, mode thumb, p032,
# mwccarm 2.0/base) is resolved from config/source_units.json, never copied.


def lane_rule(root):
    import source_units
    config = source_units.load_config(Path(root))
    rule = source_units.resolve(config, LANE_GLOB.replace('/**', '/row.c'))
    if rule.get('module') != 'main' or rule.get('mode') != 'thumb':
        raise SystemExit(f'lane rule resolved to {rule.get("module")}/{rule.get("mode")}')
    flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
    return Path(root) / rule['compilerPath'], flags


def score_row(root, spec, source, work, modes, image, base, tag='candidate'):
    compiler, flags = lane_rule(root)
    source_path = Path(work) / f'{tag}.c'
    object_path = Path(work) / f'{tag}.o'
    source_path.write_text(source, encoding='utf-8')
    compiled = form_search.compile_source(compiler, source_path, object_path, Path(root),
                                          flags=flags)
    if compiled.returncode != 0:
        return None, (compiled.stdout or compiled.stderr or '').strip()[:200]
    text, defined, relocations = form_search.read_object(object_path)
    address = int(spec['address'], 0)
    try:
        actual = form_search.relocate(text, address, relocations, defined, modes=modes)
    except form_search.UnsupportedRelocation:
        raise
    except ValueError:
        return None, 'unencodable relocation'
    size = spec['bytes']
    want = image[address - base:address - base + size]
    return form_search.score(actual, want), actual


def search(root, spec, limit=400, time_budget=300.0, keep=None, verbose=True):
    root = Path(root).resolve()
    address = int(spec['address'], 0)
    module = spec.get('module', 'main')
    image, _, base = form_search.module_image(root, module)
    modes = form_search.TargetModes(root, module)
    work = root / 'build/form_search_thumb' / f'{address:08x}'
    work.mkdir(parents=True, exist_ok=True)
    # The lane's shared context header must be resolvable from the generated
    # candidate's directory; the verified sources include it by this name.
    context = root / 'src/main/t1_main_thumb/context.h'
    if context.is_file():
        (work / 'context.h').write_bytes(context.read_bytes())
    candidates = expand(spec)
    started = time.monotonic()
    best = None
    ranked = []
    tried = 0
    skipped = 0
    for choices, source in candidates[:limit]:
        if time.monotonic() - started > time_budget:
            if verbose:
                print(f'  time budget {time_budget:.0f}s reached after {tried} candidates')
            break
        try:
            current, actual = score_row(root, spec, source, work, modes, image, base,
                                        tag=f'cand{tried:04d}')
        except form_search.UnsupportedRelocation:
            skipped += 1
            continue
        tried += 1
        if current is None:
            continue
        ranked.append((current, choices, len(actual), source))
        ranked.sort(key=lambda item: item[0])
        del ranked[20:]
        if best is None or current < best[0]:
            best = (current, choices, len(actual), source)
            if verbose:
                print(f'  #{tried:3d} best {current} '
                      + ', '.join(f'{key}={value}' for key, value in choices.items())[:140])
    if best is None:
        return {'address': address, 'score': None, 'tried': tried, 'skipped': skipped}
    (differing, length), choices, size, source = best
    if keep:
        Path(keep).write_text(source, encoding='utf-8')
    result = {
        'address': address,
        'score': (differing, length),
        'exact': (differing, length) == (0, 0),
        'tried': tried,
        'skipped': skipped,
        'choices': choices,
        'compiled': size,
        'want': spec['bytes'],
        'source': str(keep) if keep else None,
        'ranked': [{'score': list(item[0]), 'choices': item[1], 'length': item[2]}
                   for item in ranked[:5]],
    }
    if verbose:
        print(f'\ntried {tried} combinations ({skipped} unencodable); best {result["score"]} '
              f'({"EXACT" if result["exact"] else "not exact"})')
        for key, value in choices.items():
            print(f'  {key} = {value}')
        print(f'  length: compiled {size} B, image {spec["bytes"]} B')
        for rank, (current, choices, length, _source) in enumerate(ranked[:5], 1):
            print(f'  {rank}. {current} len={length} ' +
                  ', '.join(f'{k}={v}' for k, v in choices.items())[:120])
    return result


# ---------------------------------------------------------------------------
# Ranking the 197 unmatched rows.  The rank is "smallest first, then rows whose
# disassembly shows one of the three idioms", so a 60-byte loop row is tried
# before a 60-byte straight-line wrapper only when the loop actually exists.


def _load_disassembly(root):
    """Return ``address -> (lines, flags)`` from the dsd main-gap assembly."""
    path = Path(root) / 'asm/_dsd_gap@main_3.s'
    if not path.is_file():
        return {}
    lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    functions = {}
    current = None
    for index, line in enumerate(lines):
        match = re.match(r'^([A-Za-z_.$][\w.$]*): ; 0x([0-9a-fA-F]+)\s*$', line.strip())
        if match:
            current = (int(match.group(2), 16), index)
        if current and re.match(r'^\s*(thumb|arm)_func_end', line):
            functions[current[0]] = (current[1], index)
            current = None
    bodies = {}
    for address, (start, end) in functions.items():
        body = lines[start:end + 1]
        instructions = [line.strip() for line in body
                        if line.strip() and not line.strip().startswith((';', '.', '@'))]
        flags = set()
        if any(re.match(r'stm\w*\s+r\d+!', line) for line in instructions):
            flags.add('writeback-stm')
        if any(re.match(r'ldr\s+r\d+,\s*\.L_', line) for line in instructions):
            flags.add('pool-load')
        labels = {}
        for index, line in enumerate(body):
            match = re.match(r'^(\.L_[0-9a-fA-F]+):', line.strip())
            if match:
                labels[match.group(1)] = index
        for index, line in enumerate(body):
            match = re.match(r'(b\w*)\s+(\.L_[0-9a-fA-F]+)', line.strip())
            if match and match.group(2) in labels and labels[match.group(2)] < index:
                flags.add('loop')
                break
        bodies[address] = (instructions, flags)
    return bodies


def rank_targets(root, module='main', mode='thumb', exclude=()):
    """Rank the unmatched rows of one module/mode by size then idiom."""
    root = Path(root)
    rows = []
    with (root / 'ledger/functions.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            if line.strip():
                rows.append(json.loads(line))
    done = {int(address, 0) if isinstance(address, str) else int(address)
            for address in exclude}
    bodies = _load_disassembly(root)
    ranked = []
    for row in rows:
        if row.get('module') != module or row.get('mode') != mode:
            continue
        if row['matchingBytes'] >= row['bytes'] or row.get('sourceUnit'):
            continue
        address = int(row['address'], 16)
        if address in done:
            continue
        _instructions, flags = bodies.get(address, ([], set()))
        idioms = sorted(flag for flag in flags
                        if flag in ('writeback-stm', 'pool-load', 'loop'))
        ranked.append({
            'address': row['address'],
            'bytes': row['bytes'],
            'symbol': row.get('symbol'),
            'idioms': idioms,
            'rank': (row['bytes'], -len(idioms), address),
        })
    ranked.sort(key=lambda item: item['rank'])
    for position, item in enumerate(ranked, 1):
        item['position'] = position
        del item['rank']
    return ranked


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--spec', help='row spec JSON')
    parser.add_argument('--limit', type=int, default=400)
    parser.add_argument('--time-budget', type=float, default=300.0,
                        help='seconds per row (default 300)')
    parser.add_argument('--top', type=int, default=5)
    parser.add_argument('--keep', help='write the winning source here')
    parser.add_argument('--print', action='store_true', help='print the winning source')
    parser.add_argument('--rank', action='store_true', help='rank the unmatched rows')
    parser.add_argument('--json', help='write the ranking to this file')
    parser.add_argument('--module', default='main')
    parser.add_argument('--exclude', nargs='*', default=[],
                        help='addresses already authored in this batch')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if args.rank:
        ranked = rank_targets(root, args.module, 'thumb', args.exclude)
        for item in ranked:
            print(f'{item["position"]:3d}. {item["address"]:>10} {item["bytes"]:4d} B '
                  f'{",".join(item["idioms"]) or "-"}')
        if args.json:
            Path(args.json).parent.mkdir(parents=True, exist_ok=True)
            Path(args.json).write_text(json.dumps(ranked, indent=1) + '\n', encoding='utf-8')
            print(f'wrote {args.json}')
        return 0
    if not args.spec:
        parser.error('--spec or --rank is required')
    spec = load_spec(Path(args.spec))
    result = search(root, spec, args.limit, args.time_budget, args.keep,
                    verbose=True)
    if args.print and result.get('source'):
        print(Path(result['source']).read_text(encoding='utf-8'))
    return 0 if result.get('exact') else 1


if __name__ == '__main__':
    sys.exit(main())
