import json
import shutil
import utility_code
import wave20261104_child_wm_cb_link as linker
from wave20261104_child_wm_cb_prepare import ROOT, LANE, WORK
from project import read_json, write_json, sha256


def main():
    report = read_json(LANE / 'packet-ready.json')
    entry = next(e for e in report['matches'] if int(e['address'], 0) == 0x027e10d4)
    spec = utility_code.accepted_spec(entry)
    spec.update(compilerPath=ROOT / entry['compiler'], compilerProc='arm7tdmi')
    flags = entry['compilerFlags']
    utility_code.WORK = WORK / 'controls-compiled'
    positive, code = utility_code.compile_compare(ROOT / entry['source'], spec, flags[0][2:],
        flags[flags.index('-inline') + 1], 'speed' in flags)
    if code is None:
        raise ValueError('Positive whole C control failed')
    positive_link = linker.validate(positive, WORK / 'controls-positive-link')
    destination = WORK / 'controls-source'
    destination.mkdir(parents=True, exist_ok=True)
    for dependency in entry['sourceDependencies']:
        shutil.copyfile(ROOT / dependency['path'], destination / (ROOT / dependency['path']).name)
    text = (ROOT / entry['source']).read_text()
    if text.count('callback->state = WM_STATECODE_MPACK_IND;') != 1:
        raise ValueError('Expected exact typed source expressions are absent')
    wrong = destination / 'wrong-parent-size.c'
    wrong.write_text(text.replace('callback->state = WM_STATECODE_MPACK_IND;', 'callback->state = WM_STATECODE_MPACK_IND + 1;'))
    row, code = utility_code.compile_compare(wrong, spec, flags[0][2:], flags[flags.index('-inline') + 1], 'speed' in flags)
    if row.get('compileFailed') or code is not None or row['compiledBytes'] != entry['bytes']:
        raise ValueError('Wrong C must compile completely with the same extent and fail the exact byte gate')
    refusal = None
    try:
        linker.validate(row, WORK / 'controls-wrong-link')
    except ValueError as error:
        refusal = repr(error)
    link_attempt = read_json(WORK / 'controls-wrong-link/link-attempt.json')
    output = WORK / 'controls-wrong-link/caller.bin'
    raw = (ROOT / spec['binary']).read_bytes()
    original = raw[spec['address'] - spec['base']:spec['address'] - spec['base'] + spec['bytes']]
    if not refusal or link_attempt['exitCode'] != 0 or output.stat().st_size != spec['bytes'] or output.read_bytes() == original:
        raise ValueError('Actual successful wrong-C genuine link was not rejected by complete native-byte comparison')
    result = dict(generator=__file__, generatorSha256=sha256(__file__), sourceCredit=0, behaviorExecutionCredit=0,
        positiveWholeCExact=True, positiveRealLink=positive_link,
        wholeCNegativeControlsRejected=1, typedMutation='Measured MPACK callback state incremented by one',
        originalSourceUnchanged=sha256(ROOT / entry['source']) == entry['sourceSha256'],
        wrongSource=wrong.relative_to(ROOT).as_posix(), wrongSourceSha256=sha256(wrong),
        wrongCompilerResult=row, wrongRealLinkAttempt=link_attempt, wrongLinkRefusal=refusal,
        wrongGenuinelyLinkedBytes=output.stat().st_size, wrongLinkedSha256=sha256(output),
        originalNativeSha256=entry['targetSha256'],
        wrongLinkedMatchingBytes=sum(a == b for a, b in zip(output.read_bytes(), original)),
        nativeFunctionReturns=0, ordinaryFunctionCredit=0)
    write_json(LANE / 'whole-c-controls.json', result)
    print(dict(positiveWholeCExact=True, positiveGenuineLinkExact=True, wrongWholeCCompiled=True,
        wrongSameExtent=entry['bytes'], wrongRealLinkExitCode=0, wrongWholeCNativeGateRejected=True, executionCredit=0))


if __name__ == '__main__':
    main()
