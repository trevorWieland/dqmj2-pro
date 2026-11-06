from project import ROOT,sha256


def main():
    text=(ROOT/'validate_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('match_arm7_lane_initializer_20261031','match_arm7_lane_alarm_selector_20261031')
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-alarm-selector-20261031.json')
    text=text.replace('arm7-lane-initializer-controls-20261031.json','arm7-lane-alarm-selector-controls-20261031.json')
    text=text.replace('b71805001bd9cdcdad73c41c0c89fd270895be6cda43de719e802a537dd1ca51',sha256(ROOT/'match_arm7_lane_alarm_selector_20261031.py'))
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-native-helper-contracts-and-raw-mode-effects')
    text=text.replace("report.get('module') != 'arm7-wram'", "report.get('module') != 'arm7-main'")
    text=text.replace("report.get('matchedInitializedBytes') != 92 or report.get('matchedInstructionBytes') != 84 or report.get('generatedLiteralBytes') != 8", "report.get('matchedInitializedBytes') != 176 or report.get('matchedInstructionBytes') != 160 or report.get('generatedLiteralBytes') != 16")
    text=text.replace("report.get('actualNativeAndCompiledReturns') != 128 or report.get('actualSeparatelyObservedNestedReturns') != 0 or report.get('providerFreeOriginalAndCompiledReturns') != 128", "report.get('actualNativeAndCompiledReturns') != 640 or report.get('actualSeparatelyObservedNestedReturns') != 3584 or report.get('providerFreeOriginalAndCompiledReturns') != 640")
    text=text.replace("('missing-declared-includes', ('matches', 0, 'sourceDependencies'), [])", "('invented-declared-include', ('matches', 0, 'sourceDependencies'), [{'path':'invented.h','sha256':'0'*64}])")
    first=text.index("    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]",text.index('def main():'))
    last=text.index('    result = ',first)
    text=text[:first]+'''    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    mutations = (('wrong-first-mode', 'mode == 1', 'mode == 3'),
        ('wrong-second-mode', 'mode == 2', 'mode == 3'),
        ('wrong-context-first-word', 'context->value1c = 0;', 'context->value1c = 1;'),
        ('wrong-context-last-word', 'context->valued8 = 0;', 'context->valued8 = 1;'),
        ('wrong-registered-count', ', 203, 263,', ', 202, 263,'))
    for name, old, new in mutations:
        original = path(pin['source']).read_text()
        changed_text = original.replace(old,new)
        if changed_text == original:
            raise ValueError('Expected selector source mutation absent')
        directory = matcher.WORK/'controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source = directory/path(pin['source']).name
        source.write_text(changed_text)
        changed = dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()))
        reject('actual-compiler-link-rejects-'+name,lambda changed=changed:matcher.build(changed))
    native = matcher.fixture.fixture
    raw = path(pin['binary']).read_bytes()
    body = raw[native.ADDRESS-native.BASE:native.ADDRESS-native.BASE+native.SIZE]
    def require_return(value):
        if not value['states'][0]['actualReturn']:
            raise ValueError('Selector bounded execution did not actually return')
    reject('selector-exhaustion-is-not-return',lambda:require_return(native.execute(body,native.cases()[0],91,budget=1)))
    matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Selector positive proof not restored after controls')
'''+text[last:]
    text=text.replace("'matchedInitializedBytes': 92, 'actualOriginalAndCompiledReturns': 128", "'matchedInitializedBytes': 176, 'actualOriginalAndCompiledReturns': 640")
    text=text.replace("'actualSeparateNestedReturns': 0", "'actualSeparateNestedReturns': 3584")
    text=text.replace('Five independently compiled ordinary C field/count mutations; accepted inputs remain unchanged',
        'Five independently compiled ordinary C mode/field/registration mutations; accepted inputs remain unchanged')
    destination=ROOT/'validate_arm7_lane_alarm_selector_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace different selector validator')
    destination.write_text(text)
    print(dict(validatorSha256=sha256(destination)))


if __name__=='__main__':
    main()
