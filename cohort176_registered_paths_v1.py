import copy
from contextlib import contextmanager
import json
from pathlib import Path
from cohort176_epoch_v1 import ACCOUNTING, NEW, PREFS, accounting, canonical, require, sha


def prepare(epoch, legacy, contract):
    epoch.ensure()
    legacy.validate_contract(contract)
    require(sha(epoch.read_current(legacy.CONTRACT)) == epoch.contract['registeredPathContractSha256'], 'Historical path contract changed')
    require(json.loads(epoch.read_current(legacy.CONTRACT)) == contract, 'Wrong historical path contract')
    names = [contract[k] for k in ('helper', 'test', 'originalVerifier', 'preferences', 'canonicalSource')]
    names += contract['evidenceViews'] + contract['proofInputs']
    documents = {}
    for record in names:
        raw = epoch.read_current(record['path'])
        require(raw == epoch.read_committed(record['path']) and sha(raw) == record['sha256'], 'Historical proof input differs')
        require('bytes' not in record or len(raw) == record['bytes'], 'Historical proof length differs')
        if record['path'] in {r['path'] for r in contract['evidenceViews']}:
            document = json.loads(raw)
            require(document['previous']['source'] == legacy.RAW and document['previous']['sourceSha256'] == legacy.SOURCE_SHA, 'Historical alias source differs')
            documents[record['path']] = document
    policy = json.loads(epoch.read_current('source-preferences.json'))
    for record in contract['evidenceViews']:
        require(policy['preferences'].count(record['preference']) == 1, 'Preference binding differs')
        document, row = documents[record['path']], record['preference']
        require(document['preferred'] == {k: row[k] for k in ('source', 'sourceSha256', 'report')}, 'Preferred source binding differs')
        require(document['identity'] == {k: row[k] for k in ('processor', 'module', 'mode', 'address', 'bytes', 'targetSha256')}, 'Evidence namespace differs')
        require(document['romSha256'] == policy['romSha256'] and document['originalSourceUnchanged'] and document['nativeBytesUnchanged'] and document['newFunctionCredit'] == document['newByteCredit'] == 0, 'Evidence credit or preservation differs')
    for record in contract['proofInputs']:
        origins = sorted(set(b['report'] for b in epoch.registry['batches'] if any(n.replace('\\', '/') == record['path'] and h == record['sha256'] for n, h in b['sourceHashes'].items())))
        require(origins == record['originReports'], 'Historical proof origin set differs')
    require(len(documents) == 7, 'Seven exact evidence views required')
    return dict(documents=documents, report=dict(ready=True, registrySha256=NEW, preferenceSha256=PREFS,
        sourceCredit=0, historicalProofInputs=11, canonicalRegistryAuthenticated=True))


@contextmanager
def installed(module, legacy, epoch, prepared, root):
    require(prepared['report']['ready'] and len(prepared['documents']) == 7, 'Path setup incomplete')
    root = Path(root).resolve()
    saved_main, saved_reader = module.main, module.read_json
    events, state = [], dict(calls=0, completed=False)
    proof = dict(setup=prepared['report'], events=events, expectedAccounting=copy.deepcopy(ACCOUNTING), passed=False, sourceCredit=0)
    def main(*args, **kwargs):
        epoch.ensure()
        state['calls'] += 1
        require(state['calls'] == 1 and not args and not kwargs, 'Strict V8 dispatch differs')
        prior = module.read_json
        def read(path):
            document = prior(path)
            try:
                name = Path(path).resolve().relative_to(root).as_posix()
            except ValueError:
                return document
            if name not in prepared['documents']:
                return document
            require(name not in {r['path'] for r in events}, 'Duplicate evidence view')
            view = legacy.project_evidence(document, prepared['documents'][name])
            events.append(dict(path=name, field='previous.source', before=legacy.RAW, after=legacy.CANON, sourceSha256=legacy.SOURCE_SHA))
            return view
        module.read_json = read
        try:
            result = saved_main()
        finally:
            unchanged = module.read_json is read
            module.read_json = prior
            require(unchanged, 'V8 reader was replaced unexpectedly')
        require({r['path'] for r in events} == set(prepared['documents']) and len(events) == 7, 'Seven exact views not observed')
        state['completed'] = True
        return result
    module.main = main
    success = False
    try:
        yield proof
        success = True
    finally:
        unchanged = module.main is main and module.read_json is saved_reader
        module.main, module.read_json = saved_main, saved_reader
        require(unchanged, 'V8 bindings were replaced unexpectedly')
        epoch.ensure()
        if success:
            require(state['calls'] == 1 and state['completed'], 'Strict V8 did not finish once')
            proof['passed'] = True


def validate_accounting(document, unused_contract=None):
    return accounting(document)
