import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import seal

PRODUCER='match_overlay_packet28_20261031.py'
REPORTS=['evidence/matches/ov001-20261031-ability28.json','evidence/matches/ov006-20261031-summary28.json']


def main():
    subprocess.run([sys.executable,str(ROOT/PRODUCER)],cwd=ROOT,check=True)
    own=Path(__file__).name
    for relative in REPORTS:
        path=ROOT/relative
        report=read_json(path)
        existing={row['path']:row['sha256'] for row in report.get('generatorSources',[])}
        existing[own]=sha256(ROOT/own)
        report['generatorSources']=[{'path':name,'sha256':digest} for name,digest in sorted(existing.items())]
        write_json(path,report)
        seal(relative,[PRODUCER])
        report=read_json(path)
        report['replayCodeSeal']['producerCommand']=[own]
        report['replayCodeSeal']['pairedReportsRebuiltAndSealedTogether']=REPORTS
        write_json(path,report)
    print({'sealedReports':REPORTS,'sourceOrNativeByteCredit':0})


if __name__=='__main__':
    main()
