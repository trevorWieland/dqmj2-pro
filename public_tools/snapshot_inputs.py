import re
import shutil
from pathlib import PurePosixPath


MUTABLE_ROOTS = {'recovery.json', 'source-preferences.json', 'interpreted-recovery.json',
                 'manifest.json', 'recovery-ownership.json', 'source-map.json'}
MUTABLE_DIRECTORIES = {'evidence', 'provenance', 'ledger', 'generated', 'nonmatching', 'src', 'work'}


def apply_snapshot_files(root, bundle, stage, records, seen, entries, member_path, digest, error):
    if not isinstance(entries, list):
        raise error('Invalid frozen snapshot file inventory')
    positions = {target.relative_to(root).as_posix(): index for index, (target, unused, sha) in enumerate(records)}
    canonical = {name.casefold(): name for name in seen}
    updates = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) - {'path', 'sha256', 'bytes', 'replacesSha256'}:
            raise error('Invalid frozen snapshot file record')
        name, expected, size = entry.get('path'), entry.get('sha256'), entry.get('bytes')
        if not isinstance(name, str) or not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            raise error('Invalid frozen snapshot identity')
        if type(size) is not int or size < 0:
            raise error('Invalid frozen snapshot file length')
        relative, target = member_path(root, name)
        name = relative.as_posix()
        folded = name.casefold()
        if folded in updates or folded in canonical and canonical[folded] != name:
            raise error('Duplicate frozen snapshot path')
        updates.add(folded)
        position = positions.get(name)
        if 'replacesSha256' in entry:
            previous = entry['replacesSha256']
            metadata = relative.suffix in {'.json', '.jsonl'} and (
                name in MUTABLE_ROOTS or relative.parts[0] in MUTABLE_DIRECTORIES)
            if not metadata or not isinstance(previous, str) or not re.fullmatch('[0-9a-f]{64}', previous):
                raise error('Only pinned snapshot metadata may replace an archive member')
            if position is None or records[position][2] != previous or previous == expected:
                raise error('Frozen snapshot predecessor identity differs')
        elif name in seen:
            raise error('Frozen snapshot addition duplicates an archive path')
        source = bundle / 'snapshot-files' / expected
        if any(path.is_symlink() or getattr(path, 'is_junction', lambda: False)()
               for path in (source, source.parent)) or not source.resolve().is_relative_to(bundle):
            raise error('Frozen snapshot payload traverses a link')
        if not source.is_file() or source.stat().st_size != size or digest(source) != expected:
            raise error('Frozen snapshot payload identity differs')
        staged = stage.joinpath(*PurePosixPath(name).parts)
        staged.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, staged)
        if digest(staged) != expected or digest(source) != expected:
            raise error('Frozen snapshot payload changed during staging')
        record = (target, staged, expected)
        if position is None:
            records.append(record)
            seen.add(name)
        else:
            records[position] = record
    return len(updates)
