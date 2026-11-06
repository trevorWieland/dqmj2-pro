import json
import shutil
from pathlib import Path
from project import ROOT,sha256,write_json


def main():
    source_root=ROOT/'nonmatching/arm7-bulk/20261030/lane-sdk-typed68-01/arm7-wram'
    target=ROOT/'src/arm7/lane_20261031_timing'
    target.mkdir(parents=True,exist_ok=True)
    files=['native_arm7_wram_037fecac.c','native_arm7_wram_03800414.c','native_lane_sdk_types.h','native_lane_player_types.h']
    for name in files:
        destination=target/name
        if destination.exists() and destination.read_bytes()!=(source_root/name).read_bytes():
            raise ValueError('Refusing to replace a different promoted source')
        shutil.copyfile(source_root/name,destination)
    original=json.loads((ROOT/'work/arm7-bulk-20261030/lane-sdk-typed68-01/results.json').read_text())['results']
    pins=[]
    for address,code in ((0x037FECAC,284),(0x03800414,196)):
        unit=next(row for row in original if int(row['address'],0)==address)
        row=next(row for row in unit['variants'] if row.get('realLink',{}).get('exactLinkedBytes'))
        entry=row['entry']
        fields=('name','program','processor','module','mode','address','bytes','binary','base','inputModuleSha256',
            'targetSha256','compiler','compilerSha256','compilerFlags')
        pin={key:entry[key] for key in fields}
        source=target/Path(entry['source']).name
        pin.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),codeBytes=code,
            sourceDependencies=[dict(path=(target/name).relative_to(ROOT).as_posix(),sha256=sha256(target/name))
                for name in ('native_lane_player_types.h','native_lane_sdk_types.h')])
        pins.append(pin)
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-timing-final/closure.json'
    write_json(profile,dict(matches=pins))
    old=json.loads((ROOT/'nonmatching/arm7-bulk/20261030/lane-driver-leaves-final68/generator-pins.json').read_text())['files']
    retained=[item for item in old if 'lane-driver-leaves-final68' not in item['path']
        and 'lane_20261030_driver_leaves68' not in item['path'] and not item['path'].startswith('arm7_lane_driver_leaves_')]
    new=['arm7_lane_calc_timer_native_20261030.py','arm7_lane_skip_native_20261031.py',
        'arm7_lane_timing_oracle_20261031.py','arm7_lane_timing_boundaries_20261031.py',profile.relative_to(ROOT).as_posix(),
        *[path.relative_to(ROOT).as_posix() for path in target.iterdir() if path.is_file()]]
    by={item['path']:item for item in retained}
    for name in new:
        by[name]=dict(path=name,sha256=sha256(ROOT/name))
    for item in by.values():
        if sha256(ROOT/item['path'])!=item['sha256']:
            raise ValueError('Retained runtime dependency differs')
    destination=profile.with_name('generator-pins.json')
    write_json(destination,dict(files=[by[name] for name in sorted(by)]))
    print(dict(profileSha256=sha256(profile),pinsSha256=sha256(destination),inputs=len(by)))


if __name__=='__main__':
    main()
