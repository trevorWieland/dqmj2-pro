from project import ROOT,sha256


def main():
    text=(ROOT/'validate_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('match_arm7_lane_initializer_20261031','match_arm7_lane_setting_20261031')
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-setting-20261031.json')
    text=text.replace('arm7-lane-initializer-controls-20261031.json','arm7-lane-setting-controls-20261031.json')
    text=text.replace('b71805001bd9cdcdad73c41c0c89fd270895be6cda43de719e802a537dd1ca51',sha256(ROOT/'match_arm7_lane_setting_20261031.py'))
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-native-instruction-and-pointer-producer-contracts')
    text=text.replace("report.get('module') != 'arm7-wram'", "report.get('module') != 'arm7-main'")
    text=text.replace("report.get('matchedInitializedBytes') != 92 or report.get('matchedInstructionBytes') != 84", "report.get('matchedInitializedBytes') != 52 or report.get('matchedInstructionBytes') != 44")
    text=text.replace("report.get('actualNativeAndCompiledReturns') != 128", "report.get('actualNativeAndCompiledReturns') != 2120")
    text=text.replace("report.get('providerFreeOriginalAndCompiledReturns') != 128", "report.get('providerFreeOriginalAndCompiledReturns') != 2120")
    first=text.index("    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]",text.index('def main():'))
    last=text.index('    result = ',first)
    text=text[:first]+'''    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    mutations = (('wrong-byte-domain', 'value > 255', 'value > 254'),
        ('wrong-return-word', 'return 5;', 'return 4;'),
        ('wrong-ram-value', '= (s16)value;', '= (s16)(value + 1);'),
        ('wrong-mmio-value', '= (u16)value;', '= (u16)(value + 1);'),
        ('reversed-store-order',
            '    native_host_arm7_data_0380fff4->value = (s16)value;\\n    native_host_arm7_data_0480802c = (u16)value;',
            '    native_host_arm7_data_0480802c = (u16)value;\\n    native_host_arm7_data_0380fff4->value = (s16)value;'))
    for name, old, new in mutations:
        original = path(pin['source']).read_text()
        changed_text = original.replace(old,new)
        if changed_text == original:
            raise ValueError('Expected setting source mutation absent')
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
    import link_arm7_bulk_20261030 as baseline
    modules, unused = baseline.namespace('')
    reject('original-policy-refusal-preserved',lambda:baseline.data_binding(pin,0x0380FFF4,modules))
    reject('unknown-neighbor-pointer-still-rejected',lambda:matcher.linker.data_binding(pin,0x0380FFF8,modules))
    for name, key, value in (('wrong-policy-program','program','dwc/utility.bin/move/child.srl'),
        ('wrong-policy-module','module','arm7-wram'),('wrong-policy-mode','mode','thumb'),
        ('wrong-policy-caller','address','0x27e8ecc'),('wrong-policy-size','bytes',56)):
        changed = dict(pin,**{key:value})
        reject(name,lambda changed=changed:matcher.linker.data_binding(changed,0x0380FFF4,modules))
    for name, value in (('missing-pointer-producer',None),('wrong-storage-word-width',dict(pin['runtimePointerQualification'],storageBytes=8)),
        ('changed-producer-hash',dict(pin['runtimePointerQualification'],sha256='0'*64))):
        changed = dict(pin,runtimePointerQualification=value)
        reject(name,lambda changed=changed:matcher.linker.data_binding(changed,0x0380FFF4,modules))
    native = matcher.fixture.fixture
    raw = path(pin['binary']).read_bytes()
    body = raw[native.ADDRESS-native.BASE:native.ADDRESS-native.BASE+native.SIZE]
    def require_return(value):
        if not value['states'][0]['actualReturn']:
            raise ValueError('Setting bounded execution did not actually return')
    reject('setting-exhaustion-is-not-return',lambda:require_return(native.execute(body,native.cases()[0],91,budget=1)))
    reject('null-pointer-valid-input-is-unsupported',lambda:require_return(native.execute(body,dict(value=1,pointer=0,passes=1),91)))
    matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Setting positive proof not restored after controls')
'''+text[last:]
    text=text.replace("'matchedInitializedBytes': 92, 'actualOriginalAndCompiledReturns': 128", "'matchedInitializedBytes': 52, 'actualOriginalAndCompiledReturns': 2120")
    text=text.replace('Five independently compiled ordinary C field/count mutations; accepted inputs remain unchanged',
        'Five independently compiled ordinary C guard/value/order mutations plus narrow runtime-pointer policy controls; accepted inputs remain unchanged')
    destination=ROOT/'validate_arm7_lane_setting_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace different setting validator')
    destination.write_text(text)
    print(dict(validatorSha256=sha256(destination)))


if __name__=='__main__':
    main()
