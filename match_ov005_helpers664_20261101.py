import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov005_helpers664_machine_20261101 as M
import ov005_helpers664_models_20261101 as P
SOURCE = ROOT / 'src/overlays/ov005_20261101_helpers664/source.c'
WORK = ROOT / 'work/ol664-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compile_units(source, name, exact):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov005', '2', 'off', True)
    if len(rows) != 2 or any(row.get('compileFailed') for row in rows):
        raise ValueError('664 ordinary C compilation failed')
    out = {}
    for row in rows:
        entry = int(row['address'], 16)
        row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
        directory = WORK / name / ('link-' + row['address'])
        try:
            proof = validate(row, qualified_bindings(row), directory)
        except ValueError as error:
            if exact or not isinstance(error.args[0], dict):
                raise
            proof = error.args[0]
        out[entry] = row, proof, (directory / 'caller.bin').read_bytes()
    return out


def compact(result):
    return {key: result[key] for key in ['profile', 'coreRegistersAndCpsr', 'providedCalls', 'payloadReads', 'ownObserved', 'instructions']}


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('664 runtime differs')
    pins = json.loads((ROOT / 'evidence/verification/ov005-helpers664-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('664 frozen input differs', item['path']))
    accepted = json.loads((ROOT / pins['acceptedSnapshot']).read_text())['functions']
    for entry, size in M.SIZES.items():
        if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov005' and max(row['address'], entry) < min(row['address'] + row['bytes'], entry + size) for row in accepted):
            raise ValueError('664 accepted snapshot overlap')
    original = M.inputs()
    units = compile_units(SOURCE, 'positive', True)
    traces, stats = [], {}
    for entry, (row, proof, body) in units.items():
        span = original['image'][entry - M.OVERLAY:entry - M.OVERLAY + M.SIZES[entry]]
        if body != span:
            raise ValueError('664 complete genuine linked image differs')
        row['exactBytes'], row['genuineLinkComparison'] = M.SIZES[entry], freeze_link(proof)
        stats[entry] = dict(cases=[], seen=set(), provided=0)
    profiles = P.profiles()
    for index, profile in enumerate(profiles):
        entry = profile['entry']
        native = M.Machine(original, profile).run()
        candidate = M.Machine(original, profile, units[entry][2]).run()
        nm, cm = P.model(native), P.model(candidate)
        for key in ['coreRegistersAndCpsr', 'providedCalls', 'payloadReads', 'after']:
            if native[key] != candidate[key]:
                raise ValueError(('664 native/linked C differs', profile['name'], key))
        if nm != cm:
            raise ValueError('664 complete independent models differ')
        stats[entry]['seen'].update(native['ownObserved'])
        provided = len(native['providedCalls']) * 2
        stats[entry]['provided'] += provided
        trace = dict(native=compact(native), model=nm, bothActuallyReturned=True, completeRamCoreAndOrderedReadsEqual=True, fullAfterRamSha256=c.sha(native['after']), candidateInstructions=candidate['instructions'])
        traces.append(trace)
        stats[entry]['cases'].append(dict(profile=profile['name'], actualTopReturns=2, actualNativeDependencyReturns=0, providedCalls=provided, traceSha256=c.sha(encoded(trace))))
        if index % 100 == 0:
            print(dict(completedPairs=index + 1, total=len(profiles)), flush=True)
    controls = []
    template = SOURCE.read_text()
    variants = [('wrong-curve-index', template.replace('values[index-1]', 'values[index]', 1), 'curve-1'), ('wrong-point-rounding', template.replace('sum * count + 4', 'sum * count + 3', 1), 'points-1-1-1'), ('wrong-unsigned-accumulator', template.replace('s16 sum;', 'unsigned short sum;', 1).replace('sum = (s16)', 'sum = (unsigned short)', 1), 'points-2-129-1')]
    for name, text, case in variants:
        if text == template:
            raise ValueError('664 wrong source unchanged')
        directory = ROOT / 'nonmatching/overlay-lane/20261101-helpers664-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('664 frozen wrong source differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        profile = next(item for item in profiles if item['name'] == case)
        row, proof, body = compile_units(source, name, False)[profile['entry']]
        result = M.Machine(original, profile, body).run()
        try:
            P.model(result)
        except ValueError as error:
            failure = str(error)
        else:
            raise ValueError(('664 returning wrong source escaped model', name))
        trace = dict(result=compact(result), actuallyReturned=True, modelFailure=failure)
        traces.append(dict(negativeEvidence=name, **trace))
        controls.append(dict(name=name, source=row, genuineLinkComparison=proof, actuallyReturned=True, actualTopReturns=1, failure=failure, traceSha256=c.sha(encoded(trace))))
    matches, literals, bindings, native_symbols = [], [], {}, {}
    for entry, (row, proof, body) in units.items():
        stat = stats[entry]
        code_size = M.SIZES[entry] - (8 if entry == 0x021E6678 else 0)
        expected = set(range(entry, entry + code_size, 4))
        if stat['seen'] != expected:
            raise ValueError(('664 instruction coverage differs', hex(entry), sorted(expected - stat['seen']), sorted(stat['seen'] - expected)))
        for offset in range(code_size, M.SIZES[entry], 4):
            target, readers = entry + offset, []
            for index in range(0, code_size, 4):
                word, pc = int.from_bytes(body[index:index + 4], 'little'), entry + index
                if word >> 28 == 14 and word & 0x0F7F0000 == 0x051F0000 and pc + 8 + ((word & 4095) if word & 0x00800000 else -(word & 4095)) == target:
                    readers.append(hex(pc))
            if not readers or any(int(pc, 16) not in stat['seen'] for pc in readers):
                raise ValueError('664 unconditional literal readers absent')
            literals.append(dict(address=hex(target), bytes=4, value=hex(int.from_bytes(body[offset:offset + 4], 'little')), observedUnconditionalReaders=readers))
        row['oracle'] = dict(callerPairs=len(stat['cases']), actualTopReturns=2 * len(stat['cases']), actualNativeDependencyReturns=0, providedCalls=stat['provided'], observedCodeBytes=4 * len(stat['seen']), referencedLiteralBytes=M.SIZES[entry] - code_size, unclassifiedBytes=0, allArmCoreRegistersAndCpsrEqual=True, fullRamAndOrderedReadsEqual=True, casesEvidence=stat['cases'])
        matches.append(row)
        bindings.update(qualified_bindings(row))
        native_symbols.update({rel['symbol']: rel['target'] for rel in row['relocations']})
    raw = encoded(dict(cases=traces))
    artifact = ROOT / 'evidence/generated/ov005-helpers664-native-traces-20261101.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov005', moduleSha256=original['module']['sha256'], emulationModel='UC_CPU_ARM_946', matches=matches, nativeSymbols=native_symbols, nativeSymbolEntries=bindings, negativeEvidence=controls, literalEvidence=literals, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=c.sha(raw)), wholeModuleLinked=False, sourceReconstructionComplete=False, limits=['Two160B ordinary C units only. Isolated genuine MWLD comparisons require later integrator module acceptance.', 'Curve access accepts a nullable pointer and full signed32 index. Supplied nonnull indices-3..20 stay inside an actual mapped32-word array; no native bounds validation is inferred.', 'Point table levelsINT32_MIN,-1,0 and1..512 in listed profiles, counts-65535..65535 as listed, signed16 wrap per addition and final result. Model rejects signed32 product/add overflow.', 'Open0203CC2C and close0203CF9C are explicit supplied zero-RAM service boundaries; all1670 positive service calls are provided and count as zero native dependency returns.', 'Point payloads and allocation-handle words are synthetic. SkillPointTbl.bin filename is measured initialized ROM; no real resource contents/lifecycle/current state qualification.', 'Null-open paths test arbitrary large words without reading payload or evaluating nonnull multiplication. No malformed-resource, hardware, application or scene claim.'])
    write_json(ROOT / 'evidence/matches/ov005-20261101-helpers664.json', report)
    print(dict(functions=2, matchedBytes=160, callerPairs=len(profiles), actualTopReturns=len(profiles) * 2, actualNativeDependencyReturns=0, providedCalls=sum(s['provided'] for s in stats.values()), wrongActualReturns=len(controls)), flush=True)


if __name__ == '__main__':
    execute()
