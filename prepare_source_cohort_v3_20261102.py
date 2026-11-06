import argparse
import subprocess
import sys
from project import ROOT, configuration, read_json, write_json, sha256, now
import recovery_registry
from recovery_registry import register, verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources


def classify_additions(after,added):
    ordinary=[];assembly=[]
    for key in added:
        row=after[key];justification=row.get('assemblyJustification');language=row.get('sourceLanguage')
        if language is None and not justification:
            flags=row.get('compilerFlags')or[]
            modes=[b for a,b in zip(flags,flags[1:])if a=='-lang']
            assert (ROOT/row['source']).suffix=='.c'and modes and modes[-1]in('c','c99')
            language='C'
        if justification:
            assert language=='assembly'
            assert justification['classification']=='verified-original-SDK-assembly'
            assert justification['originalExplicitAsmDeclaration']is True
            assert justification['sourceStatementsDerivedFromPublishedSdkNotDisassembly']is True
            assert justification['ordinaryLogicAssemblyExceptions']==0
            assert sha256(ROOT/justification['publishedSource'])==justification['publishedSourceSha256']
            assembly.append(key)
        else:
            assert language in('C','C++')
            import re
            text=(ROOT/row['source']).read_text(encoding='utf-8')
            without_strings=re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
            assert not re.search(r'\b(?:asm|__asm__|__asm)\b',without_strings)
            ordinary.append(key)
    return dict(newOrdinaryCFunctions=len(ordinary),newOrdinaryCBytes=sum(after[k]['size']for k in ordinary),
        newVerifiedOriginalAssemblyFunctions=len(assembly),newVerifiedOriginalAssemblyBytes=sum(after[k]['size']for k in assembly))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    options = parser.parse_args()
    spec_path = ROOT / options.specification
    spec = read_json(spec_path)
    cohort, previous = spec['cohort'], spec['previousAcceptedCohort']
    assert cohort == previous + 1 and not spec.get('migrations')
    current = ROOT / 'recovery.json'
    policy = ROOT / 'source-preferences.json'
    original_registry, original_policy = current.read_bytes(), policy.read_bytes()
    old = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{previous}.json')
    assert not old['linksPending'] and sha256(current) == old['sourceRegistrySha256']
    assert sha256(policy) == old['sourcePreferenceSha256']
    transaction = ROOT / f'work/integration/cohort{cohort}-recovery-transaction.json'
    transaction.parent.mkdir(parents=True, exist_ok=True)
    transaction.write_bytes(original_registry)
    recovery_registry.REGISTRY = transaction
    verify_sources()
    before, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == old['sourceMatchedFunctions']
    fields = ['source', 'sourceSha256', 'object', 'objectSha256', 'size', 'targetSha256', 'report']
    write_json(ROOT / f'evidence/verification/cohort{cohort}-before-adoption-20261101.json', dict(
        registrySha256=sha256(transaction), preferencesSha256=sha256(policy),
        selected=[dict(key=list(key), **{field: row.get(field) for field in fields}) for key, row in sorted(before.items())]))
    reports = []
    for packet in spec['packets']:
        report, producer = packet['report'], packet['producer']
        if packet.get('directProducer'):
            register(report, producer)
        else:
            seal_sources(report, producer)
            register(report, ['seal_recovery_sources_20261031.py', report, *producer])
        reports.append(report)
    for command in spec.get('postSealCommands', []):
        subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT, check=True)
    registry = read_json(transaction)
    oracles = {item['report']: item for item in registry['oracles']}
    for item in spec.get('oracles', []):
        assert (ROOT / item['report']).is_file()
        oracles[item['report']] = item
    registry['oracles'] = list(oracles.values())
    write_json(transaction, registry)
    verify_sources()
    after, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    for key, row in before.items():
        assert all(after[key][field] == row[field] for field in ['source', 'sourceSha256', 'object', 'objectSha256'])
    added = set(after) - set(before)
    expected = {(item['module'], item['mode'], int(item['address'], 0)): item['bytes'] for item in spec['expectedAdditions']}
    assert added == set(expected)
    assert all(after[key]['size'] == expected[key] for key in added)
    delta = sum(after[key]['size'] for key in added)
    accounting=classify_additions(after,added)
    assert accounting['newOrdinaryCBytes']+accounting['newVerifiedOriginalAssemblyBytes']==delta
    plan = {key: value for key, value in old.items() if key.startswith(('expectedInterpreted', 'expectedEmpty', 'expectedNonempty', 'expectedCopy'))}
    plan.update(schemaVersion=1, createdUtc=now(), reports=reports, interpretedReports=[],
        specification=options.specification, specificationSha256=sha256(spec_path), sourceRegistrySha256=sha256(transaction),
        sourcePreferenceSha256=sha256(policy), interpretedRegistrySha256=sha256(ROOT / 'interpreted-recovery.json'),
        linksPending=True, newSourceFunctions=len(added), newSourceBytes=delta,
        duplicateMigrationFunctions=0, expectedSourceMatchedFunctions=len(after),
        expectedSourceLinkedBytes=old['sourceLinkedBytes'] + delta,
        preferredSourceInputsRequired=len(read_json(policy)['preferences']), sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False, sourceOnlyRomProven=False, fullWindowsGameFromSourceProven=False,
        androidDeviceExecutionCount=0, previousAcceptedCohort=previous, previousAcceptedFunctions=len(before),
        previousAcceptedBytes=old['sourceLinkedBytes'], allEarlierSourcesAndObjectsPreserved=True,
        fullCleanReplayOfThisCohortProven=False, transactionPreparedOnly=True)
    plan.update(accounting)
    write_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json', plan)
    assert current.read_bytes() == original_registry and policy.read_bytes() == original_policy
    print(dict(cohort=cohort, newFunctions=len(added), newBytes=delta, transactionPreparedOnly=True))


if __name__ == '__main__':
    main()
