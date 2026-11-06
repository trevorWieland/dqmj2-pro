from project import ROOT,sha256


def main():
    text=(ROOT/'validate_arm7_lane_timing_20261031.py').read_text()
    text=text.replace('match_arm7_lane_timing_20261031','match_arm7_lane_initializer_20261031')
    text=text.replace('arm7-lane-timing-20261031.json','arm7-lane-initializer-20261031.json')
    text=text.replace('arm7-lane-timing-controls-20261031.json','arm7-lane-initializer-controls-20261031.json')
    text=text.replace('5933d5ba08b5e99368e1944377f7c6b0031316c6e2e5caa1878bb7d003d21a7c',sha256(ROOT/'match_arm7_lane_initializer_20261031.py'))
    text=text.replace("report.get('matchedInitializedBytes') != 492 or report.get('matchedInstructionBytes') != 480 or report.get('generatedLiteralBytes') != 12", "report.get('matchedInitializedBytes') != 92 or report.get('matchedInstructionBytes') != 84 or report.get('generatedLiteralBytes') != 8")
    text=text.replace("report.get('actualNativeAndCompiledReturns') != 1620 or report.get('actualSeparatelyObservedNestedReturns') != 57366 or report.get('providerFreeOriginalAndCompiledReturns') != 684 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 936", "report.get('actualNativeAndCompiledReturns') != 128 or report.get('actualSeparatelyObservedNestedReturns') != 0 or report.get('providerFreeOriginalAndCompiledReturns') != 128 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0")
    text=text.replace('if len(rows) != 2:', 'if len(rows) != 1:')
    first=text.index("    pins = json.loads(matcher.PROFILE.read_text())['matches']",text.index('def main():'))
    last=text.index('    result = ',first)
    text=text[:first]+'''    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    mutations = (('missing-last-channel', 'i < 16', 'i < 15'),
        ('wrong-active-reset', 'chn->flags.active = 0;', 'chn->flags.active = 1;'),
        ('wrong-sync-reset', 'chn->flags.syncFlag = 0;', 'chn->flags.syncFlag = 1;'),
        ('wrong-mask-reset', '[1] = 0;', '[1] = 1;'),
        ('wrong-id', 'chn->id = (u8)i;', 'chn->id = (u8)(i + 1);'))
    for name, old, new in mutations:
        original = path(pin['source']).read_text()
        changed_text = original.replace(old,new)
        if changed_text == original:
            raise ValueError('Expected initializer source mutation absent')
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
        reject('actual-compiler-link-rejects-'+name,lambda changed=changed:matcher.build(changed))
    native = matcher.fixture.fixture
    raw = path(pin['binary']).read_bytes()
    body = raw[native.ADDRESS-native.BASE:native.ADDRESS-native.BASE+native.SIZE]
    def require_return(value):
        if not value['states'][0]['actualReturn']:
            raise ValueError('Initializer bounded execution did not actually return')
    reject('initializer-exhaustion-is-not-return',lambda:require_return(native.execute(body,native.cases()[0],91,budget=1)))
    matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Initializer positive proof not restored after controls')
'''+text[last:]
    text=text.replace("'matchedInitializedBytes': 492, 'actualOriginalAndCompiledReturns': 1620", "'matchedInitializedBytes': 92, 'actualOriginalAndCompiledReturns': 128")
    text=text.replace("'actualSeparateNestedReturns': 57366", "'actualSeparateNestedReturns': 0")
    text=text.replace('Five independently compiled ordinary C arithmetic and ordered-call mutations; accepted inputs remain unchanged',
        'Five independently compiled ordinary C field/count mutations; accepted inputs remain unchanged')
    destination=ROOT/'validate_arm7_lane_initializer_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace different initializer validator')
    destination.write_text(text)
    print(dict(validatorSha256=sha256(destination)))


if __name__=='__main__':
    main()
