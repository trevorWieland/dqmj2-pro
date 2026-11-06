import argparse
import base64
from pathlib import Path
import shutil
from project import ROOT, read_json, write_json, sha256, now


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--path', action='append', required=True)
    options = parser.parse_args()
    if not options.label.replace('-', '').isalnum():
        raise ValueError('Failure label must be an ASCII alphanumeric slug')
    destination = ROOT / 'evidence/attempts' / ('cohort' + str(options.cohort) + '-' + options.label)
    if destination.exists():
        raise ValueError('Failure archive already exists; preserve its original bytes')
    destination.mkdir(parents=True)
    records = []
    for name in options.path:
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or path.suffix not in ('.json', '.txt'):
            raise ValueError('Failure evidence must be a local existing JSON or text file')
        target = destination / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == '.json':
            shutil.copyfile(path, target)
            if sha256(path) != sha256(target):
                raise ValueError('Failure archive differs from original evidence')
        else:
            target = target.with_suffix('.text-bytes.json')
            write_json(target, dict(originalPath=name, originalSha256=sha256(path),
                originalBytesBase64=base64.b64encode(path.read_bytes()).decode('ascii'), sourceCredit=0))
        records.append(dict(original=name, originalSha256=sha256(path),
            archived=target.relative_to(ROOT).as_posix(), archivedSha256=sha256(target)))
    write_json(destination / 'receipt.json', dict(createdUtc=now(), cohort=options.cohort,
        sourceCredit=0, failurePreserved=True, liveFilesChanged=False, files=records))
    print(dict(archive=destination.relative_to(ROOT).as_posix(), files=len(records), sourceCredit=0))


if __name__ == '__main__':
    main()
