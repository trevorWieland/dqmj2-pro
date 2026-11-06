from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_resource_binding1808_ports_20261102 as complete

REPORT=ROOT/'evidence/matches/main-resource-interface840-20261102.json'


def main():
    complete.main()
    full=ROOT/'evidence/matches/main-resource-binding1808-ports-20261102.json';report=read_json(full)
    wanted={0x0202BEDC,0x0202EDFC,0x0202EFE4,0x0202F250}
    rows=[r for r in report['matches']if int(r['address'],0)in wanted]
    assert len(rows)==4 and sum(r['bytes']for r in rows)==840
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),matches=rows,matchedFunctions=4,matchedBytes=840,
     completeFamilyProof=dict(path=full.relative_to(ROOT).as_posix(),sha256=sha256(full),compiledBodies=7,
      unmodifiedExistingSelectionsRetained=[hex(a)for a in[0x0202F170,0x0202F3DC,0x02031FA4]]),
     reproductionCommand='python match_main_resource_interface840_20261102.py')
    report['replayDependencies'].append(dict(path=full.relative_to(ROOT).as_posix(),sha256=sha256(full)))
    write_json(REPORT,report)
    print('Four registration rows840 bytes; seven-body native/Windows evidence retained')


if __name__=='__main__':
    main()
