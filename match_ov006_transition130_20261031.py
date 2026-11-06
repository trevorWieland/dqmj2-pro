import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov006_transition130_fixture_20261031 import ENTRY, NATIVE, execute
from ov006_transition130_models_20261031 import recipes
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__

WORK = ROOT / 'work/ol130-proof'
PINS = ROOT / 'evidence/verification/ov006-transition130-inputs-20261031.json'
PINS_HASH = '369e8ea03f3077d498550d8bf4a318c06d003e7e8d7ab4fb7e3055d142c0dc19'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def run():
    if sys.version_info[:3] != (3, 13, 5) or __version__ != '2.1.4' or sha256(PINS) != PINS_HASH:
        raise ValueError('Transition130 pinned runtime/manifest differs')
    pins = json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('Frozen transition130 input differs', item['path']))
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Transition130 measured private input differs')
    metadata, overlay, unused = measured_module('ov006')
    main_metadata, main, unused = measured_module('main')
    for kind in ['transition', 'predicate']:
        source = ROOT / ('src/overlays/ov006_20261031_' + kind + '130/' + kind + '.c')
        entry, size, instruction_bytes = ENTRY[kind]
        compiler.WORK = WORK / kind / 'c'
        rows, unused = compiler.compare(source, 'ov006', '2', 'off', True, thumb=True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size:
            raise ValueError('Transition130 complete ordinary C span differs')
        row = rows[0]
        row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
        bindings = qualified_bindings(row)
        directory = WORK / kind / 'l' / row['objectSha256']
        proof = validate(row, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        offset = entry - 0x021D7240
        if linked != overlay[offset:offset + size]:
            raise ValueError('Transition130 original/source full linked bytes differ')
        save_link_snapshots.DIRECTORY = WORK / 'immutable-links'
        row.update(save_link_snapshots.freeze_link(proof))
        row.update(exactAfterGenuineLink=True, linkedMatchingBytes=size, nativeSymbolEntries=bindings)
        results, summaries, observed = [], [], set()
        for index, recipe in enumerate(recipes(kind)):
            original, candidate = execute(kind, main, overlay, recipe), execute(kind, main, overlay, recipe, linked)
            if original != candidate:
                raise ValueError('Transition130 complete original/source machine results differ')
            observed.update(original['observedCallerInstructionBytes'])
            results.append(dict(recipe=recipe, result=original))
            summaries.append(dict(case=index, recipeSha256=compiler.sha(encoded(recipe)), completeResultSha256=compiler.sha(encoded(original)),
                actualReturns=2, nativeDependencyActualReturns=2 * len(original['nativeReturns']), providedCalls=2 * len(original['providedCalls']),
                instructions=original['instructions'], observedCallerInstructionBytes=len(original['observedCallerInstructionBytes']),
                ramSha256=original['ramSha256'], pcTraceSha256=compiler.sha(encoded(original['pcTrace'])), writeTraceSha256=compiler.sha(encoded(original['writes']))))
        control = ROOT / ('nonmatching/overlay-lane/20261031-' + kind + '130-negative')
        control.mkdir(parents=True, exist_ok=True)
        before, after = ('native_fn_ov006_02203954(1, 1)', 'native_fn_ov006_02203954(1, 2)') if kind == 'transition' else ('[0x19]', '[0x18]')
        body = source.read_text().replace(before, after)
        if body == source.read_text():
            raise ValueError('Locate transition130 ordinary C negative')
        for path, content in [(control / 'source.c', body.encode()), (control / 'context.h', source.with_name('context.h').read_bytes())]:
            if path.exists() and path.read_bytes() != content:
                raise ValueError('Preserve prior transition130 control')
            path.write_bytes(content)
        compiler.WORK = WORK / kind / 'negative/c'
        negative_rows, unused = compiler.compare(control / 'source.c', 'ov006', '2', 'off', True, thumb=True)
        if len(negative_rows) != 1 or negative_rows[0].get('compiledBytes') != size:
            raise ValueError('Transition130 control complete compilation differs')
        negative_directory = WORK / kind / 'negative/l'
        try:
            rejected_link = validate(negative_rows[0], qualified_bindings(negative_rows[0]), negative_directory)
        except ValueError as error:
            rejected_link = error.args[0]
        if not isinstance(rejected_link, dict) or rejected_link.get('caller') != negative_rows[0]['name']:
            raise ValueError('Transition130 ordinary control did not genuinely link')
        try:
            execute(kind, main, overlay, recipes(kind)[0], (negative_directory / 'caller.bin').read_bytes())
        except ValueError as error:
            failure = error.args[0]
            expected = 'Transition130 independent fresh-field arguments differ' if kind == 'transition' else 'Transition130 independent actual return/completion differs'
            if (failure[0] if isinstance(failure, tuple) else failure) != expected:
                raise ValueError(('Unexpected transition130 ordinary control rejection', failure))
        else:
            raise ValueError('Transition130 ordinary source control unexpectedly passed')
        raw = encoded(dict(romSha256=config['romSha256'], module='ov006', kind=kind, results=results))
        compressed = gzip.compress(raw, mtime=0)
        artifact = WORK / 'raw-traces' / (compiler.sha(compressed) + '.json.gz')
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(compressed)
        scopes = [dict(module='ov006', processor='arm9', program='', mode='thumb', address=hex(address), instructionBytes=count,
            nativeCodeSha256=compiler.sha(overlay[address - 0x021D7240:address - 0x021D7240 + count]), sourceCredit=0)
            for address, count in NATIVE.items() if address != entry] if kind == 'transition' else []
        row['oracle'] = dict(supported=True, evidenceClass='Independent Thumb pointer/byte predicate and mutable-state caller models with actual query/predicate/state/registration helpers',
            executions=2 * len(results), actualReturns=2 * len(results), nativeDependencyActualReturns=sum(item['nativeDependencyActualReturns'] for item in summaries),
            providedCalls=sum(item['providedCalls'] for item in summaries), freshMachinePerExecution=True, instructionBound=2000,
            maximumNativeInstructions=max(item['instructions'] for item in summaries), completeImageEquality=True,
            observedNativeCallerInstructionBytes=len(observed), results=summaries, nativeScopes=scopes,
            rawTraceArtifact=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=compiler.sha(compressed), bytes=len(compressed),
                gzipMtime=0, uncompressedSha256=compiler.sha(raw)),
            limitations=['Full raw byte predicate including null pointer is qualified; malformed nonnull pointers remain unsupported',
                'Caller192 recipes exercise native query fields9/21, null/zero/nonzero readiness field25, flag0/255, late provider writes and both stored Thumb callback addresses',
                'Only four original native helpers execute as callees; UI/action/reset bodies remain explicit providers with zero native/source credit',
                'Callback registration preserves the raw tagged pointer in R0 and RAM; neither callback body is invoked and no handler signature, loaded-scene validity or reachability is inferred',
                'The predicate32-byte source receives credit only through its own exact row, not again as a dependency of the148-byte caller'])
        paths = [item['path'] for item in pins['files']] + [control.relative_to(ROOT).as_posix() + '/source.c', control.relative_to(ROOT).as_posix() + '/context.h']
        report = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], processor='arm9', program='', module='ov006', mode='thumb',
            moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], matches=[row], isolatedLink=proof,
            nativeSymbols={item['symbol']: item['target'] for item in row['relocations']}, nativeSourceBytes=size, functionMatches=1,
            acceptedSourceCredit=0, wholeModuleLinked=False, sourceReconstructionComplete=False,
            rejectedBranchCode=dict(expectedRejected=True, failure=failure, compilation=negative_rows, actualLinkComparison=rejected_link, sourceCredit=0),
            inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in paths], generatorSha256=sha256(Path(__file__)),
            limitations=['Acceptance/whole-module and ROM gates remain integrator owned', 'createdUtc is volatile; stable identity excludes only that field',
                'No assembly, executable blobs, opcode patch, invented register inputs or dependency source credit'],
            reproductionCommand='python match_ov006_transition130_20261031.py')
        report['deterministicContentSha256'] = compiler.sha(encoded({key: value for key, value in report.items() if key != 'createdUtc'}))
        write_json(ROOT / ('evidence/matches/ov006-20261031-' + kind + '130.json'), report)
        print(json.dumps(dict(kind=kind, bytes=size, **{key: row['oracle'][key] for key in ['actualReturns', 'nativeDependencyActualReturns', 'providedCalls', 'observedNativeCallerInstructionBytes']})), flush=True)


if __name__ == '__main__':
    run()
