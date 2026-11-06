import argparse
import subprocess
import sys
from copy import deepcopy
from project import ROOT, configuration, read_json, sha256, write_json


RAW = 'evidence/data/arm7-child-crc-table32-20261031.json'
OUTPUT = 'evidence/matches/arm7-child-crc-table32-integrated-20261031.json'
PROGRAM = 'dwc/utility.bin/move/child.srl'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--existing', action='store_true')
    options = parser.parse_args()
    if not options.existing:
        subprocess.run([sys.executable, str(ROOT / 'match_arm7_crc_table32_20261031.py')], cwd=ROOT, check=True)
    raw = read_json(ROOT / RAW)
    assert raw['romSha256'] == configuration()['romSha256']
    assert len(raw['dataMatches']) == 1 and raw['ordinaryCCodeBytes'] == raw['ordinaryFunctionCredit'] == 0
    row = raw['dataMatches'][0]
    assert row['program'] == PROGRAM and row['processor'] == 'arm7' and row['mode'] == 'data'
    assert row['address'] == '0x27f7f74' and row['bytes'] == row['compiledBytes'] == 32
    assert row['module'] == 'utility-child-arm7-main'
    assert row['sourceSymbolType'] == 'STT_OBJECT' and row['relocations'] == []
    assert row['kind'] == 'initialized-data' and row['ordinaryFunctionCredit'] == 0
    assert row['exactBytes'] and row['exactAfterRealMwLink']
    for key in ['source', 'object', 'inputModule', 'linkedDataBinary']:
        assert sha256(ROOT / row[key]) == row[key + 'Sha256']
    report = deepcopy(raw)
    report.update(program=PROGRAM, processor='arm7', module=row['module'])
    report['dataMatches'][0]['kind'] = 'data'
    report['adapter'] = dict(path=__file__.split('\\')[-1], sha256=sha256(__file__),
        originalReport=RAW, originalReportSha256=sha256(ROOT / RAW),
        changes=['Lift the already measured program/processor/module into the report namespace',
                 'Use the existing linker initialized-data kind'],
        sourceOrObjectChanges=0, newFunctionCredit=0, executableByteCredit=0)
    assert report['dataMatches'][0]['sourceSha256'] == row['sourceSha256']
    assert report['dataMatches'][0]['objectSha256'] == row['objectSha256']
    write_json(ROOT / OUTPUT, report)
    print(dict(report=OUTPUT, initializedDataBytes=32, ordinaryFunctionCredit=0))


if __name__ == '__main__':
    main()
