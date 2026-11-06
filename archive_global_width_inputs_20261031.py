import argparse
from project import ROOT,read_json,write_json,sha256

DESTINATION=ROOT/'generated/drafts/main-global-width-pair-20261031/seed-inputs'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--restore',action='store_true');args=parser.parse_args()
    manifest=DESTINATION/'manifest.json'
    if args.restore:
        rows=read_json(manifest)['files']
        for row in rows:
            target=(ROOT/row['originalPath']).resolve();source=ROOT/row['archivedPath']
            assert target.is_relative_to(ROOT/'work') or row['originalPath'] in ['evidence/attempts/main-expanded-breadth12-20261031.json','evidence/attempts/main-large-breadth13-20261031.json']
            assert sha256(source)==row['sha256']
            if target.exists():assert sha256(target)==row['sha256']
            else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
        print(dict(restoredOrVerifiedInputs=len(rows),sourceCredit=0));return
    paths=set()
    for stem in ['main-expanded-breadth12-20261031','main-large-breadth13-20261031']:
        report=ROOT/f'evidence/attempts/{stem}.json';paths.add(report)
        for row in read_json(report)['results']:
            if not row.get('draftSource') or row['mode']!='arm':continue
            paths.add(ROOT/row['draftSource'])
            directory=ROOT/'work'/stem/f'arm-{int(row["address"],0):08x}'/'functions'/row['nativeAlias']
            paths.update([directory/'context.c',directory/'input.s'])
    rows=[]
    for path in sorted(paths):
        relative=path.relative_to(ROOT).as_posix();target=DESTINATION/relative;data=path.read_bytes()
        if target.exists():assert target.read_bytes()==data
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        rows.append(dict(originalPath=relative,archivedPath=target.relative_to(ROOT).as_posix(),sha256=sha256(target)))
    write_json(manifest,dict(sourceCredit=0,generatorSha256=sha256(__file__),files=rows,generatedInputsOnly=True,
        reproduction=['python archive_global_width_inputs_20261031.py --restore','python draft_main_global_width_pair_20261031.py']))
    print(dict(archivedInputs=len(rows),sourceCredit=0))


if __name__=='__main__':main()
