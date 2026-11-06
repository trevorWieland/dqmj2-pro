import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov003_panel652_machine_20261101 as M
import ov003_panel652_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov003_20261101_panel652/source.c'
WORK = ROOT / 'work/ol652-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov003', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('652 ordinary C compilation failed')
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
        raise ValueError('652 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov003-panel652-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('652 frozen input differs', item['path']))
    accepted = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov003' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + M.SIZE) for row in accepted):
        raise ValueError('652 accepted snapshot overlap')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'caller', True)
    span = original['overlay'][M.ENTRY - M.OVERLAY:M.ENTRY - M.OVERLAY + M.SIZE]
    if body != span:
        raise ValueError('652 complete genuine linked bytes differ')
    row['exactBytes'], row['genuineLinkComparison'] = M.SIZE, freeze_link(proof)
    cases, traces, seen = [], [], set()
    dependencies, providers = 0, 0
    profiles = P.profiles()
    for index, profile in enumerate(profiles):
        native, candidate = M.Machine(original, profile).run(), M.Machine(original, profile, body).run()
        nm, cm = P.model(native, original['mapping']), P.model(candidate, original['mapping'])
        for key in ['coreRegistersAndCpsr', 'nativeReturns', 'providedCalls', 'nonstackWrites', 'after']:
            if native[key] != candidate[key]:
                raise ValueError(('652 native/linked C differs', profile['name'], key))
        if nm != cm:
            raise ValueError('652 complete independent models differ')
        seen.update(native['ownObserved'])
        count, provided = len(native['nativeReturns']) * 2, len(native['providedCalls']) * 2
        dependencies += count
        providers += provided
        trace = dict(native=compact(native), model=nm, bothActuallyReturned=True, completeRamCoreAndWritesEqual=True, fullAfterRamSha256=c.sha(native['after']), candidateInstructions=candidate['instructions'])
        traces.append(trace)
        cases.append(dict(profile=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=count, providedCalls=provided, traceSha256=c.sha(encoded(trace))))
        if index % 18 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    excluded = set(range(0x021DF774, 0x021DF7A4, 4))
    code = set(range(M.ENTRY, M.ENTRY + 372, 4))
    if seen != code - excluded:
        raise ValueError(('652 supported instruction coverage differs', sorted((code - excluded) - seen), sorted(seen - code)))
    template = SOURCE.read_text()
    active = next(profile for profile in profiles if profile['pattern'] == 'active15' and profile['mode'] == 0 and profile['name'].endswith('salt0'))
    choices = [('wrong-range-start', template.replace('var_r4_2 >= 8', 'var_r4_2 >= 9', 1)),
               ('wrong-signed-stack-coordinate', template.replace('(s32) (s8) M2C_FIELD(temp_r9_2, u8 *, 0x5F)', '(s32) (u8) M2C_FIELD(temp_r9_2, u8 *, 0x5F)', 1)),
               ('wrong-resource-flag', template.replace('& 2) == 2', '& 1) == 1', 1))]
    controls = []
    for name, text in choices:
        if text == template:
            raise ValueError('652 wrong source unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-panel652-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('652 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr, wp, wb = compile_unit(source, 'wrong-' + name, False)
        result = M.Machine(original, active, wb).run()
        try:
            P.model(result, original['mapping'])
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError(('652 returning wrong source escaped model', name))
        trace = dict(result=compact(result), actuallyReturned=True, modelFailure=failure)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=wr, genuineLinkComparison=wp, actuallyReturned=True, actualTopReturns=1, failure=failure, traceSha256=c.sha(encoded(trace))))
    literals = []
    for offset in range(372, 388, 4):
        target, readers = M.ENTRY + offset, []
        for index in range(0, 372, 4):
            word, pc = int.from_bytes(span[index:index + 4], 'little'), M.ENTRY + index
            if word >> 28 == 14 and word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == target:
                readers.append(hex(pc))
        if not readers or any(int(pc, 16) not in seen for pc in readers):
            raise ValueError('652 observed unconditional literal reader absent')
        literals.append(dict(address=hex(target), value=hex(int.from_bytes(span[offset:offset + 4], 'little')), bytes=4, observedUnconditionalReaders=readers))
    raw = encoded(dict(cases=traces))
    artifact = ROOT / 'evidence/generated/ov003-panel652-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    row['oracle'] = dict(callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=providers, supportedObservedCodeBytes=4 * len(seen), originalCodeBytes=372, codeBytesUnexecutedUnderStablePureMapping=48, referencedLiteralBytes=16, unclassifiedBytes=0, fullRamAndOrderedEffectsEqual=True, allArmCoreRegistersAndCpsrEqual=True, preparedProviderContractsAndRawRegisterWordsEqual=True, casesEvidence=cases)
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov003', moduleSha256=original['module']['sha256'], emulationModel='UC_CPU_ARM_946', matches=[row], nativeSymbols={rel['symbol']: rel['target'] for rel in row['relocations']}, nativeSymbolEntries=qualified_bindings(row), negativeEvidence=controls, literalEvidence=literals, nativeMappingInput=dict(address=hex(M.MAPDATA), bytes=63, sha256=c.sha(original['mapping']), source='Unchanged measured initialized overlay bytes; no reconstructed data credit'), unexecutedPath=dict(address='0x021DF774', bytes=48, predicate='Inner slot-tag127 after original pure mapper just returned a value other than127', qualifiedReason='For stable slot memory, mapper127 returns127 and skips the inner branch; no synthetic map replacement or asynchronous slot mutation is supplied', actualMapperWrites=0, scope='Only this isolated stable-memory execution; interrupt/concurrency/loaded-module changes are not generalized'), generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), wholeModuleLinked=False, sourceReconstructionComplete=False, limits=['Only this388-byte ordinary caller is reconstructed; original slot getter,mapper,empty constructor and cleanup loops add zero source credit.', 'Coordinates and resource-slot/metadata state in BSS/private RAM are supplied. The21-record mapping is unchanged measured initialized ROM data.', 'Constructor02049008 executes only the supplied count0 descriptor early-return path; no nonzero constructor/resource lifecycle qualification.', 'Selection0206B324, rendering0206006C and70 lower0208522C calls per run are supplied zero-RAM boundaries. They are never counted as native execution.', 'The48-byte inner sentinel branch is not exercised under the actual pure mapper and stable slot data. Concurrent mutation and other program lifecycles remain unsupported.', 'Physical final R0 is35 from actual cleanup loops; original public formal/return meanings and current UI/game state are not inferred.', 'No application adapter/UI changes, original input mutation or whole-scene claim.'])
    write_json(ROOT / 'evidence/matches/ov003-20261101-panel652.json', report)
    print(dict(functions=1, matchedBytes=M.SIZE, callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=providers, wrongActualReturns=len(controls)), flush=True)


if __name__ == '__main__':
    execute()
