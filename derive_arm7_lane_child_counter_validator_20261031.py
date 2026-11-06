from project import ROOT,sha256


def main():
    text=(ROOT/'validate_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('match_arm7_lane_initializer_20261031','match_arm7_lane_child_counter_20261031')
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-child-counter-20261031.json')
    text=text.replace('arm7-lane-initializer-controls-20261031.json','arm7-lane-child-counter-controls-20261031.json')
    text=text.replace('b71805001bd9cdcdad73c41c0c89fd270895be6cda43de719e802a537dd1ca51',sha256(ROOT/'match_arm7_lane_child_counter_20261031.py'))
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-utility-native-counter-and-CPSR-contracts')
    text=text.replace("report.get('program') != '' or report.get('module') != 'arm7-wram'", "report.get('program') != matcher.utility_runtime.PROGRAM or report.get('module') != 'utility-child-arm7-wram'")
    text=text.replace("report.get('matchedInitializedBytes') != 92 or report.get('matchedInstructionBytes') != 84", "report.get('matchedInitializedBytes') != 76 or report.get('matchedInstructionBytes') != 68")
    text=text.replace("report.get('actualNativeAndCompiledReturns') != 128 or report.get('actualSeparatelyObservedNestedReturns') != 0 or report.get('providerFreeOriginalAndCompiledReturns') != 128", "report.get('actualNativeAndCompiledReturns') != 2048 or report.get('actualSeparatelyObservedNestedReturns') != 4096 or report.get('providerFreeOriginalAndCompiledReturns') != 2048")
    text=text.replace("('missing-declared-includes', ('matches', 0, 'sourceDependencies'), [])", "('invented-declared-include', ('matches', 0, 'sourceDependencies'), [{'path':'invented.h','sha256':'0'*64}])")
    text=text.replace("return {('arm7', '', 'arm7-wram', row['address'], 'arm'): row for row in rows}",
        "return {(row['processor'], row.get('program',''), row['module'], row['address'], row['mode']): row for row in rows}")
    first=text.index("    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]",text.index('def main():'))
    last=text.index('    result = ',first)
    text=text[:first]+'''    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    mutations = (('incorrect-equality-step', 'sample < native_utility_child_arm7_data_03805b78', 'sample <= native_utility_child_arm7_data_03805b78'),
        ('unsigned-order-instead-of-signed', 'sample < native_utility_child_arm7_data_03805b78', '(u32)sample < (u32)native_utility_child_arm7_data_03805b78'),
        ('wrong-increment', 'native_utility_child_arm7_data_03805b7c++;', 'native_utility_child_arm7_data_03805b7c += 2;'),
        ('wrong-irq-restoration', '037fe430(interrupts);', '037fe430(0);'),
        ('wrong-counter-result', 'return native_utility_child_arm7_data_03805b7c;', 'return 0;'))
    for name, old, new in mutations:
        original = path(pin['source']).read_text()
        changed_text = original.replace(old,new)
        if changed_text == original:
            raise ValueError('Expected child counter source mutation absent')
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
            raise ValueError('Child counter bounded execution did not actually return')
    reject('counter-exhaustion-is-not-return',lambda:require_return(native.execute(body,native.cases()[0],91,budget=1)))
    matcher.build(pin)
    expected_identity = ('arm7',matcher.utility_runtime.PROGRAM,'utility-child-arm7-wram',pin['address'],'arm')
    if set(validate(report)) != {expected_identity}:
        raise ValueError('Qualified utility-child counter identity differs')
'''+text[last:]
    text=text.replace("'matchedInitializedBytes': 92, 'actualOriginalAndCompiledReturns': 128", "'matchedInitializedBytes': 76, 'actualOriginalAndCompiledReturns': 2048")
    text=text.replace("'actualSeparateNestedReturns': 0", "'actualSeparateNestedReturns': 4096")
    text=text.replace('Five independently compiled ordinary C field/count mutations; accepted inputs remain unchanged',
        'Five independently compiled ordinary C equality/signedness/increment/IRQ/result mutations; accepted inputs remain unchanged')
    destination=ROOT/'validate_arm7_lane_child_counter_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace different child counter validator')
    destination.write_text(text)
    print(dict(validatorSha256=sha256(destination)))


if __name__=='__main__':
    main()
