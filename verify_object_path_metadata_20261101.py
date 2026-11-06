import shutil
from pathlib import Path
import match_runtime as compiler
from elftools.elf.elffile import ELFFile
from project import ROOT, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def sections(path):
    with path.open('rb') as stream:
        elf = ELFFile(stream)
        return {section.name: dict(bytes=section['sh_size'], allocated=bool(section['sh_flags'] & 2),
            sha256=__import__('hashlib').sha256(section.data()).hexdigest()) for section in elf.iter_sections()}


def main():
    work = ROOT / 'work/object-path-metadata-20261101'
    source = ROOT / 'src/runtime/20261101_callback_stream/native_main_020316b4.c'
    copied = work / 'different-source-directory' / source.name
    copied.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, copied)
    assert sha256(source) == sha256(copied)
    rows, binaries = [], []
    for label, path in [('authored', source), ('copied', copied)]:
        compiler.WORK = work / label / 'compile'
        matches, unused = compiler.compare(path, 'main', 2, 'off')
        assert len(matches) == 1 and matches[0]['exactAfterDeclaredRelocation']
        row = matches[0]
        validate(row, qualified_bindings(row), work / label / 'link')
        rows.append(row)
        binaries.append(work / label / 'link/caller.bin')
    assert rows[0]['sourceSha256'] == rows[1]['sourceSha256']
    assert rows[0]['objectSha256'] != rows[1]['objectSha256']
    assert binaries[0].read_bytes() == binaries[1].read_bytes()
    left, right = [sections(ROOT / row['object']) for row in rows]
    assert set(left) == set(right)
    changed = [name for name in left if left[name] != right[name]]
    assert changed and all(not left[name]['allocated'] and not right[name]['allocated'] for name in changed)
    write_json(ROOT / 'evidence/verification/object-path-metadata-20261101.json', dict(
        generator=Path(__file__).name, generatorSha256=sha256(__file__), source=source.relative_to(ROOT).as_posix(),
        sourceSha256=sha256(source), changedNonallocatedSections=changed,
        objects=[dict(path=row['object'], sha256=row['objectSha256']) for row in rows],
        genuineLinkedBinaries=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in binaries],
        exactLinkedBytes=220, allocatedSectionsUnchanged=True, allSourceBytesUnchanged=True,
        passed=True, newSourceCredit=0,
        limitations=['A source-directory experiment demonstrates debug-object identity variance',
                    'This is not a complete fresh-checkout replay or source-only ROM proof']))
    print(dict(passed=True, changedNonallocatedSections=changed, identicalGenuineLinkedBytes=220, sourceCredit=0))


if __name__ == '__main__':
    main()
