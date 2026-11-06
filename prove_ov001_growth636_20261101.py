import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov001_growth632_machine_20261101 as M
import ov001_growth632_models_20261101 as P
SOURCE = ROOT / 'nonmatching/overlay-lane/20261101-growth634/void-wrapper/source.c'
WORK = ROOT / 'work/ol636-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_unit(source, name):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('636 complete ordinary C failed compilation')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'link'
    try:
        proof = validate(row, qualified_bindings(row), directory)
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        proof = error.args[0]
    return row, proof, (directory / 'caller.bin').read_bytes()


def compact(result):
    return {key: result[key] for key in ['actualTopReturnedWords', 'coreRegistersAndCpsr', 'nativeReturns', 'providedCalls', 'nonstackWrites', 'ownObserved', 'mainObserved', 'instructions']}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('636 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov001-growth636-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('636 frozen input differs', item['path']))
    accepted = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + M.SIZE) for row in accepted):
        raise ValueError('636 accepted snapshot overlap')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'candidate')
    profiles, traces, cases, seen = P.profiles(), [], [], set()
    dependencies, providers = 0, 0
    order_differences, raw_core_differences, raw_provider_differences = [], [], []
    for index, profile in enumerate(profiles):
        native, candidate = M.Machine(original, profile).run(), M.Machine(original, profile, body).run()
        nm, cm = P.model(native), P.model(candidate)
        if nm != cm:
            raise ValueError(('636 independent complete own-effect models differ', profile['name']))
        meaningful = lambda event: {key: value for key, value in event.items() if key != 'rawRegisterWords'}
        if [meaningful(event) for event in native['providedCalls']] != [meaningful(event) for event in candidate['providedCalls']]:
            raise ValueError('636 prepared service contracts or intermediate snapshots differ')
        if native['actualTopReturnedWords'][0] != candidate['actualTopReturnedWords'][0]:
            raise ValueError('636 physical full-word final return differs')
        nw, cw = [write[1:] for write in native['nonstackWrites']], [write[1:] for write in candidate['nonstackWrites']]
        order_equal = nw == cw
        if not order_equal:
            order_differences.append(profile['name'])
        different = [i for i, (left, right) in enumerate(zip(native['coreRegistersAndCpsr'], candidate['coreRegistersAndCpsr'])) if left != right]
        if different:
            raw_core_differences.append(dict(profile=profile['name'], coreWordIndexes=different))
        raw = [i for i, (left, right) in enumerate(zip(native['providedCalls'], candidate['providedCalls'])) if left['rawRegisterWords'] != right['rawRegisterWords']]
        if raw:
            raw_provider_differences.append(dict(profile=profile['name'], eventIndexes=raw))
        seen.update(native['ownObserved'])
        count = len(native['nativeReturns']) + len(candidate['nativeReturns'])
        supplied = len(native['providedCalls']) + len(candidate['providedCalls'])
        dependencies += count
        providers += supplied
        trace = dict(profile=profile, model=nm, native=compact(native), candidate=compact(candidate), independentCompleteNonstackModelsEqual=True, preparedServiceContractsEqual=True, orderedWritesEqual=order_equal, rawCoreDifferences=different, rawProviderRegisterDifferences=raw)
        traces.append(trace)
        cases.append(dict(profile=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=count, providedCalls=supplied, orderedWritesEqual=order_equal, traceSha256=c.sha(encoded(trace))))
        if index % 24 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    unsupported = []
    for category in [3, 4, 5]:
        try:
            M.Machine(original, dict(profiles[0], category=category))
        except ValueError as error:
            unsupported.append(dict(category=category, executionStarted=False, reason=str(error)))
        else:
            raise ValueError('636 unresolved inherited-register path was not rejected')
    template = SOURCE.read_text()
    choices = [('wrong-modifier', template.replace('0.012f', '0.013f'), next(p for p in profiles if p['modifier'] == 140 and p['case'] % 2 == 0)),
               ('wrong-halfword-store', template.replace('M2C_FIELD(native_data_ov001_0224991c,s16*,', 'M2C_FIELD(native_data_ov001_0224991c,u8*,', 1), profiles[1]),
               ('wrong-upper-cap', template.replace('0x270F', '0x270E'), profiles[1])]
    controls = []
    for name, text, profile in choices:
        if text == template:
            raise ValueError('636 wrong source unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-growth636-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('636 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr, wp, wb = compile_unit(source, 'wrong-' + name)
        result = M.Machine(original, profile, wb).run()
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError(('636 returning wrong source escaped independent model', name, profile['name']))
        trace = dict(profile=profile, result=compact(result), actuallyReturned=True, modelFailure=failure)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=wr, genuineLinkComparison=wp, actuallyReturned=True, actualTopReturns=1, failure=failure, traceSha256=c.sha(encoded(trace))))
    raw = encoded(dict(cases=traces))
    artifact = ROOT / 'evidence/generated/ov001-growth636-functional-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], address=hex(M.ENTRY), mode='arm', bytes=M.SIZE, sourceCredit=0, source=row, genuineLinkComparison=proof, callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualWatchedNativeDependencyReturns=dependencies, providedCalls=providers, supportedCategoryValues=[0, 1, 2], rejectedUnsupportedSetups=unsupported, independentCompleteNonstackRamModelsEqual=True, intermediateCalculatedStatSnapshotsEqual=True, relevantPreparedServiceContractsEqual=True, finalPhysicalR0WordsEqual=True, orderedWriteDifferences=order_differences, rawCoreDifferences=raw_core_differences, rawProviderRegisterDifferences=raw_provider_differences, cases=cases, observedNativeOwnAddresses=sorted(seen), observedNativeOwnInstructionBytes=4 * len(seen), negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), limits=['Complete1696-byte ordinary C hypothesis remains nonmatching: genuine compiled1644 bytes, only628 same-offset bytes; zero source credit.', 'Category outside0..2 requires unresolved inheritedR8 and staleSP+4. The C locals are uninitialized there; these paths are rejected before execution, never described as an original bug or repaired with a fabricated parameter/default.', 'Resource lifetime, callbacks, normalization, variant adjustment, category/metadata lookup and six final feature calls are explicitly supplied zero-RAM service boundaries.', 'Original native two32-byte clears, RNG/division and all signed/unsigned binary32 conversions/add/multiply/divide execute; every meaningful float input/result is independently checked for this finite domain.', 'Native/C final memory effects and intermediate capped-stat snapshots agree under the supported synthetic domain. Raw write ordering and unspecified scratch-word differences remain failures in the report, not exact equivalence.', 'The ordinary upstream caller discardsR0. The void wrapper preserves the observed full physical final helper word while only its low16 is stored; no public return meaning or helper range is inferred.', 'No scene, legal asset-domain, birth/scratch-byte33, whole combat or application integration claim.'])
    write_json(ROOT / 'evidence/attempts/ov001-growth636-functional-source-20261101.json', report)
    print(dict(callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualWatchedNativeDependencyReturns=dependencies, providedCalls=providers, writeOrderDifferentCases=len(order_differences), rawCoreDifferentCases=len(raw_core_differences), sourceCredit=0), flush=True)


if __name__ == '__main__':
    execute()
