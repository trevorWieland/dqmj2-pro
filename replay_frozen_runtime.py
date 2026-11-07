import argparse
import copy
from pathlib import Path
import runpy
import sys
from project import ROOT, read_json, write_json, sha256
from frozen_runtime_input import FrozenRuntimeInput


def local(name, existing=True):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or existing and not path.is_file():
        raise ValueError('Frozen replay path escaped or is unavailable')
    return path


def mapping_context(document):
    fields = ('fromPath', 'expectedSha256', 'snapshotPath', 'snapshotSha256')
    context = FrozenRuntimeInput(ROOT, **{key: document[key] for key in fields})
    if sha256(context.snapshot) != document['expectedSha256']:
        raise ValueError('Frozen runtime snapshot pin differs')
    return context


def replay(mapping_name):
    mapping_path = local(mapping_name)
    mapping = read_json(mapping_path)
    if mapping.get('schemaVersion') != 1:
        raise ValueError('Unknown frozen replay mapping schema')
    producer = mapping['producer']
    if not producer or not isinstance(producer, list) or not all(isinstance(x, str) for x in producer):
        raise ValueError('Frozen replay producer must be an explicit argument list')
    executable = local(producer[0])
    if executable.suffix != '.py':
        raise ValueError('Frozen replay requires a repository Python producer')
    raw = local(mapping['rawWorkerReport'])
    target = local(mapping['workerReport'], False)
    receipt_path = local(mapping['receipt'], False)
    context = mapping_context(mapping)
    protected = {raw, mapping_path, executable, context.logical, context.snapshot}
    if not all(path.is_relative_to(ROOT / 'work') for path in (target, receipt_path)):
        raise ValueError('Frozen replay additive outputs must remain under work')
    if target in protected or receipt_path in protected or target == receipt_path:
        raise ValueError('Frozen replay requires separate additive outputs')
    previous_argv = sys.argv
    try:
        with context:
            sys.argv = [str(executable), *producer[1:]]
            runpy.run_path(str(executable), run_name='__main__')
    finally:
        sys.argv = previous_argv
    receipt = context.receipt()
    if not receipt['liveLedgerUnchanged'] or not receipt['readCalls']:
        raise ValueError('Frozen replay did not consume its declared immutable input')
    receipt.update(mapping=dict(path=mapping_path.relative_to(ROOT).as_posix(), sha256=sha256(mapping_path)),
        producer=producer, rawReportSha256=sha256(raw), sourceCredit=0)
    write_json(receipt_path, receipt)
    report = copy.deepcopy(read_json(raw))
    report['frozenRuntimeInputReplay'] = dict(receipt=receipt_path.relative_to(ROOT).as_posix(),
        receiptSha256=sha256(receipt_path), mapping=receipt['mapping'],
        fromPath=receipt['fromPath'], snapshotPath=receipt['snapshotPath'],
        snapshotSha256=receipt['snapshotSha256'], liveLedgerUnchanged=True)
    write_json(target, report)
    return dict(report=target.relative_to(ROOT).as_posix(), liveLedgerUnchanged=True, sourceCredit=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mapping')
    print(replay(parser.parse_args().mapping))
