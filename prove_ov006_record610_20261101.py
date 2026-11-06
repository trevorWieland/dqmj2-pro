import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov006_record610_machine_20261101 as M
import ov006_record610_models_20261101 as P
SOURCE = ROOT / 'nonmatching/overlay-lane/20261101-record610/source.c'
WORK = ROOT / 'work/ol610-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_unit(source, name):
    previous = c.symbol_address
    def resolver(symbol):
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+', symbol):
            raise RuntimeError('610 unqualified compiler intrinsic rejected: ' + symbol)
        return previous(symbol)
    c.symbol_address = resolver
    c.WORK = WORK / name / 'compile'
    try:
        rows, unused = c.compare(source, 'ov006', '2', 'off', True)
    finally:
        c.symbol_address = previous
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('610 ordinary C failed compilation')
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
    return {key: result[key] for key in ['coreRegistersAndCpsr', 'nativeReturns', 'providedCalls', 'nonstackWrites', 'ownObserved', 'nativeObserved', 'instructions']}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('610 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov006-record610-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('610 frozen input differs', item['path']))
    selected = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    for entry in selected:
        if entry['processor'] == 'arm9' and entry['program'] == '' and entry['module'] == 'ov006' and entry['mode'] == 'arm' and entry['address'] < M.ENTRY + M.SIZE and entry['address'] + entry.get('bytes', 0) > M.ENTRY:
            raise ValueError('610 accepted snapshot overlaps the new draft')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'candidate')
    profiles, cases, traces, seen = P.profiles(), [], [], set()
    dependencies, providers = 0, 0
    for index, profile in enumerate(profiles):
        native = M.Machine(original, profile).run()
        candidate = M.Machine(original, profile, body).run()
        nm, cm = P.model(native), P.model(candidate)
        if nm != cm or native['providedCalls'] != candidate['providedCalls']:
            raise ValueError(('610 independent effects or provided contracts differ', profile['name']))
        nw = [write[1:] for write in native['nonstackWrites']]
        cw = [write[1:] for write in candidate['nonstackWrites']]
        if nw != cw or native['coreRegistersAndCpsr'] != candidate['coreRegistersAndCpsr']:
            raise ValueError(('610 ordered writes or raw core words differ', profile['name']))
        nr = [(ret['entry'], ret['returnedWords'][0]) for ret in native['nativeReturns']]
        cr = [(ret['entry'], ret['returnedWords'][0]) for ret in candidate['nativeReturns']]
        if nr != cr:
            raise ValueError('610 original dependency return order/result differs')
        seen.update(native['ownObserved'])
        count = len(native['nativeReturns']) + len(candidate['nativeReturns'])
        provided = len(native['providedCalls']) + len(candidate['providedCalls'])
        dependencies += count
        providers += provided
        trace = dict(profile=profile, model=nm, native=compact(native), candidate=compact(candidate), independentNonstackRamModelsEqual=True, orderedWritesEqual=True, allCoreRegistersAndCpsrEqual=True)
        traces.append(trace)
        cases.append(dict(profile=profile['name'], actualTopReturns=2, actualWatchedNativeDependencyReturns=count, providedCalls=provided, traceSha256=c.sha(encoded(trace))))
        if index % 16 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    template = SOURCE.read_text()
    choices = [('wrong-level-byte', template.replace('= temp_r10;', '= temp_r10 + 1;', 1), profiles[-1]),
               ('wrong-first-count', template.replace('var_r7 += 1;', 'var_r7 += 2;', 1), profiles[-1]),
               ('wrong-equality-selector', template.replace('var_r1 = 2;', 'var_r1 = 3;', 1), profiles[-2])]
    controls = []
    for name, text, profile in choices:
        if text == template:
            raise ValueError('610 wrong source was unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-record610-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('610 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr, wp, wb = compile_unit(source, 'wrong-' + name)
        result = M.Machine(original, profile, wb).run()
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError('610 returning wrong C escaped model')
        trace = dict(profile=profile, result=compact(result), modelFailure=failure, actuallyReturned=True)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=wr, genuineLinkComparison=wp, actualTopReturns=1, actuallyReturned=True, modelFailure=failure, traceSha256=c.sha(encoded(trace))))
    code = set(range(M.ENTRY, M.ENTRY + 1068, 4))
    if seen != code:
        raise ValueError(('610 full own native code coverage differs', len(seen), len(code), sorted(code - seen)))
    span = original['overlay'][M.ENTRY - M.OVERLAY:M.ENTRY - M.OVERLAY + M.SIZE]
    literals = []
    for offset in range(1068, 1092, 4):
        address = M.ENTRY + offset
        readers = []
        for index in range(0, 1068, 4):
            word = int.from_bytes(span[index:index + 4], 'little')
            pc = M.ENTRY + index
            if word >> 28 == 14 and word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == address:
                readers.append(hex(pc))
        if not readers or any(int(pc, 16) not in seen for pc in readers):
            raise ValueError('610 literal not independently referenced by observed code')
        literals.append(dict(address=hex(address), value=hex(int.from_bytes(span[offset:offset + 4], 'little')), bytes=4, unconditionalObservedReaders=readers))
    raw = encoded(dict(traces=traces))
    artifact = ROOT / 'evidence/generated/ov006-record610-functional-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov006', moduleSha256=original['module']['sha256'], address=hex(M.ENTRY), mode='arm', bytes=M.SIZE, sourceCredit=0, source=row, genuineLinkComparison=proof, callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualWatchedNativeDependencyReturns=dependencies, providedCalls=providers, cases=cases, nativeCodeBytes=1068, nativeReferencedLiteralBytes=24, nativeOwnObservedAddresses=sorted(seen), nativeLiteralEvidence=literals, allIndependentCompleteNonstackRamModelsEqual=True, allOrderedNonstackWritesEqual=True, allCoreRegistersAndCpsrEqual=True, allPreparedProviderWordsEqual=True, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), limits=['This 1092-byte ordinary C remains nonmatching: two adjacent STR/MOV instructions are ordered differently; source credit is zero.', 'Entry setup, new UID/record resolution, base/cap/category/growth callback values, file contents, curve allocation and final cleanup are supplied service boundaries.', 'Original native info getter, six growth bodies, point calculation, raw-five lookup, two-byte clearing, skill-pair setters, selector setter, RNG/division and context writer execute. Providers are never counted as native returns.', 'Synthetic signed species, raw variant/level bytes, raw five input bytes, raw base/cap words, category0..5, callback0..2, optional tables and mapped buffers are explicit input domains. No ordinary scene or lifecycle claim.', 'Skill iteration counts nonzero raw bytes then copies the first count bytes without compacting holes. No ability/skill identity semantics or original public formal types are claimed.', 'Both main and overlay are hash-qualified; another overlay at the same virtual address is a different program.'])
    write_json(ROOT / 'evidence/attempts/ov006-record610-functional-source-20261101.json', report)
    print(dict(callerPairs=len(profiles), actualTopReturns=len(profiles) * 2, actualWatchedNativeDependencyReturns=dependencies, providedCalls=providers, sourceCredit=0), flush=True)


if __name__ == '__main__':
    execute()
