#!/usr/bin/env python3
"""Accept a decomp-permuter result only through the project's own measurement path.

A permuter score of 0 is decomp-permuter diffing two objdump streams. That is not the
project's acceptance rule and must never be treated as one: the ledger is matched by
compiling with the pinned mwccarm, applying the thumb/arm branch and absolute
relocations, and comparing the resulting bytes with the module image. This gate does
exactly that, independently of anything the permuter reported, and refuses to pass
unless a set of controls also behaves.

    python ops/verify_permuter.py work/permuter/ov006_02203ebc_sp1 --source best.c

Checks, in order (all must pass):

1. **workspace integrity** -- the module image still hashes to the recorded value and
   ``target.o``'s ``.text`` is the recorded image slice with the recorded relocation
   slots zeroed. This proves the search was aimed at the right bytes.
2. **negative control: the base source** -- the unchanged best-known source must NOT
   reproduce the row. If it did, the permuter run proved nothing.
3. **positive: byte + relocation exactness** -- the candidate source is compiled with
   the row's compiler, flags and mode; its instruction bytes, after expanding branch
   and absolute relocations, must equal the image slice exactly (score ``(0, 0)``).
4. **absolute text equality** -- with the relocation slots zeroed, the candidate's
   ``.text`` must equal ``target.o``'s ``.text`` byte for byte.
5. **relocation identity** -- the candidate must reference the same symbols at the same
   offsets as the base object. This is the anti-cheat for the byte compare: a candidate
   that silently dropped a call or a data reference cannot pass.
6. **negative controls: shifted slices** -- the candidate must not also reproduce the
   image two bytes before/after the row. A comparison that passes on shifted data is a
   comparison bug, not a match.

The receipt (``<workspace>/receipt.json``, plus ``--json``) records the candidate hash,
the compiler hash, the permuter pin, every check result and the exact commands. No ROM
bytes are written; only hashes.

Exit status 0 only when every check passes.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import form_search  # noqa: E402  the project's compile/relocate/score path
import permuter    # noqa: E402


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def project_path(path):
    """Repo-relative when possible, so a committed receipt is not machine-specific.

    The as-given path is tried before resolving symlinks/junctions: this checkout shares
    tools/ and extract/ with the private tree through links, and the receipt should name
    the path the project uses, not the link target.
    """
    raw = Path(path)
    if not raw.is_absolute():
        raw = ROOT / raw
    for candidate in (raw, raw.resolve()):
        try:
            return candidate.relative_to(ROOT).as_posix()
        except ValueError:
            continue
    return raw.resolve().as_posix()


class Checker:
    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve()
        self.checks = []

    def check(self, name, ok, detail=''):
        self.checks.append({'name': name, 'ok': bool(ok), 'detail': detail})
        print(f'{"PASS" if ok else "FAIL"}  {name}' + (f'  ({detail})' if detail else ''))
        return ok

    def failed(self):
        return [entry for entry in self.checks if not entry['ok']]


def measure(row, source, scratch, modes):
    """Compile one source with the row's settings and return the relocated bytes."""
    flags = row['flags']
    thumb = bool(row['thumb'])
    compiler = row['compiler']
    obj = scratch / (Path(source).stem + '.o')
    built = permuter.compile_object(ROOT, source, obj, flags, thumb, compiler=compiler)
    if built.returncode != 0:
        raise RuntimeError('compile failed: ' + (built.stderr or built.stdout).strip()[:400])
    text, defined, relocations = form_search.read_object(obj)
    address = int(row['address'], 16)
    # modes resolves BL vs BLX from the branch *target*; without it every Thumb call is
    # patched as BL and any row that calls ARM code shows a phantom 2-byte mismatch.
    actual = form_search.relocate(text, address, relocations, defined, modes=modes)
    return {'text': text, 'relocations': relocations, 'actual': actual,
            'object': str(obj), 'objectSha256': sha256_file(obj)}


