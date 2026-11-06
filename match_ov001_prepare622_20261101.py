import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_prepare622_machine_20261101 as M
import ov001_prepare622_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov001_20261101_prepare622/source.c'
WORK = ROOT / 'work/ol622-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', False)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('622 ordinary C compilation failed')
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'link'
    try:
        proof = validate(row, qualified_bindings(row), directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0], dict):
            raise
        proof = error.args[0]
    return row, proof, (directory / 'caller.bin').read_bytes()


def compact(result):
    return {key: result[key] for key in ['profile', 'coreRegistersAndCpsr', 'nativeReturns', 'providedCalls', 'nonstackWrites', 'ownObserved', 'nativeObserved', 'instructions']}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('622 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov001-prepare622-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('622 frozen input differs', item['path']))
    accepted = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + M.SIZE) for row in accepted):
        raise ValueError('622 accepted snapshot overlap')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'caller', True)
    span = original['overlay'][M.ENTRY - M.OVERLAY:M.ENTRY - M.OVERLAY + M.SIZE]
    if body != span:
        raise ValueError('622 actual complete freshly linked span differs')
    row['exactBytes'] = M.SIZE
    row['genuineLinkComparison'] = freeze_link(proof)
    cases, traces, seen = [], [], set()
    dependencies, providers = 0, 0
    profiles = P.profiles()
    for index, profile in enumerate(profiles):
        native = M.Machine(original, profile).run()
        candidate = M.Machine(original, profile, body).run()
        nm, cm = P.model(native), P.model(candidate)
        for key in ['coreRegistersAndCpsr', 'nativeReturns', 'providedCalls', 'nonstackWrites', 'after']:
            if native[key] != candidate[key]:
                raise ValueError(('622 native/linked C differs', profile['name'], key))
        if nm != cm:
            raise ValueError('622 complete independent models differ')
        seen.update(native['ownObserved'])
        count, provided = 2 * len(native['nativeReturns']), 2 * len(native['providedCalls'])
        dependencies += count
        providers += provided
        trace = dict(native=compact(native), model=nm, candidateInstructions=candidate['instructions'], bothActuallyReturned=True, fullAfterRamSha256=c.sha(native['after']), completeRamCoreAndWritesEqual=True)
        traces.append(trace)
        cases.append(dict(profile=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=count, providedCalls=provided, traceSha256=c.sha(encoded(trace))))
        if index % 72 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    code = set(range(M.ENTRY, M.ENTRY + 284, 4))
    if seen != code:
        raise ValueError(('622 complete native own-code coverage differs', sorted(code - seen)))
    template = SOURCE.read_text()
    lookup_profile = lambda kind, mode: next(profile for profile in profiles if profile['row'] == 0 and profile['header'] & 15 == kind and profile['mode'] == mode)
    choices = [('wrong-six-group', template.replace('case 6:', 'case 7:', 1), lookup_profile(6, 100)),
               ('wrong-hundred-mode', template.replace('case 100:', 'case 99:', 1), lookup_profile(1, 100)),
               ('wrong-full-word-store', template.replace('*(u16*)', '*(u32*)', 1), lookup_profile(1, 0))]
    controls = []
    for name, text, profile in choices:
        if text == template:
            raise ValueError('622 wrong source unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-prepare622-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('622 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr, wp, wb = compile_unit(source, 'wrong-' + name, False)
        result = M.Machine(original, profile, wb).run()
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError('622 returning wrong source escaped independent model')
        trace = dict(result=compact(result), actuallyReturned=True, modelFailure=failure)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=wr, genuineLinkComparison=wp, actualTopReturns=1, actuallyReturned=True, failure=failure, traceSha256=c.sha(encoded(trace))))
    literals = []
    for offset in range(284, 308, 4):
        target, readers = M.ENTRY + offset, []
        for index in range(0, 284, 4):
            word = int.from_bytes(span[index:index + 4], 'little')
            pc = M.ENTRY + index
            if word >> 28 == 14 and word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == target:
                readers.append(hex(pc))
        if not readers or any(int(pc, 16) not in seen for pc in readers):
            raise ValueError('622 unconditional native literal reader not executed')
        literals.append(dict(address=hex(target), value=hex(int.from_bytes(span[offset:offset + 4], 'little')), bytes=4, observedUnconditionalReaders=readers))
    raw = encoded(dict(cases=traces))
    artifact = ROOT / 'evidence/generated/ov001-prepare622-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    row['oracle'] = dict(callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=providers, ownObservedCodeBytes=284, referencedLiteralBytes=24, unclassifiedBytes=0, fullRamAndOrderedEffectsEqual=True, allArmCoreRegistersAndCpsrEqual=True, preparedProviderContractsAndRawRegisterWordsEqual=True, casesEvidence=cases)
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], emulationModel='UC_CPU_ARM_946', matches=[row], nativeSymbols={rel['symbol']: rel['target'] for rel in row['relocations']}, nativeSymbolEntries=qualified_bindings(row), negativeEvidence=controls, literalEvidence=literals, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), wholeModuleLinked=False, sourceReconstructionComplete=False, limits=['Only this308-byte ordinary caller is reconstructed; actual native RNG/division add zero source credit.', 'Initializer02044FF4 and metadata lookup020449D4 are explicitly supplied with zero RAM effects; their original bodies are not executed or counted.', 'Synthetic row0..2, full32-bit ID words, every low4 metadata value, poisoned upper header bits, nine raw mode bytes and deterministic seeds are tested.', 'For raw low4 kinds1..6 and unrecognized modes the variant byte remains its supplied poison0xCC; the fixture does not infer a legal game-mode restriction.', 'The source bitfield describes measured16-bit load/low4 extraction only. Original formal types and meanings remain unproved.', 'The caller has the separately reconstructed CD00 upstream caller, but this packet does not execute it or establish current scene/RNG/input lifecycle.', 'Physical R0 forwards the final RNG result; the ordinary C wrapper is void and no semantic return value is claimed.'])
    write_json(ROOT / 'evidence/matches/ov001-20261101-prepare622.json', report)
    print(dict(functions=1, matchedBytes=M.SIZE, callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=providers, wrongActualReturns=len(controls)), flush=True)


if __name__ == '__main__':
    execute()
