import json
import shutil
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    directory=ROOT/'src/arm7/lane_20261031_initializer'
    directory.mkdir(parents=True,exist_ok=True)
    source_root=ROOT/'nonmatching/arm7-bulk/20261030/lane-sdk-typed68-01/arm7-wram'
    for name in ('native_arm7_wram_037ff164.c','native_lane_channel_init_types.h','native_lane_player_types.h'):
        target=directory/name
        if target.exists() and target.read_bytes()!=(source_root/name).read_bytes():
            raise ValueError('Refusing to replace different promoted initializer source')
        shutil.copyfile(source_root/name,target)
    unit=json.loads((ROOT/'work/arm7-bulk-20261030/lane-sdk-typed68-01/arm7-wram/037ff164/result.json').read_text())
    entry=next(row['entry'] for row in unit['variants'] if row.get('realLink',{}).get('exactLinkedBytes'))
    fields=('name','program','processor','module','mode','address','bytes','binary','base','inputModuleSha256',
        'targetSha256','compiler','compilerSha256','compilerFlags')
    pin={key:entry[key] for key in fields}
    source=directory/Path(entry['source']).name
    pin.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),codeBytes=84,
        sourceDependencies=[dict(path=(directory/name).relative_to(ROOT).as_posix(),sha256=sha256(directory/name))
            for name in ('native_lane_channel_init_types.h','native_lane_player_types.h')])
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-initializer-final/closure.json'
    write_json(profile,dict(matches=[pin]))
    boundary=(ROOT/'arm7_lane_driver_leaves_boundaries_20261030.py').read_text()
    boundary=boundary.replace('expected_calls = {0x037FEA20: {}, 0x037FEAC0: {}}','expected_calls = {0x037FF164: {}}')
    boundary_path=ROOT/'arm7_lane_initializer_boundaries_20261031.py'
    if boundary_path.exists() and boundary_path.read_text()!=boundary:
        raise ValueError('Refusing to replace different initializer boundary source')
    boundary_path.write_text(boundary)
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261030/lane-driver-leaves-final68/generator-pins.json').read_text())['files']
    retained=[item for item in old if 'lane-driver-leaves-final68' not in item['path']
        and 'lane_20261030_driver_leaves68' not in item['path'] and not item['path'].startswith('arm7_lane_driver_leaves_')]
    new=['arm7_lane_initializer_native_20261031.py','arm7_lane_initializer_oracle_20261031.py',boundary_path.name,
        profile.relative_to(ROOT).as_posix(),*[path.relative_to(ROOT).as_posix() for path in directory.iterdir() if path.is_file()]]
    by={item['path']:item for item in retained}
    for name in new:
        by[name]=dict(path=name,sha256=sha256(ROOT/name))
    for item in by.values():
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Initializer runtime dependency differs')
    pins=profile.with_name('generator-pins.json')
    write_json(pins,dict(files=[by[name] for name in sorted(by)]))
    text=(ROOT/'match_arm7_lane_timing_20261031.py').read_text()
    text=text.replace('arm7_lane_timing_boundaries_20261031','arm7_lane_initializer_boundaries_20261031')
    text=text.replace('arm7_lane_timing_oracle_20261031','arm7_lane_initializer_oracle_20261031')
    text=text.replace('lane-timing-final','lane-initializer-final')
    text=text.replace('696c228b06306f846b3e2d99a5d6f010c0a86c84c4511385ec70fa90fe68df39',sha256(profile))
    text=text.replace('ff103158f9809ebfabe027089bbf8752bbe7afd315d45224c71270740f29ed89',sha256(pins))
    text=text.replace("implementationFamily='bounded-timer-calculation' if address == 0x037FECAC else 'sequence-skip-and-real-alarm-state'", "implementationFamily='channel-id-flags-and-mask-initialization'")
    text=text.replace('arm7-lane-timing-20261031.json','arm7-lane-initializer-20261031.json')
    matcher=ROOT/'match_arm7_lane_initializer_20261031.py'
    if matcher.exists() and matcher.read_text()!=text:
        raise ValueError('Refusing to replace different initializer matcher')
    matcher.write_text(text)
    print(dict(profileSha256=sha256(profile),pinsSha256=sha256(pins),matcherSha256=sha256(matcher),inputs=len(by)))


if __name__=='__main__':
    main()
