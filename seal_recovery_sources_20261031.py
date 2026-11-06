import argparse
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import seal,code_closure


def seal_sources(relative,producer):
    seal(relative,producer)
    document=read_json(ROOT/relative);pins={row['path']:row['sha256'] for row in document['generatorSources']}
    for row in document.get('replayDependencies',[]):
        if Path(row['path']).suffix.lower() in ['.c','.cpp','.h','.inc','.py','.s']:
            assert sha256(ROOT/row['path'])==row['sha256'];pins[row['path']]=row['sha256']
    for path in code_closure(['seal_recovery_sources_20261031.py']):pins[path]=sha256(ROOT/path)
    document['generatorSources']=[{'path':path,'sha256':digest} for path,digest in sorted(pins.items())]
    document['replayCodeSeal']['immutableDeclaredSourceFilesIncluded']=True
    write_json(ROOT/relative,document)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('report');parser.add_argument('--existing',action='store_true');parser.add_argument('producer',nargs='+');args=parser.parse_args()
    if not args.existing:subprocess.run([sys.executable,str(ROOT/args.producer[0]),*args.producer[1:]],cwd=ROOT,check=True)
    seal_sources(args.report,args.producer)


if __name__=='__main__':
    main()
