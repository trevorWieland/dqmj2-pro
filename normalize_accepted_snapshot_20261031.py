import argparse
import copy
import hashlib
import json
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    args = parser.parse_args()
    source = ROOT / f'evidence/verification/accepted-cohort{args.cohort}-identities-20261031.json'
    snapshot = read_json(source)
    raw = (ROOT / 'manifest.json').read_bytes()
    manifest = json.loads(raw)
    assert snapshot['romSha256'] == manifest['rom']['sha256']
    modules = {row['name']: row for row in manifest['modules']}
    assert len(modules) == len(manifest['modules'])
    changes, functions = [], []
    for index, original in enumerate(snapshot['functions']):
        item = copy.deepcopy(original)
        module = modules[item['module']]
        for field, default in [('processor', module['processor']), ('program', module.get('program') or '')]:
            if item.get(field) in [None, ''] and item.get(field) != default:
                changes.append(dict(index=index, address=item['address'], module=item['module'],
                                    field=field, previous=item.get(field), normalized=default))
                item[field] = default
            assert item.get(field, '') == default
        assert item['processor'] in ['arm9', 'arm7']
        functions.append(item)
    output = dict(acceptedCohort=args.cohort, romSha256=snapshot['romSha256'],
                  functions=functions, normalization=dict(input=source.relative_to(ROOT).as_posix(),
                  inputSha256=sha256(source), moduleMetadata='manifest.json',
                  moduleMetadataSha256=hashlib.sha256(raw).hexdigest(), changes=changes,
                  sourceCredit=0, historicalSnapshotModified=False))
    target = ROOT / f'evidence/verification/accepted-cohort{args.cohort}-identities-v2-20261031.json'
    if target.exists():
        existing = read_json(target)
        assert existing['functions'] == functions and existing['romSha256'] == snapshot['romSha256']
        assert existing['normalization']['inputSha256'] == sha256(source)
        print(dict(existingFrozenSnapshotRetained=True, functions=len(functions), sourceCredit=0))
        return
    write_json(target, output)
    print(dict(functions=len(functions), normalizedFields=len(changes), sourceCredit=0))


if __name__ == '__main__':
    main()
