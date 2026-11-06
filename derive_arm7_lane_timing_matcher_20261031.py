from pathlib import Path
from project import ROOT,sha256


def main():
    text=(ROOT/'match_arm7_lane_driver_leaves_20261030.py').read_text()
    text=text.replace('arm7_lane_driver_leaves_boundaries_20261030','arm7_lane_timing_boundaries_20261031')
    text=text.replace('arm7_lane_driver_leaves_oracle_20261030','arm7_lane_timing_oracle_20261031')
    text=text.replace('lane-driver-leaves-final68','lane-timing-final')
    text=text.replace("ROOT / 'nonmatching/arm7-bulk/20261030/lane-timing-final/closure.json'", "ROOT / 'nonmatching/arm7-bulk/20261031/lane-timing-final/closure.json'")
    profile=ROOT/'nonmatching/arm7-bulk/20261031/lane-timing-final/closure.json'
    text=text.replace('da82cdc6ed8fbff02c7bd68a91a89fd9be43198c88dc3e677de5ed0dc2ed1152',sha256(profile))
    text=text.replace('41d2bb1e52fa98573d88aeed3866701937ec3dfcf956a63ceb0b6509ae643841',sha256(profile.with_name('generator-pins.json')))
    first=text.index('    includes = re.findall(')
    last=text.index('    directory = WORK',first)
    text=text[:first]+'''    seen = set()
    pending = [source]
    while pending:
        current = pending.pop()
        for name in re.findall(r'^#include "([^"<>]+)"$', current.read_text(), re.M):
            included = (current.parent/name).resolve()
            if not included.is_relative_to(source.parent.resolve()):
                raise ValueError('Source-only quoted include escaped promoted closure')
            if included not in seen:
                seen.add(included)
                pending.append(included)
    if {path.relative_to(ROOT).as_posix() for path in seen} != {item['path'] for item in pin['sourceDependencies']}:
        raise ValueError('Actual recursive compiler include closure differs')
'''+text[last:]
    text=text.replace("implementationFamily='typed-mmio-stop-and-halfword-timer'", "implementationFamily='bounded-timer-calculation' if address == 0x037FECAC else 'sequence-skip-and-real-alarm-state'")
    text=text.replace("'syntheticBiosContractOriginalAndCompiledReturns': 0", "'syntheticBiosContractOriginalAndCompiledReturns': sum(row['oracle']['syntheticBiosContractOriginalAndCompiledReturns'] for row in results)")
    text=text.replace("'referenceProvenance': {'kind': 'measured-native-driver-cpu-behavior', 'compilerInput': False}", "'referenceProvenance': {'kind': 'local-SDK-correspondence-plus-independent-native-contracts', 'compilerInput': False}")
    text=text.replace('arm7-lane-driver-leaves-20261030.json','arm7-lane-timing-20261031.json')
    destination=ROOT/'match_arm7_lane_timing_20261031.py'
    if destination.exists() and destination.read_text()!=text:
        raise ValueError('Refusing to replace a different timing matcher')
    destination.write_text(text)
    print(dict(matcherSha256=sha256(destination)))


if __name__=='__main__':
    main()
