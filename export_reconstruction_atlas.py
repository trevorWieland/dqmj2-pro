import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from parallel_status import finalized


ROOT = Path(__file__).resolve().parent
LABELS = ['unresolved', 'accepted-c-cpp-and-pools', 'justified-assembly-and-pools',
          'accepted-initialized-data', 'accepted-padding', 'regenerated-linkage']


def number(value):
    return int(value, 0) if isinstance(value, str) else int(value)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(revision):
    commit = subprocess.run(['git', 'rev-parse', revision + '^{commit}'], cwd=ROOT,
        capture_output=True, check=True, text=True).stdout.strip()
    pins = {}

    def read(name, lines=False, text=False):
        data = subprocess.run(['git', 'show', commit + ':' + name], cwd=ROOT,
            capture_output=True, check=True).stdout
        pins[name] = sha(data)
        if text:
            return data.decode('utf-8')
        return [json.loads(row) for row in data.splitlines() if row] if lines else json.loads(data)
    return commit, pins, read


def place(module, field, address, size, value):
    start = number(address) - module['base']
    end = start + size
    if start < 0 or end > module['bytes'] or size < 0:
        raise ValueError('Atlas range escaped initialized module: ' + module['name'])
    if field == 'partial':
        module[field][start:end] = bytes(max(old, value) for old in module[field][start:end])
    else:
        module[field][start:end] = bytes([value]) * size


def runs(values):
    result = []
    start = 0
    for end in range(1, len(values) + 1):
        if end == len(values) or values[end] != values[start]:
            result.append([start, end - start, values[start]])
            start = end
    return result


def accepted_manifest(read):
    match = re.search(r'^Latest accepted source cohort (\d+):', read('README.md', text=True), re.M)
    if not match:
        raise ValueError('Snapshot does not declare an accepted source cohort')
    cohort = int(match[1])
    receipt = read('evidence/verification/cohort-2026-10-29-' + str(cohort) + '.json')
    closure = read('evidence/verification/cohort' + str(cohort) + '-expanded-source-closure-20261101.json')
    if not finalized(receipt, closure):
        raise ValueError('Atlas requires finalized acceptance and committed source/oracle closure')
    manifest = read('manifest.json')
    if manifest['functionMatched'] != receipt['sourceMatchedFunctions'] or manifest['sourceLinkedBytes'] != receipt['sourceLinkedBytes']:
        raise ValueError('Snapshot manifest differs from its accepted cohort')
    return cohort, manifest