def verify(workspace, source_name, json_path, emit_path):
    checker = Checker(workspace)
    workspace = checker.workspace
    row_path = workspace / 'row.json'
    if not row_path.is_file():
        print(f'FAIL  workspace metadata: {row_path} is missing')
        return 1
    row = json.loads(row_path.read_text(encoding='utf-8'))
    address = int(row['address'], 16)
    size = row['bytes']
    scratch = workspace / '.build'
    scratch.mkdir(exist_ok=True)

    # 1. workspace integrity, straight from the module image.
    image, base, image_path = permuter.module_info(ROOT, row['module'])
    checker.check('module image hash matches the workspace',
                  sha256_bytes(image) == row['imageSha256'],
                  f'{image_path.name}')
    offset = address - base
    image_slice = image[offset:offset + size]
    expected = bytearray(image_slice)
    for slot_offset, _kind, _symbol in row['target']['slots']:
        expected[slot_offset:slot_offset + 4] = b'\0\0\0\0'
    target_text, _ = permuter.object_text(workspace / 'target.o')
    checker.check('target.o is the image slice with relocation slots zeroed',
                  bytes(target_text) == bytes(expected) and len(expected) == size,
                  f'{size} B, {len(row["target"]["slots"])} slot(s)')

    # 2. negative control: the base source must not already match.
    modes = form_search.TargetModes(ROOT, row['module'])
    base_source = workspace / 'base.c'
    base = measure(row, base_source, scratch, modes)
    base_score, _ = form_search.score(base['actual'], image_slice)
    checker.check('negative control: base.c does NOT reproduce the row',
                  base_score != 0, f'score {base_score}')

    # 3. the positive result, through the project's measurement path.
    candidate_path = Path(source_name)
    if not candidate_path.is_absolute():
        candidate_path = workspace / candidate_path
    if not candidate_path.is_file():
        checker.check(f'candidate source exists: {candidate_path}', False)
        return report(checker, workspace, row, json_path, None, None)
    candidate = measure(row, candidate_path, scratch, modes)
    score, length_delta = form_search.score(candidate['actual'], image_slice)
    exact = score == 0 and length_delta == 0
    checker.check('byte + relocation exactness against the module image', exact,
                  f'score ({score}, {length_delta}), {len(candidate["actual"])} B')

    # 4. absolute text equality against the workspace target.
    candidate_text = bytearray(candidate['text'])
    for slot_offset, _kind, _symbol in row['target']['slots']:
        if slot_offset + 4 <= len(candidate_text):
            candidate_text[slot_offset:slot_offset + 4] = b'\0\0\0\0'
    checker.check('candidate .text equals target .text with slots zeroed',
                  bytes(candidate_text) == bytes(target_text),
                  f'{len(candidate_text)} B')

    # 5. relocation identity: same symbols, same offsets, same kinds.
    #    read_object() hands back (offset, kind, symbol, addend); the addend is an
    #    encoding artefact of mwcc's branch relocations and is not part of identity.
    slot_key = lambda entries: sorted((entry[0], entry[1], entry[2]) for entry in entries)
    checker.check('candidate relocations identical to the base object',
                  slot_key(candidate['relocations']) == slot_key(base['relocations']),
                  f'{len(candidate["relocations"])} relocation(s)')

    # 6. negative controls: the same bytes must not match a shifted slice.
    step = 2 if row['thumb'] else 4
    for shift in (-step, step):
        shifted_offset = offset + shift
        if shifted_offset < 0 or shifted_offset + size > len(image):
            continue
        shifted = image[shifted_offset:shifted_offset + size]
        shifted_score, _ = form_search.score(candidate['actual'], shifted)
        checker.check(f'negative control: candidate does not match the slice at {shift:+d}',
                      shifted_score != 0, f'score {shifted_score}')

    source_text = candidate_path.read_text(encoding='utf-8')
    accepted = None
    if not checker.failed() and emit_path:
        destination = Path(emit_path)
        if not destination.is_absolute():
            destination = ROOT / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source_text, encoding='utf-8')
        accepted = str(destination)
        print(f'emitted accepted source: {destination}')
    return report(checker, workspace, row, json_path, candidate_path, {
        'score': [score, length_delta],
        'sourceSha256': sha256_bytes(source_text.encode('utf-8')),
        'objectSha256': candidate['objectSha256'],
        'baseScore': base_score,
        'checks': checker.checks,
        'acceptedSource': accepted,
    })


def report(checker, workspace, row, json_path, candidate_path, detail):
    failures = checker.failed()
    receipt = {
        'kind': 'permuter-acceptance',
        'generatedAt': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'workspace': project_path(workspace),
        'module': row['module'],
        'address': row['address'],
        'bytes': row['bytes'],
        'mode': row['mode'],
        'symbol': row['symbol'],
        'image': row['image'],
        'imageSliceSha256': row['imageSliceSha256'],
        'compiler': project_path(row['compiler']),
        'compilerSha256': sha256_file(Path(row['compiler'])),
        'flags': row['flags'],
        'permuterPin': row['permuterPin'],
        'candidate': project_path(candidate_path) if candidate_path else None,
        'checks': checker.checks,
        'passed': not failures,
    }
    if detail:
        receipt.update(detail)
    destination = Path(json_path) if json_path else workspace / 'receipt.json'
    if not destination.is_absolute():
        destination = ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(f'\nreceipt: {destination}')
    if failures:
        print(f'{len(failures)} check(s) failed; the result is NOT accepted')
        return 1
    print('all checks passed; the result is accepted by the project measurement path')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('workspace', help='generated permuter workspace (holds row.json)')
    parser.add_argument('--source', default='best.c',
                        help='candidate C source, relative to the workspace (default best.c)')
    parser.add_argument('--json', help='receipt path (default <workspace>/receipt.json)')
    parser.add_argument('--emit', help='copy the accepted source here when every check passes')
    args = parser.parse_args(argv)
    try:
        return verify(args.workspace, args.source, args.json, args.emit)
    except (RuntimeError, ValueError) as error:
        print(f'FAIL  {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
