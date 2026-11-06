import argparse
from copy import deepcopy
from project import ROOT, read_json, write_json, sha256, now
from recovery_order import order_batches


def amend(registry, pins, root=ROOT):
    provider = pins['startupReport']
    batches = {row['report']: row for row in registry['batches']}
    if provider not in batches:
        raise ValueError('Embedded startup producer is not registered')
    startup = read_json(root / provider)
    if startup['romSha256'] != pins['romSha256']:
        raise ValueError('Embedded startup ROM namespace differs')
    for pin in pins['frozenInputs']:
        if sha256(root / pin['path']) != pin['sha256']:
            raise ValueError('Immutable utility inventory changed: ' + pin['path'])
    result, changes = deepcopy(registry), []
    for batch in result['batches']:
        if 'utility_code.py' not in batch.get('sourceHashes', {}):
            continue
        report = read_json(root / batch['report'])
        if not any(row.get('module', '').startswith('utility-child-') for row in report.get('matches', [])):
            continue
        if batch['report'] == provider or report['romSha256'] != pins['romSha256']:
            raise ValueError('Utility consumer startup/build namespace differs')
        requires = batch.get('replayRequires', [])
        if not isinstance(requires, list) or not all(isinstance(path, str) for path in requires):
            raise ValueError('Replay prerequisites must be report paths')
        batch['replayRequires'] = list(dict.fromkeys([*requires, provider]))
        for pin in pins['frozenInputs']:
            previous = batch['sourceHashes'].get(pin['path'])
            if previous is not None and previous != pin['sha256']:
                raise ValueError('Refusing to replace an existing inventory identity')
            batch['sourceHashes'][pin['path']] = pin['sha256']
        changes.append(batch['report'])
    if not changes:
        raise ValueError('No embedded utility consumers require this repair')
    ordered = order_batches(result['batches'], root=root)
    positions = {row['report']: index for index, row in enumerate(ordered)}
    if not all(positions[provider] < positions[path] for path in changes):
        raise ValueError('Startup provider was not ordered before utility consumers')
    for old, new in zip(registry['batches'], result['batches']):
        for field in set(old) | set(new):
            if field not in ('sourceHashes', 'replayRequires') and old.get(field) != new.get(field):
                raise ValueError('Replay repair changed source/object/producer contracts')
        if any(new['sourceHashes'].get(path) != value for path, value in old.get('sourceHashes', {}).items()):
            raise ValueError('Replay repair changed an existing frozen source identity')
    return result, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--pins', required=True)
    parser.add_argument('--dry-run', action='store_true')
    options = parser.parse_args()
    path = ROOT / ('recovery.json' if options.dry_run else
        'work/integration/cohort' + str(options.cohort) + '-recovery-transaction.json')
    before = sha256(path)
    result, changes = amend(read_json(path), read_json(ROOT / options.pins))
    if not options.dry_run:
        write_json(path, result)
    receipt = dict(passed=True, createdUtc=now(), sourceCredit=0, dryRun=options.dry_run,
        registry=path.relative_to(ROOT).as_posix(), beforeSha256=before, afterSha256=sha256(path),
        consumers=changes, originalSourcesObjectsAndProducerArgvPreserved=True,
        startupOrderedBeforeAllConsumers=True, inputPins=options.pins, inputPinsSha256=sha256(ROOT / options.pins),
        fullCleanReplayProven=False)
    name = 'evidence/verification/' + ('parallel-wave20261102/utility-replay-inputs-dry-run.json' if options.dry_run else
        'cohort' + str(options.cohort) + '-utility-replay-inputs-20261101.json')
    write_json(ROOT / name, receipt)
    print(dict(passed=True, consumers=len(changes), dryRun=options.dry_run, sourceCredit=0))


if __name__ == '__main__':
    main()
