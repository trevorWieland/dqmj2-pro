"""Decide whether a ledger row is genuinely unclaimed by the public source tree.

Every authoring lane needs one answer before it drafts anything: *is this address
already defined?* The ledger's ``functionMatched`` flag cannot answer it, because a
source can land in ``src/`` before the ledger absorbs it (measured on 2026-11-11:
207 rows, 12,156 bytes). Ad-hoc screens also miss two shapes that have already cost
rounds of rework:

* a source file whose **stem** encodes the address while the symbol inside is
  semantically named (``native_main_020685bc.c`` defining
  ``saved_identity_profile_pointer``);
* the same address used by a different overlay, since every overlay loads at
  ``0x021d7240`` — a claim in ``src/ov000`` must not hide an ``ov004`` row.

Source evidence comes first, in three kinds, strongest first:

===========  ===================================================================
``symbol``   a definition whose identifier encodes the address
             (``native_ov000_021e0478``, in C, C++ or assembly)
``file``     a source file whose stem encodes the address, even when the symbol
             inside carries only a semantic name
``data``     a data definition named after the address; it claims the bytes but
             does not prove a function body
===========  ===================================================================

A *mention* — an ``extern`` declaration, a prototype, a call site, a comment or an
immediate operand — is never a claim. Claims are **module-scoped**: the module is
inferred from the symbol tokens and from every path component, so ``src/ov000/...``
cannot claim an ``ov004`` row that happens to share the address. A claim whose
module cannot be inferred is reported as ``unscoped`` and still counts as a claim.

Ledger state is secondary. A row is listed as genuinely unclaimed when the source
tree has no claim for it; ``functionMatched`` then only moves confidence:

* ``high`` — unmatched in the ledger and no mention anywhere in ``src/``;
* ``medium`` — unmatched in the ledger but the address is mentioned in ``src/``
  (a caller or a leftover declaration exists, so something may still surface);
* ``low`` — the ledger says matched while no claim exists (an *inverse* row). It is
  not unclaimed by definition, so it is only listed with ``--include-inverse``.

    python ops/unclaimed.py --module ov000
    python ops/unclaimed.py --all --json work/unclaimed.json
    python ops/unclaimed.py --check-addresses 0x021FBB04 main:0x020685bc \
        --address-file work/batch.txt

``--check-addresses`` exits 1 when any address in the batch is already defined, so
a packet build can gate on it. A bare address is checked against every module; a
``module:address`` line is checked against that module only, plus unscoped claims.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ('main', 'itcm', 'dtcm', 'ov000', 'ov001', 'ov002', 'ov003', 'ov004',
           'ov005', 'ov006', 'ov007', 'arm7-boot', 'arm7-wram', 'arm7-main',
           'utility-child-arm9-main', 'utility-child-arm9-itcm',
           'utility-child-arm9-dtcm', 'utility-child-arm7-boot',
           'utility-child-arm7-wram', 'utility-child-arm7-main')
SOURCES = ('.c', '.s', '.inc', '.cpp')
HEADERS = ('.h', '.hpp')
HEX8 = re.compile(r'[0-9a-f]{8}')
HEX8_ANY = re.compile(r'[0-9a-f]{8}', re.I)
COMMENTS = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)
DEFINITION = re.compile(r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(')
DATA_DEFINITION = re.compile(
    r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[[^\]]*\]\s*)?(?:=|;)')
ASM_EXPORT = re.compile(r'^\s*\.(?:global|globl|type)\s+([A-Za-z_][A-Za-z0-9_]*)')
ASM_LABEL = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):')
KEYWORDS = frozenset((
    'if', 'for', 'while', 'switch', 'return', 'sizeof', 'do', 'else', 'case',
    'typedef', 'struct', 'union', 'enum', 'static', 'const', 'volatile',
))
ALIASES = tuple((module, tuple(module.replace('-', '_').split('_'))) for module in MODULES)
TOKENS = re.compile(r'[^a-z0-9]+')


class Claim:
    """One definition of an address in the public tree."""

    __slots__ = ('address', 'source', 'symbol', 'kind', 'modules')

    def __init__(self, address, source, symbol, kind, modules):
        self.address = address
        self.source = source
        self.symbol = symbol
        self.kind = kind
        self.modules = tuple(sorted(modules))

    @property
    def scoped(self):
        return bool(self.modules)

    def applies_to(self, module):
        return not self.modules or module in self.modules

    def as_dict(self):
        return {'address': self.address, 'source': self.source, 'symbol': self.symbol,
                'kind': self.kind, 'modules': list(self.modules),
                'scoped': self.scoped}

    def __repr__(self):
        scope = ','.join(self.modules) if self.modules else 'unscoped'
        return f'Claim({self.address} {self.kind} {scope} {self.source})'


class SourceIndex:
    """Claims and mentions for the ledger addresses, built from one src/ pass."""

    def __init__(self, claims, mentions, files):
        self.claims = claims      # address -> [Claim]
        self.mentions = mentions  # address -> set(source paths)
        self.files = files        # number of source files scanned

    def claims_for(self, address, module=None):
        found = self.claims.get(address, ())
        if module is None:
            return list(found)
        return [claim for claim in found if claim.applies_to(module)]


def _tokens(text):
    return [part for part in TOKENS.split(text.lower()) if part]


def modules_in(text):
    """Modules named by contiguous tokens of ``text`` (symbols, path components)."""
    tokens = _tokens(text)
    found = set()
    for module, alias in ALIASES:
        width = len(alias)
        for start in range(len(tokens) - width + 1):
            if tuple(tokens[start:start + width]) == alias:
                found.add(module)
                break
    return found


def _addresses(text):
    return {match.group(0) for match in HEX8.finditer(text.lower())}


def _c_definitions(text):
    """Names defined in a C-family translation unit, comments already stripped."""
    lines = text.splitlines()
    names = []
    for index, line in enumerate(lines):
        if not line or line[0] in ' \t#':
            continue
        if not HEX8_ANY.search(line):
            continue  # a claim must encode the address in its identifier
        if line.startswith('extern') or line.startswith('typedef'):
            continue
        match = DEFINITION.match(line)
        if match:
            name = match.group(1)
            if name in KEYWORDS:
                continue
            tail = line[match.end() - 1:]
            if tail.rstrip().endswith(';'):
                continue  # prototype or declaration
            if '{' not in tail:
                # The header may wrap across lines before the body opens; a
                # declaration closes with ';' first, so scanning forward until
                # either token decides it without guessing.
                body = False
                for following in lines[index + 1:index + 8]:
                    if '{' in following:
                        body = True
                        break
                    if following.rstrip().endswith(';'):
                        break
                if not body:
                    continue
            names.append((name, 'symbol'))
            continue
        match = DATA_DEFINITION.match(line)
        if match:
            name = match.group(1)
            if name in KEYWORDS:
                continue
            if '=' in line or line.rstrip().endswith(';'):
                names.append((name, 'data'))
    return names


def _asm_symbols(text):
    names = []
    for line in text.splitlines():
        if not HEX8_ANY.search(line):
            continue  # exported labels must encode the address to claim a row
        match = ASM_EXPORT.match(line) or ASM_LABEL.match(line)
        if match:
            names.append((match.group(1), 'symbol'))
    return names


def scan_sources(root=ROOT, wanted=None):
    """Scan ``src/`` once and return a :class:`SourceIndex`.

    ``wanted`` restricts mention tracking to those addresses; claims are always
    collected for every address.
    """
    root = Path(root)
    claims = {}
    mentions = {}
    files = 0
    for path in (root / 'src').rglob('*'):
        suffix = path.suffix.lower()
        if not path.is_file() or suffix not in SOURCES + HEADERS:
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        relative = path.relative_to(root).as_posix()
        body = text if suffix == '.s' else COMMENTS.sub('', text)
        # A file can carry the address only in its stem (native_main_020685bc.c),
        # so the prefilter must look at the name as well as the text, and mentions
        # are read from the raw text so a comment still counts as soft evidence.
        stem_addresses = _addresses(path.stem)
        present = _addresses(text) | stem_addresses
        if wanted is not None and not present & wanted:
            continue
        files += 1
        found = {}
        if wanted is None or (_addresses(body) | stem_addresses) & wanted:
            definitions = _asm_symbols(text) if suffix == '.s' else _c_definitions(body)
            for name, kind in definitions:
                hit = _addresses(name)
                if not hit:
                    continue
                modules = modules_in(name)
                for address in hit:
                    found[address] = kind
                    claims.setdefault(address, []).append(
                        Claim(address, relative, name, kind, modules))
        if suffix not in HEADERS and stem_addresses:
            parent = relative.rsplit('/', 1)[0] if '/' in relative else ''
            modules = modules_in(parent + ' ' + path.stem)
            for address in stem_addresses:
                found.setdefault(address, 'file')
                claims.setdefault(address, []).append(
                    Claim(address, relative, None, 'file', modules))
        if wanted:
            for address in present & wanted:
                if address not in found:
                    mentions.setdefault(address, set()).add(relative)
    return SourceIndex(claims, mentions, files)


def load_rows(root=ROOT, path=None):
    """Ledger rows with measured bytes, in ledger order."""
    source = Path(path) if path else Path(root) / 'ledger/functions.jsonl'
    rows = []
    for line in source.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get('bytes'):
            rows.append(row)
    return rows


def address_key(row):
    return '%08x' % int(row['address'], 16)


def classify(root=ROOT, module=None, index=None):
    """Classify every ledger row; return ``(records, summary)``.

    Statuses: ``claimed`` (source claim, ledger unmatched), ``consistent`` (claim
    and ledger agree), ``data-claimed`` (only a data definition), ``inverse``
    (ledger matched, no claim), ``unclaimed`` (no claim, ledger unmatched).
    """
    rows = load_rows(root)
    if module and module != 'all':
        rows = [row for row in rows if row['module'] == module]
    wanted = {address_key(row) for row in rows}
    index = index or scan_sources(root, wanted=wanted)
    records = []
    summary = {'rows': len(rows), 'files': index.files, 'unclaimed': 0,
               'unclaimedBytes': 0, 'claimed': 0, 'consistent': 0,
               'dataClaimed': 0, 'inverse': 0,
               'byModule': {}, 'byConfidence': {}}
    for row in rows:
        address = address_key(row)
        claims = index.claims_for(address, row['module'])
        matched = bool(row['states'].get('functionMatched'))
        mentions = len(index.mentions.get(address, ()))
        strong = [claim for claim in claims if claim.kind != 'data']
        if strong:
            status = 'consistent' if matched else 'claimed'
            confidence = 'high'
        elif claims:
            status = 'data-claimed'
            confidence = 'medium'
        elif matched:
            status, confidence = 'inverse', 'low'
        else:
            status = 'unclaimed'
            confidence = 'medium' if mentions else 'high'
        record = {
            'address': row['address'], 'key': address, 'module': row['module'],
            'bytes': row['bytes'], 'mode': row['mode'], 'status': status,
            'confidence': confidence, 'mentions': mentions,
            'ledgerMatched': matched,
            'claims': [claim.as_dict() for claim in claims],
        }
        records.append(record)
        if status == 'unclaimed':
            summary['unclaimed'] += 1
            summary['unclaimedBytes'] += record['bytes']
            bucket = summary['byModule'].setdefault(
                record['module'], {'rows': 0, 'bytes': 0})
            bucket['rows'] += 1
            bucket['bytes'] += record['bytes']
            summary['byConfidence'][confidence] = \
                summary['byConfidence'].get(confidence, 0) + 1
        elif status == 'claimed':
            summary['claimed'] += 1
        elif status == 'consistent':
            summary['consistent'] += 1
        elif status == 'data-claimed':
            summary['dataClaimed'] += 1
        else:
            summary['inverse'] += 1
    return records, summary


def displayed(records, include_inverse=False):
    return [record for record in records
            if record['status'] == 'unclaimed'
            or (include_inverse and record['status'] == 'inverse')]


def parse_target(text):
    """``module:0xADDR`` or ``0xADDR`` -> (module or None, 8-hex key)."""
    text = text.strip()
    if not text or text.startswith('#'):
        return None, None
    module = None
    if ':' in text:
        module, text = text.split(':', 1)
        module = module.strip() or None
        if module and module not in MODULES:
            raise ValueError(f'unknown module: {module}')
    text = text.strip()
    if re.fullmatch(r'(?:0x)?[0-9a-fA-F]{1,8}', text) is None:
        raise ValueError(f'not an address: {text}')
    return module, '%08x' % int(text, 16)


def check_addresses(root, targets):
    """Return (results, blocked count) for a batch of (module, address) targets."""
    wanted = {key for _, key in targets}
    index = scan_sources(root, wanted=wanted)
    results = []
    blocked = 0
    for module, key in targets:
        claims = index.claims_for(key, module)
        hit = bool(claims)
        blocked += 1 if hit else 0
        results.append({'module': module, 'address': '0x' + key, 'defined': hit,
                        'claims': [claim.as_dict() for claim in claims],
                        'mentions': sorted(index.mentions.get(key, ()))[:5]})
    return results, blocked


def write_report(path, records, summary):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({'summary': summary, 'rows': records}, indent=1) + '\n',
                      encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--module', default=None,
                        help='ledger module (ov000, main, arm7-wram, ...) or "all"')
    parser.add_argument('--all', action='store_true', help='every module')
    parser.add_argument('--json', dest='json_path', default=None)
    parser.add_argument('--check-addresses', nargs='*', default=None,
                        help='addresses to gate: 0xADDR or module:ADDR')
    parser.add_argument('--address-file', default=None,
                        help='one 0xADDR or module:ADDR per line')
    parser.add_argument('--include-inverse', action='store_true',
                        help='also list ledger-matched rows with no source claim')
    parser.add_argument('--limit', type=int, default=None)
    parser.add_argument('--quiet', action='store_true', help='summary only')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.check_addresses is not None:
        targets = []
        for text in args.check_addresses:
            for piece in text.replace(',', ' ').split():
                targets.append(parse_target(piece))
        if args.address_file:
            for line in Path(args.address_file).read_text(encoding='utf-8').splitlines():
                targets.append(parse_target(line))
        targets = [target for target in targets if target[0] or target[1]]
        if not targets:
            parser.error('no addresses given')
        results, blocked = check_addresses(root, targets)
        for result in results:
            label = f"{result['module']}:{result['address']}" if result['module'] \
                else result['address']
            print(f"{'BLOCKED' if result['defined'] else 'clear':8s} {label}")
            for claim in result['claims']:
                scope = ','.join(claim['modules']) or 'unscoped'
                print(f"           claim: {claim['kind']:6s} {claim['source']}"
                      f" ({scope}) {claim['symbol'] or ''}".rstrip())
            if not result['defined']:
                for mention in result['mentions']:
                    print(f"           mention: {mention}")
        print(f'\n{len(results)} addresses, {blocked} already defined under src/')
        return 1 if blocked else 0

    if args.all or args.module in (None, 'all'):
        module = 'all'
    else:
        module = args.module
        if module not in MODULES:
            parser.error(f'unknown module: {module}')
    records, summary = classify(root, module)
    shown_records = displayed(records, args.include_inverse)
    if not args.quiet:
        print(f"'{module}' ledger rows with bytes: {summary['rows']}")
        print(f"genuinely unclaimed: {summary['unclaimed']} rows, "
              f"{summary['unclaimedBytes']} bytes "
              f"({summary['files']} source files scanned)")
        print(f"  claimed by source: {summary['claimed']}, "
              f"consistent: {summary['consistent']}, "
              f"data-claimed: {summary['dataClaimed']}, "
              f"inverse: {summary['inverse']}")
        print(f"  by confidence: {summary['byConfidence']}")
        print(f"\n{'address':>12s} {'module':8s} {'bytes':>5s} {'mode':5s} "
              f"{'confidence':10s} {'mentions':>8s}")
        shown = 0
        for record in shown_records:
            if args.limit is not None and shown >= args.limit:
                print(f'  ... {len(shown_records) - shown} more')
                break
            print(f"{record['address']:>12s} {record['module']:8s} "
                  f"{record['bytes']:5d} {record['mode']:5s} "
                  f"{record['confidence']:10s} {record['mentions']:8d}")
            shown += 1
    else:
        print(json.dumps({'summary': summary}))
    if args.json_path:
        write_report(args.json_path, records, summary)
        print(f'report written: {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
