import argparse
import sys
from project import ROOT,read_json,write_json,sha256
import wave20261105_gpi_connect_next_profilecallback_packet as original
from wave20261105_gpi_connect_next_profilecallback_paths import assert_owned,EVIDENCE as LANE


def main():
    assert_owned(LANE)
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();path=LANE/'qualified-inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable qualified manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    previous=sys.argv
    try:
        sys.argv=[original.__file__,'--inputs-sha256','dde559cd788ac73a64ba57c89273b6826e21c4a3c6230b3242a9c185e91974d4'];original.main()
    finally:sys.argv=previous
    report=read_json(LANE/'match.json')
    report.update(inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=__file__.split('\\')[-1].split('/')[-1],generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],seedManifestClosureQualified=True)
    write_json(LANE/'match.json',report)


if __name__=='__main__':main()
