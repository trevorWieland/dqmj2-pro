import gzip
import hashlib
import json
import sys
import match_runtime
import unicorn
from project import ROOT, configuration, read_json, sha256, write_json
from link_runtime_unit import measured_module
import match_ov001_action822_20261102 as B
import ov001_action822_machine_20261102 as M
import ov001_action830_machine_20261102 as A
import ov001_action830_model_20261102 as G
from ov001_action830_profiles_20261102 import profiles

SOURCE = ROOT / 'src/overlays/ov001_20261102_action830'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('830 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov001-action830-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('830 input differs', row['path']))
    selected = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], A.ENTRY) < min(row['address'] + row['bytes'], A.ENTRY + 988) for row in selected):
        raise ValueError('830 selected overlap')
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov001')
    B.WORK = ROOT / 'work/ol830-proof'
    match, body = B.build(SOURCE / 'dispatch.c', 'source')
    template = (SOURCE / 'dispatch.c').read_text()
    variants = [('wrong-return', '    return 0U;', '    return 1U;', 0x02650000), ('wrong-token-signedness', '(u32) (s8) M2C_FIELD', '(u32) (u8) M2C_FIELD', 0x02652000)]
    controls = []
    images = {}
    for name, before, after, origin in variants:
        if template.count(before) != 1:
            raise ValueError(('830 wrong-source edit ambiguous', name))
        directory = ROOT / 'nonmatching/overlay-lane/20261102-action830-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        text = template.replace(before, after)
        if source.exists() and source.read_text() != text:
            raise ValueError(('830 frozen control differs', name))
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, wrong = B.build(source, name, origin)
        images[origin] = wrong
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, suppliedCalls=0, independentModelPairs=0)
    traces = []
    cases = []
    pcs = set()
    counts = {}
    outcomes = set()
    for profile in profiles():
        results = []
        failures = []
        for kind, entry in [('native', A.ENTRY), ('source', A.ENTRY)] + [(row['name'], row['origin']) for row in controls]:
            vm = A.Machine(main, overlay, images, profile)
            if kind == 'source':
                vm.u.mem_write(A.ENTRY, body)
            result = vm.run(entry)
            result['kind'] = kind
            results.append(result)
            failures.append(G.model(vm, result))
        original, candidate = results[:2]
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov001-action830-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(B.compact, results))))
            raise ValueError(('830 original/source model failed', profile['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'calls', 'rawCalls', 'nativeEntries', 'nativeCompletions', 'writes', 'context', 'actors', 'memory', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov001-action830-source-rejected-20261102.json', dict(profile=profile, differences=differences, results=list(map(B.compact, results))))
            raise ValueError(('830 native/source difference', profile['ordinal'], differences))
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        count = original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['actualNativeReturnInstructions'] += count
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        pcs.update(original['ownPcs'])
        outcomes.add(original['context'][0x1B])
        for result in results[:2]:
            for row in result['nativeCompletions']:
                counts[row['address']] = counts.get(row['address'], 0) + 1
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(B.compact, results)), modelFailures=failures, originalSourceDifferences=differences)
        cases.append(dict(ordinal=profile['ordinal'], actualTopReturns=2, actualNativeDependencyReturns=count, suppliedCalls=len(original['calls']) + len(candidate['calls']), traceSha256=hashlib.sha256(encoded(trace)).hexdigest()))
        traces.append(trace)
    missing = sorted(set(range(A.ENTRY, A.ENTRY + 976, 4)) - pcs)
    if missing:
        write_json(ROOT / 'evidence/attempts/ov001-action830-coverage-rejected-20261102.json', dict(missingPcs=list(map(hex, missing)), observed=len(pcs)))
        raise ValueError(('830 own instruction coverage incomplete', len(missing)))
    if any(not row['rejected'] for row in controls):
        raise ValueError('830 returning negative rejection missing')
    raw = encoded(traces)
    artifact = ROOT / 'evidence/generated/ov001-action830-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=988, sourceCreditPendingIntegrator=988, allPassed=True, totals=totals, nativeDependencyCounts=counts, allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allRawCallWordsAndOrderedWritesEqual=True, allOwnCodeObserved=dict(codeBytes=976, literalBytes=12, unclassifiedBytes=0), observedRawDispatchBytes=sorted(outcomes), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['988-byte ordinary C source with genuine canonical link; integrator module/ROM admission pending.', 'Actual MoveTbl getters/flag reader and originalF358C opponent scan with original actor lookup/eligibility execute. UI/resource/action/notification services remain supplied, with legal caller-saved/CPSR clobbers and no RAM effects.', 'Own phase9, signed resource/effect0x0C, actor+0x80/current+0x84, raw marker1FF, raw opponent267 and table fields are synthetic inputs. No ordinary scene reachability, record33 initialization, ability names or future RNG claim.', 'Signed byte token forwarding to main0205D6F4 is measured; wrong unsigned-byte C controls retain legitimate unaffected positives separately.', 'Four field left shifts explicitly cast u16 to u32 BEFORE shifting; no promoted signed-left-overflow assumption is needed at these sites. Old M2C/switch and six-byte condition-direction failures remain retained separately.', 'Caller-specific service word views do not establish complete original callee formal types. No malformed-pointer/hardware/device or host execution claim.'])
    write_json(ROOT / 'evidence/matches/ov001-20261102-action830.json', report)
    print(dict(**totals, matchedBytes=988, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls], observedRawDispatchBytes=sorted(outcomes)), flush=True)


if __name__ == '__main__':
    execute()
