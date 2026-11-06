import json
import shutil
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    target=ROOT/'src/arm7/lane_20261031_alarm_selector'
    target.mkdir(parents=True,exist_ok=True)
    name='native_arm7_main_027e5bac.c'
    original=ROOT/'nonmatching/arm7-bulk/20261031/lane-main-alarm-selector'/name
    if (target/name).exists() and (target/name).read_bytes()!=original.read_bytes():
        raise ValueError('Refusing to replace different promoted selector source')
    shutil.copyfile(original,target/name)
    entry=json.loads((ROOT/'work/arm7-bulk-20261030/lane-main-alarm-selector-base/027e5bac/report.json').read_text())['entry']
    fields=('name','program','processor','module','mode','address','bytes','binary','base','inputModuleSha256',
        'targetSha256','compiler','compilerSha256','compilerFlags')
    pin={key:entry[key] for key in fields}
    pin.update(source=(target/name).relative_to(ROOT).as_posix(),sourceSha256=sha256(target/name),codeBytes=160,sourceDependencies=[])
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-alarm-selector-final/closure.json'
    write_json(profile,dict(matches=[pin]))
    text=(ROOT/'arm7_lane_initializer_boundaries_20261031.py').read_text()
    text=text.replace('expected_calls = {0x037FF164: {}}','expected_calls = {0x027E5BAC: {0x027E5BD8:0x037FDA38,0x027E5BF4:0x037FD898,0x027E5C18:0x037FDA38,0x027E5C34:0x037FD898}}')
    boundary=ROOT/'arm7_lane_alarm_selector_boundaries_20261031.py'
    if boundary.exists() and boundary.read_text()!=text:
        raise ValueError('Refusing to replace different selector boundary source')
    boundary.write_text(text)
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-initializer-final/generator-pins.json').read_text())['files']
    retained=[item for item in old if 'lane-initializer-final' not in item['path'] and 'lane_20261031_initializer' not in item['path']
        and not item['path'].startswith('arm7_lane_initializer_')]
    new=['arm7_lane_alarm_selector_native_20261031.py','arm7_lane_alarm_selector_oracle_20261031.py',boundary.name,
        'arm7_lane_skip_native_20261031.py',profile.relative_to(ROOT).as_posix(),(target/name).relative_to(ROOT).as_posix(),
        'src/arm7/20261029rotated30/native_arm7_wram_037fd898.c','src/arm7/translated04/native_arm7_wram_037fda38.c']
    by={item['path']:item for item in retained}
    for value in new:
        by[value]=dict(path=value,sha256=sha256(ROOT/value))
    for item in by.values():
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Selector runtime dependency differs')
    pins=profile.with_name('generator-pins.json')
    write_json(pins,dict(files=[by[value] for value in sorted(by)]))
    text=(ROOT/'match_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('arm7_lane_initializer_boundaries_20261031','arm7_lane_alarm_selector_boundaries_20261031')
    text=text.replace('arm7_lane_initializer_oracle_20261031','arm7_lane_alarm_selector_oracle_20261031')
    text=text.replace('lane-initializer-final','lane-alarm-selector-final')
    text=text.replace('e8005734c929f7f4a2476b42044647b8d52a2a521c9811586dfc0a186cd6453e',sha256(profile))
    text=text.replace('797c6158533f9a507cbe6a1bff3859707520df0d99738c5898acf025d2b187fe',sha256(pins))
    text=text.replace("implementationFamily='channel-id-flags-and-mask-initialization'", "implementationFamily='raw-mode-context-and-native-alarm-registration'")
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-native-helper-contracts-and-raw-mode-effects')
    text=text.replace("'module': 'arm7-wram'", "'module': 'arm7-main'")
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-alarm-selector-20261031.json')
    matcher=ROOT/'match_arm7_lane_alarm_selector_20261031.py'
    if matcher.exists() and matcher.read_text()!=text:
        raise ValueError('Refusing to replace different selector matcher')
    matcher.write_text(text)
    print(dict(profileSha256=sha256(profile),pinsSha256=sha256(pins),matcherSha256=sha256(matcher),inputs=len(by)))


if __name__=='__main__':
    main()