def build(revision, pending, bins):
    commit, pins, read = snapshot(revision)
    cohort, manifest = accepted_manifest(read)
    functions = read('ledger/functions.jsonl', True)
    data = read('ledger/data.json')['records']
    linkage = read('ledger/linkage.json')
    drafts = read('ledger/drafts.jsonl', True)
    behavior = read('ledger/behavior-drafts-20261101.json')
    scripts = read('ledger/interpreted-programs.jsonl', True)
    modules = {}
    for row in manifest['modules']:
        modules[row['name']] = dict(name=row['name'], processor=row['processor'], program=row.get('program') or '',
            base=number(row['base']), bytes=row['bytes'], acceptedBytes=row['sourceMatchedBytes'],
            acceptedFunctions=row['sourceMatchedFunctions'], unresolvedBytes=row['unresolvedModuleBytes'],
            sourceComplete=row['sourceReconstructionComplete'], expectedBssBytes=row['expectedBssBytes'],
            acceptedBssBytes=row['sourceMatchedBssBytes'], expectedSourcePaddingBytes=row['sourceMatchedPaddingBytes'],
            status=bytearray(row['bytes']), partial=bytearray(row['bytes']), pending=bytearray(row['bytes']), units=[], draftEvidence=[])
    for row in functions:
        if not row['states']['functionMatched']:
            continue
        module = modules[row['module']]
        language = row.get('sourceLanguage') or ''
        is_assembly = language in ('assembly', 'metrowerks-assembler-function') or str(row['sourceUnit']).endswith('.s')
        place(module, 'status', row['address'], row['bytes'], 2 if is_assembly else 1)
        for region in row.get('hardwareAssemblyRanges', []) + row.get('justifiedAssemblyRanges', []):
            place(module, 'status', region.get('address', region.get('start')), region.get('bytes', region.get('size')), 2)
        module['units'].append(dict(address=row['address'], bytes=row['bytes'], mode=row['mode'],
            source=row['sourceUnit'], evidence=row['evidence'], moduleLinked=row['states']['moduleLinked']))
    for row in data:
        if row['storedBytes'] and row['states']['dataMatched']:
            place(modules[row['module']], 'status', row['address'], row['storedBytes'], 3)
    for row in manifest['modules']:
        fill = (row.get('linkOutput') or {}).get('sourceAlignmentFill')
        if fill:
            place(modules[row['name']], 'status', fill['start'], fill['bytes'], 4)
    for row in linkage['regions']:
        if row.get('linkerRegenerated'):
            module = modules[row['module']]
            start = number(row['address']) - module['base']
            if any(module['status'][start:start + row['bytes']]):
                raise ValueError('Linker region overlaps accepted source')
            place(module, 'status', row['address'], row['bytes'], 5)
    for row in drafts:
        if not row['nativeFunctionHasAcceptedImplementation'] and row['states']['drafted']:
            implementations = row['implementations']
            confidence = 3 if any(i['sourceCurrent'] and i['compiledUnderRecordedScope'] for i in implementations) else 2 if any(i['sourceCurrent'] for i in implementations) else 1
            module = modules[row['module']]
            place(module, 'partial', row['address'], row['nativeBytes'], confidence)
            module['draftEvidence'].append(dict(id=row['id'], address=row['address'], bytes=row['nativeBytes'],
                confidence=confidence, evidenceScope='frozen-generated-draft-ledger', sourceCredit=0,
                implementations=[{key: i.get(key) for key in ('source', 'sourceSha256', 'report', 'reportSha256',
                    'sourceCurrent', 'compiledUnderRecordedScope', 'nativeSemanticsVerified', 'knownSemanticMismatch')} for i in implementations]))
    for row in behavior['functions']:
        module = modules[row['module']]
        place(module, 'partial', row['address'], row['initializedBytes'], 4)
        module['draftEvidence'].append(dict(address=row['address'], bytes=row['initializedBytes'], confidence=4,
            evidenceScope='selective-bounded-behavior-draft-ledger', source=row['source'], sourceSha256=row['sourceSha256'],
            evidence=row['evidence'], sourceCredit=0))
    packets, identities = [], set()
    for path in pending:
        payload = path.read_bytes()
        specification = json.loads(payload)
        count = total = 0
        for row in specification['expectedAdditions']:
            key = row['module'], row['mode'], number(row['address'])
            if key in identities:
                raise ValueError('Duplicate prepared identity')
            identities.add(key)
            place(modules[row['module']], 'pending', row['address'], row['bytes'], 1)
            count += 1
            total += row['bytes']
        packets.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha(payload), cohort=specification['cohort'],
            functions=count, proposedBytes=total, inputScope='unaccepted-worktree-specification', sourceCredit=0))
    totals = Counter()
    output = []
    for module in modules.values():
        status = module['status']
        counts = Counter(status)
        accepted = sum(counts[k] for k in (1, 2, 3, 4))
        missing = module['acceptedBytes'] - accepted
        if missing < 0:
            raise ValueError('Map overcredits source: ' + module['name'])
        if counts[0] != module['unresolvedBytes'] + missing:
            raise ValueError('Map does not reconcile remaining bytes: ' + module['name'])
        module['unlocatedAcceptedBytes'] = missing
        module['categories'] = {LABELS[k]: counts[k] for k in range(len(LABELS))}
        confidence_counts = Counter(module['partial'][i] for i in range(len(status)) if status[i] == 0)
        module['draftConfidenceBytes'] = {str(k): confidence_counts[k] for k in (1, 2, 3, 4)}
        module['partialUnacceptedBytes'] = sum(module['partial'][i] >= 2 and status[i] == 0 for i in range(len(status)))
        module['pendingUnacceptedBytes'] = sum(bool(module['pending'][i]) and status[i] == 0 for i in range(len(status)))
        module['acceptedPreparedOverlapBytes'] = sum(bool(module['pending'][i]) and status[i] in (1, 2, 3, 4) for i in range(len(status)))
        combined = bytearray((6 if module['pending'][i] else 7 if module['partial'][i] >= 2 else 0) if status[i] == 0 else status[i] for i in range(len(status)))
        module['regions'] = runs(combined)
        module['bins'] = []
        module['draftConfidenceBins'] = []
        for index in range(min(bins, module['bytes'])):
            start, end = index * module['bytes'] // min(bins, module['bytes']), (index + 1) * module['bytes'] // min(bins, module['bytes'])
            values = Counter(combined[start:end])
            module['bins'].append([start, end - start, *[values[k] for k in range(8)]])
            classes = Counter(module['partial'][i] for i in range(start, end) if status[i] == 0)
            module['draftConfidenceBins'].append([classes[k] for k in (1, 2, 3, 4)])
        del module['status'], module['partial'], module['pending']
        for key in ['bytes', 'acceptedBytes', 'unresolvedBytes', 'unlocatedAcceptedBytes', 'partialUnacceptedBytes', 'pendingUnacceptedBytes']:
            totals[key] += module[key]
        output.append(module)
    if totals['acceptedBytes'] != manifest['sourceMatchedBytes'] or totals['unresolvedBytes'] != manifest['unresolvedModuleBytes']:
        raise ValueError('Atlas totals differ from committed manifest')
    if totals['bytes'] != totals['acceptedBytes'] + totals['unresolvedBytes'] + manifest['linkerRegeneratedBytes']:
        raise ValueError('Atlas source, linkage and remaining byte partition differs')
    return dict(schemaVersion=1, sourceCommit=commit, acceptedCohort=cohort, sourceSnapshotPins=pins,
        acceptedFunctions=manifest['functionMatched'], metrics=dict(totals), initializedModuleSourcePercentage=totals['acceptedBytes'] / totals['bytes'] * 100,
        regeneratedLinkerBytes=manifest['linkerRegeneratedBytes'], categories=LABELS + ['prepared-unaccepted', 'partial-unaccepted'],
        draftConfidenceClasses={'1': 'historical-or-stale-draft-record; not colored as current partial work',
            '2': 'source-current claim in frozen draft ledger; uncompiled', '3': 'compiled under recorded scope; native semantics unverified',
            '4': 'selective independently bounded behavior evidence; not a full byte match'},
        modules=output, pendingPackets=packets, evidenceDimensions=dict(nativeInventoryComplete=manifest['executableInventoryComplete'],
            sourceOnlyRomProven=manifest['wholeRomMatchedFromSource'], scaffoldAssistedExactRom=manifest['exactContainerMatchWithScaffolding'],
            boundedBehaviorLedgerSelective=True), interpretedSummary=manifest['interpretedCoverage'],
        interpretedImages=[dict(codeSha256=r['codeSha256'], codeContainerBytes=r['codeContainerBytes'], sourceBytes=r['ordinarySourceByteCredit'],
            sourceUnits=r['ordinarySourceUnitCredit'], complete=bool(r['completeImageCredit']), opaqueSysNodes=r['opaqueSysNodes']) for r in scripts],
        limitations=['Initialized module bytes include data and function literal pools; this is not overall game completion.',
            'Prepared and partial regions receive zero accepted source credit. Partial draft ledger is incomplete.',
            'Metadata reflects one committed snapshot; source/object recompilation and new clean replay are separate proofs.',
            'Regenerated linker bytes and BSS are separate from the accepted initialized-source numerator.'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--pending', type=Path, action='append', default=[])
    parser.add_argument('--bins', type=int, default=128)
    parser.add_argument('--output', type=Path, default=ROOT / 'work/parallel-wave20261102/atlas')
    options = parser.parse_args()
    if not 16 <= options.bins <= 512:
        raise ValueError('Use16..512 bins per module')
    output = options.output.resolve()
    if output == ROOT or not output.is_relative_to(ROOT / 'work'):
        raise ValueError('Atlas output must be a dedicated repository work directory')
    result = build(options.revision, [(ROOT / path).resolve() for path in options.pending], options.bins)
    output.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, separators=(',', ':'))
    (output / 'atlas.json').write_text(payload + '\n', encoding='utf-8')
    compact = dict(result)
    compact['modules'] = [{k: v for k, v in row.items() if k not in ('units', 'regions', 'draftEvidence')} for row in result['modules']]
    compact.pop('interpretedImages')
    (output / 'atlas-summary.json').write_text(json.dumps(compact, separators=(',', ':')) + '\n', encoding='utf-8')
    template = (ROOT / 'visualizations/reconstruction-atlas.html').read_text(encoding='utf-8')
    fragment = template.replace('__ATLAS_JSON__', json.dumps(compact, separators=(',', ':')).replace('</', '<\\/'))
    if len(fragment.encode('utf-8')) >= 1000000:
        raise ValueError('Atlas fragment exceeds its inline size budget')
    (output / 'reconstruction-atlas.html').write_text(fragment, encoding='utf-8')
    print(json.dumps(dict(sourceCommit=result['sourceCommit'], acceptedFunctions=result['acceptedFunctions'], metrics=result['metrics'],
        percentage=result['initializedModuleSourcePercentage'], output=str(output), jsonBytes=len(payload))))


if __name__ == '__main__':
    main()
