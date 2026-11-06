import gzip
import json
from pathlib import Path
import match_runtime as c
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov001_action436_machine_20261101 as M
import ov001_action436_models_20261101 as P
SOURCE = ROOT / 'nonmatching/overlay-lane/20261101-action436'
WORK = ROOT / 'work/ol436-proof'
REPORT = ROOT / 'evidence/attempts/ov001-action436-functional-near-20261101.json'

def link(source, directory):
    c.WORK = directory / 'compile'
    rows, _ = c.compare(source, 'ov001', '2', 'off', True)
    row = rows[0]
    if row.get('compileFailed'):
        raise ValueError(('436 source compilation failed', row))
    try:
        proof = validate(row, qualified_bindings(row), directory / 'linked')
        exact = True
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        proof = error.args[0]
        exact = False
    return (row, proof, exact, (directory / 'linked/caller.bin').read_bytes())

def normalized(data, extent):
    value = bytearray(data)
    start = M.ENTRY - M.BASE
    value[start:start + extent] = b'\x00' * extent
    cut = M.STACK - 65536 - M.BASE
    end = M.STACK + 4096 - M.BASE
    return c.sha(bytes(value[:cut]) + bytes(value[end:]))

def run():
    accepted = ROOT / 'evidence/verification/accepted-cohort97-identities-v2-20261101.json'
    rows = json.loads(accepted.read_text())['functions']
    if any((r['processor'] == 'arm9' and (not r['program']) and (r['module'] == 'ov001') and (max(r['address'], M.ENTRY) < min(r['address'] + r['bytes'], M.ENTRY + M.SIZE)) for r in rows)):
        raise ValueError('436 subject now overlaps selected source')
    original = M.inputs()
    compilation, proof, exact, body = link(SOURCE / 'source.c', WORK / 'preferred')
    if exact:
        raise ValueError('436 near-proof scope changed to exact; require a separate acceptance packet')
    traces = []
    summaries = []
    original_coverage = set()
    candidate_coverage = set()
    counts = dict(actualTopReturns=0, actualNativeDependencyReturns=0, rngReturnsWithinDependencyTotal=0, providedCalls=0)
    negative_profiles = []
    for profile in P.profiles():
        native = M.Machine(original, profile).run()
        native_model = P.model(native)
        candidate = M.Machine(original, profile, body).run()
        candidate_model = P.model(candidate)
        extent = max(M.SIZE, len(body))
        native_hash = normalized(native['after'], extent)
        candidate_hash = normalized(candidate['after'], extent)
        if native_model != candidate_model or native_hash != candidate_hash or native['events'] != candidate['events'] or (native['nativeReturns'] != candidate['nativeReturns']):
            raise ValueError(('436 original/linked source behavior differs', profile['name']))
        original_coverage.update(native['ownObserved'])
        candidate_coverage.update(candidate['ownObserved'])
        counts['actualTopReturns'] += 2
        counts['actualNativeDependencyReturns'] += len(native['nativeReturns']) + len(candidate['nativeReturns'])
        counts['rngReturnsWithinDependencyTotal'] += sum((r['entry'] == 33804948 for r in native['nativeReturns'] + candidate['nativeReturns']))
        counts['providedCalls'] += native['providedCalls'] + candidate['providedCalls']
        trace = dict(profile=profile, nativeEvents=native['events'], candidateEvents=candidate['events'], nativeReturns=native['nativeReturns'], candidateReturns=candidate['nativeReturns'], nativeObserved=native['ownObserved'], candidateObserved=candidate['ownObserved'], model=native_model, normalizedFinalNonstackSha256=native_hash)
        encoded = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        traces.append(trace)
        summaries.append(dict(name=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=len(native['nativeReturns']) + len(candidate['nativeReturns']), rngReturnsWithinDependencyTotal=sum((r['entry'] == 33804948 for r in native['nativeReturns'] + candidate['nativeReturns'])), providedCalls=native['providedCalls'] + candidate['providedCalls'], nativeInstructions=native['instructions'], candidateInstructions=candidate['instructions'], rawState13=native_model['rawState13'], traceSha256=c.sha(encoded)))
        if native_model['rawState13'] == 2:
            negative_profiles.append(profile)
    if len(original_coverage) * 4 != 1220:
        raise ValueError(('436 native own-code coverage incomplete', len(original_coverage) * 4))
    controls = []
    source = (SOURCE / 'source.c').read_text()
    header = (SOURCE / 'context.h').read_bytes()
    wrong_state = source.replace('s8 *, 0x13) = 2;', 's8 *, 0x13) = 4;')
    if wrong_state == source:
        raise ValueError('436 control state rewrite absent')
    wrong_cost = '\n'.join((line.replace('(s32) required', '0') if 'native_fn_ov001_021db834(' in line else line for line in source.splitlines())) + '\n'
    if wrong_cost == source:
        raise ValueError('436 control cost rewrite absent')
    for name, text in [('wrong-state', wrong_state), ('wrong-native-debit-input', wrong_cost)]:
        directory = WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'source.c').write_text(text)
        (directory / 'context.h').write_bytes(header)
        row, linked, control_exact, wrong_body = link(directory / 'source.c', directory / 'build')
        results = []
        selected_controls = negative_profiles if name == 'wrong-state' else [p for p in negative_profiles if p['mode'] != 1 and p['required'] != 0]
        for profile in selected_controls[:12]:
            result = M.Machine(original, profile, wrong_body).run()
            try:
                P.model(result)
            except ValueError as error:
                results.append(dict(profile=profile['name'], actualTopReturns=1, rejected=True, reason=str(error)))
            else:
                raise ValueError(('436 compiled negative control unexpectedly accepted', name, profile['name']))
        if len(results) != 12:
            raise ValueError('436 insufficient returning negative cases')
        controls.append(dict(name=name, sourceSha256=sha256(directory / 'source.c'), contextSha256=sha256(directory / 'context.h'), compilation=row, genuineLinkComparison=linked, exact=control_exact, actualTopReturns=len(results), results=results))
    trace_data = json.dumps(dict(schemaVersion=1, sourceCredit=0, records=traces), sort_keys=True, separators=(',', ':')).encode()
    archive = ROOT / 'evidence/generated/ov001-action436-functional-20261101.json.gz'
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(gzip.compress(trace_data, compresslevel=9, mtime=0))
    imports = ['ov001_action436_machine_20261101.py', 'ov001_action436_models_20261101.py']
    boundaries = []
    for address, r in original['ranges'].items():
        image = original['arm'] if r['module'] == 'main' else original['overlay']
        base = M.BASE if r['module'] == 'main' else M.OVERLAY_BASE
        boundaries.append(dict(address=hex(address), module=r['module'], mode=r['mode'], bytes=r['bytes'], nativeSpanSha256=c.sha(image[address - base:address - base + r['bytes']])))
    write_json(REPORT, dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], mainModuleSha256=original['main']['sha256'], nativeSpanSha256=c.sha(original['overlay'][M.ENTRY - M.OVERLAY_BASE:M.ENTRY - M.OVERLAY_BASE + M.SIZE]), address=hex(M.ENTRY), mode='arm', nativeBytes=M.SIZE, sourceCredit=0, exactFunctions=0, exactBytes=0, classification='genuine-linked ordinary C with bounded functional evidence; not byte-exact', compilation=compilation, genuineLinkComparison=proof, linkedElfSha256=sha256(WORK / 'preferred/linked/linked.elf'), linkedCallerSha256=c.sha(body), linkerSha256=sha256(ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'), sourceSha256=sha256(SOURCE / 'source.c'), contextSha256=sha256(SOURCE / 'context.h'), generatorSha256=sha256(__file__), localImports=[dict(path=p, sha256=sha256(ROOT / p)) for p in imports], acceptedSnapshot=dict(path=accepted.relative_to(ROOT).as_posix(), sha256=sha256(accepted)), profiles=len(summaries), pairs=len(summaries), **counts, originalCallerObservedBytes=len(original_coverage) * 4, originalCallerCodeBytes=1220, originalCallerLiteralBytes=12, candidateCallerObservedBytes=len(candidate_coverage) * 4, maxInstructions=max((max(r['nativeInstructions'], r['candidateInstructions']) for r in summaries)), instructionBound=32768, freshMachinePerExecution=True, cpu='ARM946', allNonstackEffectsIndependentlyChecked=True, relevantCallContractsIndependentlyChecked=True, compiledReturningControls=controls, nativeDependencyBoundaries=boundaries, traceArchive=dict(path=archive.relative_to(ROOT).as_posix(), sha256=sha256(archive), decodedSha256=c.sha(trace_data), bytes=archive.stat().st_size), caseSummaries=summaries, reproductionCommand='python qualify_ov001_action436_20261101.py', limits=['1232-byte linked draft has1213 matching bytes;19 register/scheduling bytes remain failures andsource credit is0', 'Original RNG/division,actor lookup/validity,raw class check,available-value getters/resource updates andmemory clear execute; their returns are included in the dependency total', 'Initialization,move/resource queries,maximum-base calculation,slot policy,notification andtwo final actor-field providers are supplied contracts,not recovered scene reachability', 'Caller state,expanded records,table fields,loaded actor pools andRNG seeds are deterministic synthetic inputs; no future RNG scene orsave/persistence claim', 'Raw context/actor field names andstate values are retained; no game-mechanic meaning is inferred from matching behavior', 'Only relevant caller-prepared words are compared; unspecified caller-saved scratch registers are poisoned andnot asserted as semantic ABI', 'Native physical return words are compared as observations; unused return values do not acquire semantic meaning', 'No all-invalid random-target case is supported; each supplied eligibility mask is nonzero andthe independent deterministic retry model has64 iterations', 'Normal andcontrol images are genuinely compiled andMW-linked; entire substituted image extents take precedence over native entry watches']))
    print(json.dumps(dict(pairs=len(summaries), **counts, originalCallerObservedBytes=len(original_coverage) * 4, compiledReturningControls=sum((x['actualTopReturns'] for x in controls)), sourceCredit=0)))
if __name__ == '__main__':
    run()
