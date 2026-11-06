import argparse
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256
from wave20261106_itcm_reset_next_paths import EVIDENCE,assert_owned


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();assert_owned();path=EVIDENCE/'package-inputs-v3.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable package manifest changed')
    package=read_json(path)
    for pin in package['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    original=package['originalProducer'];subprocess.run([sys.executable,str(ROOT/original[0]),*original[1:]],cwd=ROOT,check=True)
    report=read_json(EVIDENCE/'match.json');report.update(packageInputManifest=path.relative_to(ROOT).as_posix(),packageInputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=package['generatorSources'],originalFrozenProducer=original,actualPinnedCompilerRuntimeDlls=package['compilerRuntimeDlls'])
    write_json(EVIDENCE/'match.json',report)


if __name__=='__main__':main()
