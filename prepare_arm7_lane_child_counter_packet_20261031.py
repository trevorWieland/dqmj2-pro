import json
import shutil
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    target=ROOT/'src/arm7/lane_20261031_child_counter'
    target.mkdir(parents=True,exist_ok=True)
    name='native_utility_child_arm7_wram_037fddcc.c'
    source=ROOT/'nonmatching/arm7-bulk/20261031/lane-child-counter76'/name
    if (target/name).exists() and (target/name).read_bytes()!=source.read_bytes():
        raise ValueError('Refusing to replace different promoted child counter source')
    shutil.copyfile(source,target/name)
    entry=json.loads((ROOT/'work/arm7-bulk-20261030/lane-child-counter76/037fddcc/report.json').read_text())['entry']
    fields=('name','program','processor','module','mode','address','bytes','binary','base','inputModuleSha256',
        'targetSha256','compiler','compilerSha256','compilerFlags')
    pin={key:entry[key] for key in fields}
    pin.update(source=(target/name).relative_to(ROOT).as_posix(),sourceSha256=sha256(target/name),codeBytes=68,sourceDependencies=[])
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-child-counter-final/closure.json'
    write_json(profile,dict(matches=[pin]))
    text=(ROOT/'arm7_lane_initializer_boundaries_20261031.py').read_text()
    text=text.replace('evidence/arm7/ghidra-runtime-inventory.json','evidence/utility/ghidra-arm7.json')
    text=text.replace('expected_calls = {0x037FF164: {}}','expected_calls = {0x037FDDCC: {0x037FDDD4:0x037FE41C,0x037FDDFC:0x037FE430}}')
    boundary=ROOT/'arm7_lane_child_counter_boundaries_20261031.py'
    if boundary.exists() and boundary.read_text()!=text:
        raise ValueError('Refusing to replace different child counter boundary source')
    boundary.write_text(text)
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-initializer-final/generator-pins.json').read_text())['files']
    retained=[item for item in old if 'lane-initializer-final' not in item['path'] and 'lane_20261031_initializer' not in item['path']
        and not item['path'].startswith('arm7_lane_initializer_')]
    new=['arm7_lane_child_counter_native_20261031.py','arm7_lane_child_counter_oracle_20261031.py',boundary.name,
        profile.relative_to(ROOT).as_posix(),(target/name).relative_to(ROOT).as_posix(),'evidence/utility/ghidra-arm7.json']
    by={item['path']:item for item in retained}
    for value in new:
        by[value]=dict(path=value,sha256=sha256(ROOT/value))
    for item in by.values():
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Child counter runtime dependency differs')
    pins=profile.with_name('generator-pins.json')
    write_json(pins,dict(files=[by[value] for value in sorted(by)]))
    text=(ROOT/'match_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('import arm7_runtime','import arm7_runtime\nimport utility_runtime')
    text=text.replace('arm7_lane_initializer_boundaries_20261031','arm7_lane_child_counter_boundaries_20261031')
    text=text.replace('arm7_lane_initializer_oracle_20261031','arm7_lane_child_counter_oracle_20261031')
    text=text.replace('lane-initializer-final','lane-child-counter-final')
    text=text.replace('e8005734c929f7f4a2476b42044647b8d52a2a521c9811586dfc0a186cd6453e',sha256(profile))
    text=text.replace('797c6158533f9a507cbe6a1bff3859707520df0d99738c5898acf025d2b187fe',sha256(pins))
    text=text.replace("layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())", 'layout, unused = utility_runtime.derive()')
    text=text.replace("sourceLanguage='C99'","sourceLanguage='C'")
    text=text.replace("implementationFamily='channel-id-flags-and-mask-initialization'", "implementationFamily='signed-sample-comparison-and-wrapping-counter'")
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-utility-native-counter-and-CPSR-contracts')
    text=text.replace("'program': '', 'module': 'arm7-wram'", "'program': utility_runtime.PROGRAM, 'module': 'utility-child-arm7-wram'")
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-child-counter-20261031.json')
    matcher=ROOT/'match_arm7_lane_child_counter_20261031.py'
    if matcher.exists() and matcher.read_text()!=text:
        raise ValueError('Refusing to replace different child counter matcher')
    matcher.write_text(text)
    print(dict(profileSha256=sha256(profile),pinsSha256=sha256(pins),matcherSha256=sha256(matcher),inputs=len(by)))


if __name__=='__main__':
    main()
