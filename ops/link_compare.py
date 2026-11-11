"""Compare a row two ways: object-patched bytes, and a linked image at its absolute address.

The compiler leaves an interworking call as a plain ``bl`` plus a relocation; the ARM/Thumb
decision belongs to the linker. A comparator that patches relocations itself therefore has to
guess the target mode. This tool makes the difference visible:

1. compile the row exactly as ``ops/compiler_matrix.py`` does, patch the object with
   :mod:`ops.form_search`, and diff against the measured image slice;
2. link the same object at the row's absolute address with the pinned ``mwldarm``, using
   :mod:`ops.form_search`'s measured symbol addresses for undefined data and one stub
   section per branch target placed at its measured address, then diff the linked bytes;
3. for every branch relocation, encode both modes with the project encoder and report which
   one matches the image. That separates "our encoder is wrong" from "our mode guess is wrong".

Linking a Thumb caller to an ARM stub makes ``mwldarm`` emit an interworking veneer rather than
a direct ``blx``; the call site then differs from the image even though the mode is right. Both
facts are reported, because they mean different things.

    python ops/link_compare.py --module ov006 --rows ops/compiler_specs/rows.json \\
        --names 02203ebc,021fb384,021ff02c --json build/link-compare.json
"""

import argparse
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import form_search  # noqa: E402

DATA_KINDS = {2}
BRANCH_KINDS = {10, 30}


