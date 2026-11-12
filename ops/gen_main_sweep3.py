"""Generate the main-sweep3 transcription lane.

Each row is emitted as one address-named translation unit whose body is the row's
measured instruction stream, decoded from ``extract/arm9/arm9.bin`` and spelled in
the mwccarm assembler dialect. The decode/spelling engine is
``ops/transcribe_chunk.py`` (the round-8 transcriber) driven by the Capstone
renderer in ``ops/capstone_disasm.py``, because the pinned LLVM objdump that
``ops/disasm.py`` shells out to is not installed in this checkout.

The lane's plan file carries the two judgement fields per row (``purpose`` and
``unknowns``); everything else is read from the image:

    python ops/gen_main_sweep3.py --plan ops/main_sweep3_plan.json
    python ops/gen_main_sweep3.py --plan ops/main_sweep3_plan.json --check

``--check`` writes nothing and reports which planned rows would be refused, which
is how a row that is really data (or that hides a pool word the assembler cannot
reproduce) is caught before the verifier runs.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import capstone_disasm  # noqa: E402
capstone_disasm.install()
import transcribe_chunk  # noqa: E402

LANE = ROOT / 'src/verified_assembly/20261112_main_sweep3'
DEFAULT_PLAN = Path(__file__).resolve().parent / 'main_sweep3_plan.json'


def target(row, plan):
    directory = LANE / (row['module'] if row['mode'] == 'arm' else row['module'] + '_thumb')
    return directory / ('native_%s_%08x.c' % (row['module'].replace('-', '_'),
                                              int(row['address'], 16)))


def retitle(text):
    """Correct the copy classifier's fallback label for non-copy rows.

    ``transcribe_chunk.describe`` was written for the aggregate-copy class and has
    no label for an ordinary instruction run, so it prints "aggregate copy" for a
    forwarder or a getter. Saying that in the header would be false; the
    replacement states what the body actually is.
    """
    return text.replace(' * Decoded shape: aggregate copy.',
                        ' * Decoded shape: no aggregate-copy shape (an ordinary instruction run).')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--plan', type=Path, default=DEFAULT_PLAN)
    parser.add_argument('--check', action='store_true', help='report, write nothing')
    parser.add_argument('--only', nargs='*', default=None, help='limit to these addresses')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8'))['rows']
    wanted = {int(item['address'][2:], 16) for item in plan} if args.only is None \
        else {int(value, 0) for value in args.only}
    written, refused, bytes_written = [], [], 0
    for item in plan:
        address = int(item['address'], 0)
        if address not in wanted:
            continue
        row = transcribe_chunk.row_for(item['module'], address)
        if row is None:
            refused.append((address, 'not in the ledger'))
            continue
        try:
            text = transcribe_chunk.emit(item['module'], row, item['purpose'],
                                         item['unknowns'], constant_aliases=True,
                                         unique_pool_slots=True)
            text = retitle(text)
        except SystemExit as error:
            refused.append((address, str(error)))
            continue
        except Exception as error:  # noqa: BLE001
            refused.append((address, '%s: %s' % (type(error).__name__, error)))
            continue
        path = target(row, item)
        written.append((address, int(row['bytes']), path))
        bytes_written += int(row['bytes'])
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='ascii')
    for address, size, path in written:
        print('%08x %4d B %s' % (address, size, path.relative_to(ROOT).as_posix()))
    for address, reason in refused:
        print('%08x REFUSED %s' % (address, reason))
    print('\n%d written, %d refused, %d bytes%s'
          % (len(written), len(refused), bytes_written, ' (check only)' if args.check else ''))
    return 1 if refused else 0


if __name__ == '__main__':
    sys.exit(main())
