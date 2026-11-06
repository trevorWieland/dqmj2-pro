import json
import re
import shutil
from pathlib import Path
import match_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_GRP_CALL
from project import ROOT,sha256,write_json


def main():
    results=json.loads((ROOT/'work/arm7-bulk-20261030/lane-card-init188-v5/report.json').read_text())['results']
    folder=ROOT/'src/arm7/lane_20261031_card_init188'
    export=ROOT/'evidence/verification/accepted-cohort80-identities-20261031.json'
    accepted=json.loads(export.read_text())['functions']
    pins,calls=[],{}
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    decoder.detail=True
    for address,level in ((0x03802624,2),):
        result=next(row for row in results if int(str(row['address']),0)==address)
        selected=next(row for row in result['outcomes'] if row['compilerFlags'][0]=='-O'+str(level)
            and '/base/' in row['compiler'] and row.get('realLink',{}).get('exactLinkedBytes'))
        entry=selected['entry']
        if any(row['processor']=='arm7' and not row['program'] and row['module']=='arm7-wram'
            and int(str(row['address']),0)<address+entry['bytes'] and address<int(str(row['address']),0)+row['bytes'] for row in accepted):
            raise ValueError('Message source overlaps current accepted export')
        unit=folder/f'{address:08x}'
        unit.mkdir(parents=True,exist_ok=True)
        source=unit/Path(entry['source']).name
        for old,new in ((ROOT/entry['source'],source),(ROOT/entry['sourceDependencies'][0]['path'],unit/'native_card_service_types.h')):
            if new.exists() and new.read_bytes()!=old.read_bytes():
                raise ValueError('Refusing to mutate promoted message source closure')
            shutil.copy2(old,new)
        pin={key:entry[key] for key in ('name','program','processor','module','mode','address','bytes','binary','base',
            'inputModuleSha256','targetSha256','compiler','compilerSha256','compilerFlags')}
        pin.update(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),codeBytes=164,
            sourceDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p)) for p in unit.glob('*.h')])
        pins.append(pin)
        raw=(ROOT/pin['binary']).read_bytes()[address-pin['base']:address-pin['base']+pin['bytes']]
        calls[address]={instruction.address:instruction.operands[0].imm for instruction in decoder.disasm(raw,address) if instruction.group(CS_GRP_CALL)}
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-card-init188-final/closure.json'
    write_json(profile,dict(matches=pins,acceptedIdentityExport=dict(path=export.relative_to(ROOT).as_posix(),sha256=sha256(export),overlap=False),
        sourceCredit=0,profileScope='Base O2/space only for these measured periodic-registration unit'))
    boundary=(ROOT/'arm7_lane_channel_five_boundaries_20261031.py').read_text()
    first,last=boundary.index('    expected_calls = '),boundary.index('    if {row.address:')
    boundary=boundary[:first]+'    expected_calls = '+repr(calls)+'\n'+boundary[last:]
    (ROOT/'arm7_lane_card_init_boundaries_20261031.py').write_text(boundary)
    previous=ROOT/'nonmatching/arm7-bulk/20261031/lane-scheduler212-final/generator-pins.json'
    paths={row['path'] for row in json.loads(previous.read_text())['files'] if not row['path'].startswith('arm7_lane_mmio_pair_')}
    paths.update(['arm7_lane_card_init_boundaries_20261031.py','arm7_lane_card_init_native_20261031.py',
        'arm7_lane_card_init_oracle_20261031.py','arm7_lane_heap_engine_20261031.py'])
    generator_pins=profile.with_name('generator-pins.json')
    write_json(generator_pins,dict(files=[dict(path=name,sha256=sha256(ROOT/name)) for name in sorted(paths)],
        limitation='Explicit local closure; frozen list model import and original helper calls add no reconstructed-source credit'))
    matcher=(ROOT/'match_arm7_lane_mmio_pair_20261031.py').read_text()
    matcher=matcher.replace('arm7_lane_mmio_pair','arm7_lane_card_init').replace('lane-mmio-pair-final','lane-card-init188-final')
    matcher=matcher.replace('arm7-lane-mmio-pair136','arm7-lane-card-init188')
    matcher=matcher.replace('typed-capture-and-output-full-word-mmio-writers','common-state-thread-and-callback-initialization')
    matcher=matcher.replace('verified-public-sdk-enum-types-and-measured-mmio-contracts','native-card-common-layout-and-reference-qualifiers')
    matcher=re.sub(r"PROFILE_SHA = '[0-9a-f]+'","PROFILE_SHA = '"+sha256(profile)+"'",matcher)
    matcher=re.sub(r"PIN_SHA = '[0-9a-f]+'","PIN_SHA = '"+sha256(generator_pins)+"'",matcher)
    matcher=matcher.replace("    inputs = [dict", "    if not re.search(r'^BOOL\\s+' + re.escape(pin['name']) + r'\\(void\\)', text, re.M):\n        raise ValueError('Measured BOOL registration entry has no formal input words')\n    inputs = [dict")
    matcher=matcher.replace("        implementationFamily=", "        sourceAbiContract={'physicalArgumentWords': 0, 'return': 'void', 'createThreadPhysicalWords': 6},\n        implementationFamily=")
    matcher=matcher.replace('^BOOL','^void').replace('BOOL32','void')
    target=ROOT/'match_arm7_lane_card_init_20261031.py'
    target.write_text(matcher)
    write_json(ROOT/'provenance/arm7-lane-card-init188-sealing-20261031.json',dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),
        matcherSha256=sha256(target),profileSha256=sha256(profile),pinsSha256=sha256(generator_pins),sourceCredit=0))
    print(dict(matcher=target.name,sha256=sha256(target),bytes=188))


if __name__=='__main__':
    main()
