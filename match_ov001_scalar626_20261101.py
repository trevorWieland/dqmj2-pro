import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_scalar626_machine_20261101 as M
import ov001_scalar626_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov001_20261101_scalar626/source.c'
WORK = ROOT / 'work/ol626-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_unit(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError('626 ordinary C compilation failed')
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
    return {key: result[key] for key in ['profile', 'coreRegistersAndCpsr', 'actualTopReturnedWords', 'nativeReturns', 'nonstackWrites', 'ownObserved', 'mainObserved', 'instructions']}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('626 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov001-scalar626-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('626 frozen input differs', item['path']))
    accepted = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + M.SIZE) for row in accepted):
        raise ValueError('626 accepted snapshot overlap')
    original = M.inputs()
    row, proof, body = compile_unit(SOURCE, 'caller', True)
    span = original['overlay'][M.ENTRY - M.OVERLAY:M.ENTRY - M.OVERLAY + M.SIZE]
    if body != span:
        raise ValueError('626 complete genuine linked bytes differ')
    row['exactBytes'], row['genuineLinkComparison'] = M.SIZE, freeze_link(proof)
    cases, traces, seen = [], [], set()
    profiles = P.profiles()
    dependencies = 0
    for index, profile in enumerate(profiles):
        native, candidate = M.Machine(original, profile).run(), M.Machine(original, profile, body).run()
        nm, cm = P.model(native), P.model(candidate)
        for key in ['coreRegistersAndCpsr', 'nativeReturns', 'nonstackWrites', 'after']:
            if native[key] != candidate[key]:
                raise ValueError(('626 native/linked C differs', profile['name'], key))
        if nm != cm:
            raise ValueError('626 independent complete models differ')
        seen.update(native['ownObserved'])
        count = len(native['nativeReturns']) * 2
        dependencies += count
        trace = dict(native=compact(native), model=nm, candidateInstructions=candidate['instructions'], bothActuallyReturned=True, completeRamCoreAndWritesEqual=True, fullAfterRamSha256=c.sha(native['after']))
        traces.append(trace)
        cases.append(dict(profile=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=count, withinUnsigned16CallerDomain=profile['withinUnsigned16CallerDomain'], traceSha256=c.sha(encoded(trace))))
        if index % 96 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    if seen != set(range(M.ENTRY, M.ENTRY + 112, 4)):
        raise ValueError('626 complete native own code coverage differs')
    template = SOURCE.read_text()
    profile_for = lambda scalar: next(profile for profile in profiles if profile['row'] == 0 and profile['scalar'] == scalar)
    choices = [('wrong-multiply', template.replace('1.25,', '1.5,', 1), profile_for(4)),
               ('wrong-wide-minimum', template.replace('u16 value = (u16)', 'u32 value = (u32)', 1), profile_for(52389)),
               ('wrong-cap', template.replace('value > 100', 'value > 99').replace(' = 100;', ' = 99;'), profile_for(40))]
    controls = []
    for name, text, profile in choices:
        if text == template:
            raise ValueError('626 wrong source unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-scalar626-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('626 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wr, wp, wb = compile_unit(source, 'wrong-' + name, False)
        result = M.Machine(original, profile, wb).run()
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError('626 returning wrong source escaped independent model')
        trace = dict(result=compact(result), actuallyReturned=True, modelFailure=failure)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=wr, genuineLinkComparison=wp, actuallyReturned=True, actualTopReturns=1, failure=failure, traceSha256=c.sha(encoded(trace))))
    literals = []
    for offset in range(112, 124, 4):
        target, readers = M.ENTRY + offset, []
        for index in range(0, 112, 4):
            word, pc = int.from_bytes(span[index:index + 4], 'little'), M.ENTRY + index
            if word >> 28 == 14 and word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == target:
                readers.append(hex(pc))
        if not readers or any(int(pc, 16) not in seen for pc in readers):
            raise ValueError('626 observed unconditional literal reader absent')
        literals.append(dict(address=hex(target), value=hex(int.from_bytes(span[offset:offset + 4], 'little')), bytes=4, observedUnconditionalReaders=readers))
    raw = encoded(dict(cases=traces))
    artifact = ROOT / 'evidence/generated/ov001-scalar626-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    generated = dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw))
    row['oracle'] = dict(callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=0, ownObservedCodeBytes=112, referencedLiteralBytes=12, unclassifiedBytes=0, fullRamAndOrderedEffectsEqual=True, allArmCoreRegistersAndCpsrEqual=True, allFiniteBinary64ArgumentAndReturnPairsModeled=True, casesEvidence=cases)
    contracts = [dict(entry=hex(M.U32DOUBLE), consumedWords='R0 unsigned32', returnedWords='IEEE binary64 R0-low/R1-high', domain='Listed scalar words0..3435973796'), dict(entry=hex(M.MULTIPLY), consumedWords='Binary64 R0/R1 and R2/R3', returnedWords='IEEE binary64 R0-low/R1-high', domain='1.25 times listed nonnegative exact converted scalar'), dict(entry=hex(M.ADD), consumedWords='Binary64 R0/R1 and R2/R3', returnedWords='IEEE binary64 R0-low/R1-high', domain='50.0 plus the listed finite products'), dict(entry=hex(M.TRUNCATE), consumedWords='Binary64 R0-low/R1-high', returnedWords='Unsigned32 integral in R0; R1 is scratch', domain='Listed nonnegative finite sums through4294967295')]
    write_json(ROOT / 'evidence/abi/main-float626-row-scalar-chain-20261101.json', dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='main', moduleSha256=original['main']['sha256'], sourceCredit=0, providedCalls=0, actualNativeReturnsAcrossBothCallerRuns=dependencies, callerPairs=len(profiles), existingCallerExecutionsReused=True, additionalExecutions=0, contracts=contracts, generatedTrace=generated, publicOriginalTypesProven=False, limits=['These are finite measured word contracts from the ordinary caller, not general special-value/overflow contracts.', 'Both original and candidate call the same original native helpers; their returns are counted once in the caller report, not added again as separate ABI executions.']))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=original['module']['sha256'], matches=[row], nativeSymbols={rel['symbol']: rel['target'] for rel in row['relocations']}, nativeSymbolEntries=qualified_bindings(row), negativeEvidence=controls, literalEvidence=literals, generatedTrace=generated, physicalMathContracts=contracts, wholeModuleLinked=False, sourceReconstructionComplete=False, limits=['Only this124-byte ordinary caller is reconstructed; original math helper execution gives zero new helper source credit.', 'There are zero supplied callees; original unsigned-to-double, multiplication, addition and unsigned conversion execute with their complete word pairs checked.', 'Finite scalar words through3435973796 and row0..2 are qualified; values producing unsigned conversion overflow, NaN/Inf/negative conversion, malformed pointers and ordinary scene reachability remain unsupported.', 'The separate actual upstream getter supplies an unsigned16 scalar. Listed larger words are direct-entry tests and do not establish ordinary caller inputs.', 'The low16 truncation occurs before cap100; wrapped small outputs from large unsigned16 inputs are measured, not an inferred legal game domain.', 'Original public formal types and semantic return meaning are not established; physical R0 retains the base byte-address residue.'])
    write_json(ROOT / 'evidence/matches/ov001-20261101-scalar626.json', report)
    print(dict(functions=1, matchedBytes=M.SIZE, callerPairs=len(profiles), actualTopReturns=2 * len(profiles), actualNativeDependencyReturns=dependencies, providedCalls=0, wrongActualReturns=len(controls)), flush=True)


if __name__ == '__main__':
    execute()
