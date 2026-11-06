from project import ROOT,sha256


def main():
    text=(ROOT/'validate_arm7_lane_driver_leaves_20261030.py').read_text()
    text=text.replace('match_arm7_lane_driver_leaves_20261030','match_arm7_lane_timing_20261031')
    text=text.replace('arm7-lane-driver-leaves-20261030.json','arm7-lane-timing-20261031.json')
    text=text.replace('arm7-lane-driver-leaves-controls-20261030.json','arm7-lane-timing-controls-20261031.json')
    text=text.replace('39933a1fb8e81733c98699ed8a53c618fe85b34dbc6f0d7944342b2fe2306b16',sha256(ROOT/'match_arm7_lane_timing_20261031.py'))
    text=text.replace('measured-native-driver-cpu-behavior','local-SDK-correspondence-plus-independent-native-contracts')
    text=text.replace("report.get('matchedInitializedBytes') != 64 or report.get('matchedInstructionBytes') != 64 or report.get('generatedLiteralBytes') != 0", "report.get('matchedInitializedBytes') != 492 or report.get('matchedInstructionBytes') != 480 or report.get('generatedLiteralBytes') != 12")
    text=text.replace("report.get('actualNativeAndCompiledReturns') != 2048 or report.get('actualSeparatelyObservedNestedReturns') != 0 or report.get('providerFreeOriginalAndCompiledReturns') != 2048 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0", "report.get('actualNativeAndCompiledReturns') != 1620 or report.get('actualSeparatelyObservedNestedReturns') != 57366 or report.get('providerFreeOriginalAndCompiledReturns') != 684 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 936")
    first=text.index('    pin = copy.deepcopy(')
    last=text.index('    result = ',first)
    text=text[:first]+'''    pins = json.loads(matcher.PROFILE.read_text())['matches']
    mutations = ((0, 'narrowed-64bit-product', 'u64 result =', 'u32 result ='),
        (0, 'lost-signed-timer-extension', 'result *= timer;', 'result *= (u32)timer;'),
        (0, 'wrong-pitch-normalization', '768', '769'),
        (1, 'wrong-release-argument', 'trk, ply, 127', 'trk, ply, 126'),
        (1, 'counter-off-by-one', 'counter += i;', 'counter += i + 1;'))
    for index, name, old, new in mutations:
        pin = copy.deepcopy(pins[index])
        original = path(pin['source']).read_text()
        changed_text = original.replace(old,new)
        if changed_text == original:
            raise ValueError('Expected source mutation expression absent')
        directory = matcher.WORK/'controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source = directory/path(pin['source']).name
        source.write_text(changed_text)
        dependencies = []
        for item in pin['sourceDependencies']:
            header = directory/path(item['path']).name
            header.write_bytes(path(item['path']).read_bytes())
            dependencies.append(dict(path=header.relative_to(ROOT).as_posix(),sha256=digest(header.read_bytes())))
        changed = dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()),sourceDependencies=dependencies)
        reject('actual-compiler-link-rejects-'+name,lambda changed=changed: matcher.build(changed))
    timer = matcher.fixture.timer
    skip = matcher.fixture.skip
    raw = path(pins[0]['binary']).read_bytes()
    timer_body = raw[timer.ADDRESS-timer.BASE:timer.ADDRESS-timer.BASE+timer.SIZE]
    skip_body = raw[skip.ADDRESS-skip.BASE:skip.ADDRESS-skip.BASE+skip.SIZE]
    def require_return(value):
        if not value.get('states',[value])[0]['actualReturn']:
            raise ValueError('Bounded timing execution did not actually return')
    reject('timer-exhaustion-is-not-return',lambda:require_return(timer.execute(timer_body,timer.cases()[0],91,budget=1)))
    reject('missing-bios-is-not-return',lambda:require_return(timer.execute(timer_body,dict(timer.cases()[0],service=None),91)))
    reject('unqualified-bios-output-word',lambda:timer.execute(timer_body,dict(timer.cases()[0],service=65536),91))
    reject('undefined-source-shift-domain',lambda:timer.expected(dict(timer=1,pitch=49152,service=0)))
    reject('skip-exhaustion-is-not-return',lambda:require_return(skip.execute(skip_body,skip.cases()[0],91,budget=1)))
    for pin in pins:
        matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Timing positive proof not restored after controls')
'''+text[last:]
    text=text.replace("'matchedInitializedBytes': 64, 'actualOriginalAndCompiledReturns': 2048", "'matchedInitializedBytes': 492, 'actualOriginalAndCompiledReturns': 1620")
    text=text.replace("'actualSeparateNestedReturns': 0", "'actualSeparateNestedReturns': 57366")
    text=text.replace('Five independently compiled ordinary C logic and hardware-slot mutations; accepted inputs remain unchanged','Five independently compiled ordinary C arithmetic and ordered-call mutations; accepted inputs remain unchanged')
    destination=ROOT/'validate_arm7_lane_timing_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace a different timing validator')
    destination.write_text(text)
    print(dict(validatorSha256=sha256(destination)))


if __name__=='__main__':
    main()