def compile_stub(cc, path, obj, root, thumb, symbol):
    """Compile a one-function stub in the requested instruction set."""
    text = f"void {symbol}(void) {{ }}\n"
    source = path.with_suffix('.c')
    source.write_text(text, encoding='utf-8')
    flags = list(form_search.FLAGS)
    if thumb:
        flags = ['-thumb'] + flags
    env = dict(os.environ, LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat'))
    return subprocess.run([str(cc), *flags, '-c', str(source), '-o', str(obj)],
                          capture_output=True, text=True, env=env)


def linker(root, build):
    cc = root / 'tools/mwccarm' / build / 'mwccarm.exe'
    ld = cc.parent / 'mwldarm.exe'
    return cc, ld


def make_lcf(path, address, branch_targets, data_targets):
    lines = ['MEMORY {', f'    row (RWX) : ORIGIN={address:#010x}, LENGTH=0x00001000']
    for index, (_, target) in enumerate(branch_targets):
        lines.append(f'    t{index} (RX) : ORIGIN={target:#010x}, LENGTH=0x00000010')
    lines += ['}', '', 'SECTIONS {']
    for symbol, target in data_targets:
        lines.append(f'    {symbol} = {target:#010x};')
    lines += ['    .text : {', '        row.o (.text)', '        . = ALIGN(4);',
              '    } > row', '    .data : {', '        * (.data)', '        . = ALIGN(4);',
              '    } >> row', '    .bss : {', '        * (.bss)', '        *(COMMON)',
              '        . = ALIGN(4);', '    } >> row']
    for index, (symbol, target) in enumerate(branch_targets):
        lines += [f'    .target{index} : {{', f'        stub{index}.o (.text)',
                  '    } > t' + str(index)]
    lines += ['}', '']
    path.write_text('\n'.join(lines), encoding='utf-8')


def linked_bytes(elf_path, address):
    from elftools.elf.elffile import ELFFile
    with open(elf_path, 'rb') as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section['sh_addr'] == address and section['sh_type'] == 'SHT_PROGBITS':
                return section.data()
    raise ValueError('linked image has no section at the row address')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--rows', required=True)
    parser.add_argument('--names', help='comma-separated row names (default: all)')
    parser.add_argument('--build', default='mwccarm/2.0/base')
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--work', default=None)
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    rows = json.loads(Path(args.rows).read_text(encoding='utf-8'))['rows']
    wanted = set(args.names.split(',')) if args.names else None
    work = Path(args.work or root / 'build/link_compare')
    work.mkdir(parents=True, exist_ok=True)
    image, _, base = form_search.module_image(root, args.module)
    cc, ld = linker(root, args.build)
    if not cc.exists() or not ld.exists():
        raise SystemExit(f'compiler/linker not found under {cc.parent}')

    report = {}
    for row in rows:
        if wanted and row['name'] not in wanted:
            continue
        address = int(row['address'], 0)
        size = row['bytes']
        want = image[address - base:address - base + size]
        source = Path(row['source'])
        if not source.is_absolute():
            source = root / source
        row_work = work / row['name']
        row_work.mkdir(parents=True, exist_ok=True)
        obj = row_work / 'row.o'
        compiled = form_search.compile_source(cc, source, obj, root)
        if compiled.returncode != 0:
            raise SystemExit(f"{row['name']}: compile failed\n{compiled.stderr}")
        text, defined, relocations = form_search.read_object(obj)

        patched = form_search.relocate(text, address, relocations, defined)
        patch_diff = [i for i, (a, b) in enumerate(zip(patched, want)) if a != b]

        branch_targets = []
        data_targets = []
        for _, kind, symbol, _ in relocations:
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            if kind in BRANCH_KINDS:
                branch_targets.append((symbol, target))
            elif kind in DATA_KINDS:
                data_targets.append((symbol, target))
            else:
                raise SystemExit(f"{row['name']}: unsupported relocation {kind} ({symbol})")
        branch_targets = list(dict(branch_targets).items())
        data_targets = list(dict(data_targets).items())

        # The image itself says which mode each call site encodes. Use that to pick the stub
        # mode, and report the evidence; never hide a disagreement.
        mode_of = {}
        modes = {}
        for offset, kind, symbol, addend in relocations:
            if kind not in BRANCH_KINDS:
                continue
            place = address + offset
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            encoded = {}
            for arm in (False, True):
                first, second = form_search.encode_thumb_branch(place, target, addend, arm)
                encoded['arm' if arm else 'thumb'] = struct.pack('<HH', first, second)
            matches = [mode for mode, value in encoded.items() if value == want[offset:offset + 4]]
            modes[hex(offset)] = {'symbol': symbol, 'target': hex(target),
                                  'image_matches': matches,
                                  'encoded': {k: v.hex() for k, v in encoded.items()}}
            if len(matches) == 1:
                mode_of.setdefault(symbol, matches[0])

        stub_objects = []
        for index, (symbol, _) in enumerate(branch_targets):
            stub_path = row_work / f'stub{index}'
            stub_obj = row_work / f'stub{index}.o'
            thumb = mode_of.get(symbol, 'arm') == 'thumb'
            result = compile_stub(cc, stub_path, stub_obj, root, thumb=thumb, symbol=symbol)
            if result.returncode != 0:
                raise SystemExit(f"{row['name']}: stub compile failed\n{result.stderr}")
            stub_objects.append(stub_obj)

        lcf = row_work / 'row.lcf'
        make_lcf(lcf, address, branch_targets, data_targets)
        elf = row_work / 'row.elf'
        env = dict(os.environ,
                   MWLibraries=str(cc.parent),
                   LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat'))
        env.pop('MWLibraryFiles', None)
        command = [str(ld), '-main', '', '-o', str(elf), str(lcf), str(obj)] + \
                  [str(x) for x in stub_objects]
        if any(mode_of.get(symbol, 'arm') == 'arm' for symbol, _ in branch_targets):
            command.insert(1, '-interworking')
        linked = subprocess.run(command, capture_output=True, text=True, env=env)
        if linked.returncode != 0:
            raise SystemExit(f"{row['name']}: link failed\n{linked.stdout}\n{linked.stderr}")
        linked_data = linked_bytes(elf, address)
        link_diff = [i for i, (a, b) in enumerate(zip(linked_data[:size], want)) if a != b]

        verdict = ('DISAPPEARS' if patch_diff and not link_diff and len(linked_data) == size else
                   'STAYS' if patch_diff == link_diff and len(linked_data) == size else
                   'CHANGES' if link_diff else 'EXACT')
        report[row['name']] = {
            'address': row['address'], 'bytes': size,
            'patched': {'diff': len(patch_diff) + abs(len(patched) - size),
                        'offsets': patch_diff, 'size': len(patched)},
            'linked': {'diff': len(link_diff) + abs(len(linked_data) - size),
                       'offsets': link_diff, 'size': len(linked_data),
                       'extra_bytes': len(linked_data) - size},
            'branch_modes': modes,
            'verdict': verdict,
        }
        print(f"\n{row['name']} {row['address']} ({size} B)")
        print(f"  patched diff={report[row['name']]['patched']['diff']} "
              f"offsets={patch_diff} size={len(patched)}")
        print(f"  linked  diff={report[row['name']]['linked']['diff']} "
              f"offsets={link_diff} size={len(linked_data)} (+{len(linked_data) - size})")
        for offset, info in modes.items():
            print(f"  branch @{offset} {info['symbol']} -> {info['target']}: "
                  f"image matches {info['image_matches']}; "
                  f"thumb={info['encoded']['thumb']} arm={info['encoded']['arm']}")
        print(f"  verdict: {verdict}")

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
        print(f'\nwritten {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
