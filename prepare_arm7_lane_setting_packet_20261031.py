import json
import shutil
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    target=ROOT/'src/arm7/lane_20261031_setting'
    target.mkdir(parents=True,exist_ok=True)
    source_root=ROOT/'nonmatching/arm7-bulk/20261031/lane-main-setting'
    for name in ('native_arm7_main_027e8ec8.c','native_setting_types.h'):
        destination=target/name
        if destination.exists() and destination.read_bytes()!=(source_root/name).read_bytes():
            raise ValueError('Refusing to replace different promoted setting source')
        shutil.copyfile(source_root/name,destination)
    original=json.loads((ROOT/'work/arm7-bulk-20261030/lane-main-setting-qualified/027e8ec8/report.json').read_text())['entry']
    fields=('name','program','processor','module','mode','address','bytes','binary','base','inputModuleSha256',
        'targetSha256','compiler','compilerSha256','compilerFlags','runtimePointerQualification')
    pin={key:original[key] for key in fields}
    pin.update(source=(target/Path(original['source']).name).relative_to(ROOT).as_posix(),
        sourceSha256=sha256(target/Path(original['source']).name),codeBytes=44,
        sourceDependencies=[dict(path=(target/'native_setting_types.h').relative_to(ROOT).as_posix(),sha256=sha256(target/'native_setting_types.h'))])
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-setting-final/closure.json'
    write_json(profile,dict(matches=[pin]))
    text=(ROOT/'arm7_lane_initializer_boundaries_20261031.py').read_text()
    text=text.replace('expected_calls = {0x037FF164: {}}','expected_calls = {0x027E8EC8: {}}')
    boundary=ROOT/'arm7_lane_setting_boundaries_20261031.py'
    if boundary.exists() and boundary.read_text()!=text:
        raise ValueError('Refusing to replace different setting boundary source')
    boundary.write_text(text)
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-initializer-final/generator-pins.json').read_text())['files']
    retained=[item for item in old if 'lane-initializer-final' not in item['path'] and 'lane_20261031_initializer' not in item['path']
        and not item['path'].startswith('arm7_lane_initializer_')]
    new=['arm7_lane_setting_native_20261031.py','arm7_lane_setting_oracle_20261031.py','arm7_lane_setting_boundaries_20261031.py',
        'prove_arm7_lane_setting_producer_20261031.py','evidence/attempts/arm7-lane-setting-producer-20261031.json',
        'link_arm7_runtime_pointer_20261031.py',profile.relative_to(ROOT).as_posix(),
        *[path.relative_to(ROOT).as_posix() for path in target.iterdir() if path.is_file()]]
    by={item['path']:item for item in retained}
    for name in new:
        by[name]=dict(path=name,sha256=sha256(ROOT/name))
    for item in by.values():
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Setting runtime dependency differs')
    pins=profile.with_name('generator-pins.json')
    write_json(pins,dict(files=[by[name] for name in sorted(by)]))
    text=(ROOT/'match_arm7_lane_initializer_20261031.py').read_text()
    text=text.replace('import link_arm7_bulk_20261030 as linker','import link_arm7_runtime_pointer_20261031 as linker\nimport prove_arm7_lane_setting_producer_20261031 as producer')
    text=text.replace('arm7_lane_initializer_boundaries_20261031','arm7_lane_setting_boundaries_20261031')
    text=text.replace('arm7_lane_initializer_oracle_20261031','arm7_lane_setting_oracle_20261031')
    text=text.replace('lane-initializer-final','lane-setting-final')
    text=text.replace('e8005734c929f7f4a2476b42044647b8d52a2a521c9811586dfc0a186cd6453e',sha256(profile))
    text=text.replace('797c6158533f9a507cbe6a1bff3859707520df0d99738c5898acf025d2b187fe',sha256(pins))
    text=text.replace("sourceLanguage='C99'","sourceLanguage='C'")
    text=text.replace('local-SDK-correspondence-plus-independent-native-contracts','measured-native-instruction-and-pointer-producer-contracts')
    text=text.replace("implementationFamily='channel-id-flags-and-mask-initialization'", "implementationFamily='bounded-byte-setting-through-produced-runtime-pointer'")
    text=text.replace("'module': 'arm7-wram'", "'module': 'arm7-main'")
    text=text.replace('arm7-lane-initializer-20261031.json','arm7-lane-setting-20261031.json')
    text=text.replace('    import unicorn\n', '    producer.main()\n    import unicorn\n')
    matcher=ROOT/'match_arm7_lane_setting_20261031.py'
    if matcher.exists() and matcher.read_text()!=text:
        raise ValueError('Refusing to replace different setting matcher')
    matcher.write_text(text)
    print(dict(profileSha256=sha256(profile),pinsSha256=sha256(pins),matcherSha256=sha256(matcher),inputs=len(by)))


if __name__=='__main__':
    main()
