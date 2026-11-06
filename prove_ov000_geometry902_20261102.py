import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
import unicorn
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_geometry902_machine_20261102 as M
import ov000_geometry902_model_20261102 as G

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-geometry876/021dbc18/whole-q12'
WORK = ROOT / 'work/ol902-proof'


def build(source, name, origin):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov000', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('902 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'} | dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('902 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov000-geometry902-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('902 input differs', row['path']))
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov000')
    candidate, body = build(SOURCE / 'source.c', 'candidate', 0x02650000)
    if candidate['canonicalComparison'].get('exactCallerBytes'):
        raise ValueError('902 unexpectedly exact; review outside research gate')
    template = (SOURCE / 'source.c').read_text()
    wrongReturn = template.replace('    return found;', '    return found ^ 1;')
    wrongPoint = template.replace('        output->y = resultY;', '        output->y = resultY + 4096U;')
    wrongDivisor = template.replace('                displacement = (s32) (0U - ratio);', '                ratio = 0U;\n                displacement = (s32) (0U - ratio);')
    if any(text == template for text in [wrongReturn, wrongPoint, wrongDivisor]):
        raise ValueError('902 whole-C control site absent')
    images = {0x02650000: body}
    controls = []
    for index, (name, text) in enumerate([('wrong-return', wrongReturn), ('wrong-point', wrongPoint), ('wrong-ratio', wrongDivisor)]):
        origin = 0x02652000 + index * 0x2000
        directory = ROOT / 'nonmatching/overlay-lane/20261102-geometry902' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('902 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, image = build(source, name, origin)
        images[origin] = image
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    traces = []
    cases = []
    pcs = set()
    totals = dict(pairs=0, actualTopReturns=0, actualNativeHelperReturns=0, suppliedCalls=0, independentModelPairs=0, hitPairs=0, missPairs=0)
    profiles = G.profiles()
    for profile in profiles:
        results = []
        failures = []
        for kind, entry in [('native', M.ENTRY), ('candidate', 0x02650000)] + [(row['name'], row['origin']) for row in controls]:
            vm = M.Machine(main, overlay, images, profile)
            result = vm.run(entry)
            result['kind'] = kind
            results.append(result)
            failure = G.model(vm, result)
            travel = profile['point'][1] + 4096 - profile.get('slopeX', 0) * profile['point'][0] - profile.get('slopeZ', 0) * profile['point'][2]
            if any(row['actualReturnWord'] != travel for row in result['calls'] if row['target'] == '0x200235c'):
                failure.append('independent integer-plane native ratio return')
            failures.append(failure)
        original, hypothesis = results[:2]
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov000-geometry902-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('902 model rejected', profile['ordinal'], failures[:2]))
        fields = ['outputHex', 'meshHex', 'contextHex', 'calls', 'writes', 'deviceWrites', 'hardwareOperations', 'hardwareSha256']
        differences = [key for key in fields if original[key] != hypothesis[key]]
        if differences or original['registers'][0] != hypothesis['registers'][0]:
            raise ValueError(('902 relevant own effects differ', profile['ordinal'], differences))
        firstStack = min(original['privateStackStart'], hypothesis['privateStackStart'])
        if firstStack < M.SP - 0x1000 or firstStack > M.SP:
            raise ValueError('902 private stack bound')
        memories = []
        for result in [original, hypothesis]:
            memory = bytearray(result['memory'])
            memory[firstStack - 0x02000000:M.SP - 0x02000000] = bytes(M.SP - firstStack)
            memories.append(memory)
        if memories[0] != memories[1]:
            raise ValueError('902 observable RAM difference outside measured private stack')
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        totals['hitPairs' if original['registers'][0] else 'missPairs'] += 1
        totals['suppliedCalls'] += sum('suppliedReturn' in row for result in [original, hypothesis] for row in result['calls'])
        totals['actualNativeHelperReturns'] += sum(len(result['nativeHelperPhysicalReturns']) for result in [original, hypothesis])
        pcs.update(original['ownPcs'])
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(compact, results)), modelFailures=failures, consumedAbiDifferences=differences, observedPrivateStackStart=firstStack, observableRamSha256=hashlib.sha256(memories[0]).hexdigest(), scratchDifferences=[i for i in [1, 2, 3, 12] if original['registers'][i] != hypothesis['registers'][i]], cpsrDiffers=original['cpsr'] != hypothesis['cpsr'])
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        cases.append(dict(ordinal=profile['ordinal'], traceSha256=hashlib.sha256(raw).hexdigest(), actualTopReturns=2))
        traces.append(trace)
    if any(not row['rejected'] for row in controls) or not totals['hitPairs'] or not totals['missPairs']:
        raise ValueError('902 positive/negative scope incomplete')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov000-geometry902-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, canonicalMatchedFunctions=0, canonicalMatchedBytes=0, allPassed=True, romSha256=configuration()['romSha256'], module='ov000', processor='arm9', program='', address=hex(M.ENTRY), nativeBytes=1884, moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], candidate=candidate, totals=totals, relevantAbiOwnEffectsEqual=True, observableRamEqualOutsideMeasuredPrivateStack=True, nativeOwnInstructionAddresses=sorted(pcs), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Behavior-qualified near C only; canonical1884-byte source match fails and compiled1272-byte image runs at a genuine private origin without overwriting adjacent native functions.', 'Synthetic one-record mesh/one-block tree, all three adjacency entries negative, low16 initial index0, all256 raw capacity-byte representations, four index-word upper halves, poisoned prior count/list, bounded horizontal/tilted Q12 planes, flags and optional output. Arbitrary graphs/meshes, multiple candidate records and ordinary scene reachability remain unqualified.', 'Independent integer geometric model checks inclusive triangle containment, downward projection from y+4096, squared displacement threshold0x4000, unchanged mesh, original preparation list/count writes, hit metadata writes and exact output point/return behavior. Plane slopes include(0,0),(1,0),(0,1),(-1,1); all plane/cross inputs are bounded integer Q12 values.', 'Original main235C/2458/23C4 execute with unchanged pinned BlendMathHardware mode1. Only its supported numerator>=0/denominator>0 domain is selected; busy latency, signed-negative/zero divisors and other modes remain unsupported. Actual return opcodes/SP/callee-saved state and full4KiB MMIO state are checked. Original BBB8/BB50/B968 preparation and A57C hit notification execute and mutate context; zero function providers. Hardware MMIO behavior remains a supplied pinned model, with no real-device coherence or timing claim.', 'The positive-domain subset excludes reversed normals and negative ray travel. Both geometry input words and actual original wrapper return equal the independent integer-plane projection model. Actual preparation overwrites the poisoned prior count and establishes one candidate before eligibility. All helper entries, actual return opcodes and seven physical BB50/B968 caller words are checked; no original formal arity is inferred from those views. Frozen874/877 full-domain supplied-boundary proofs remain unchanged.', 'Both full private-linked C and original properly return with preserved callee-saved GPRs/SP; caller-saved/CPSR/call-unused words remain qualified. RAM excludes only the union of measured callee-private stack; all original/private code storage is identical across compared machines.', 'Unsigned modular Q12 expressions avoid signed64 sum overflow; this packet establishes pinned ARM behavior only; separate895 PE32 bounded execution remains frozen. Per-call native/private LR addresses are retained, and complete RAM comparisons catch any such address escaping callee-private stack.', 'No exact/module/ROM credit, game meaning, application/UI changes, record33 or host/device execution claim.'])
    write_json(ROOT / 'evidence/application/ov000-geometry902-behavior-20261102.json', report)
    print(dict(**totals, sourceCredit=0, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    execute()
