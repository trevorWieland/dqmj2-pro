import argparse
import match_main_fifo_requests352_v2_20261101 as producer
from project import ROOT, read_json, write_json, sha256
from source_dependencies import dependencies_current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--existing', action='store_true')
    options = parser.parse_args()
    if not options.existing:
        producer.main()
    path = ROOT / 'evidence/matches/main-fifo-requests352-v2-20261101.json'
    report = read_json(path)
    assert report['generatorSha256'] == sha256(producer.__file__)
    assert report['fixtureSha256'] == sha256(ROOT / report['fixture'])
    header = 'src/runtime/20261101_fifo_requests352/state.h'
    declared = 'ca49923c24f09c1de242f6bfe7f7f4380b67917f8370b2604437b239ed4c308e'
    assert sha256(ROOT / header) == declared
    for row in report['matches']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert '#include "state.h"' in (ROOT / row['source']).read_text()
        assert row['exactAfterDeclaredRelocation'] and row['bytes'] == row['compiledBytes']
        row['sourceDependencies'] = [dict(path=header, sha256=declared)]
        assert dependencies_current(row, report)
    report['authoredHeaderDependencySeal'] = dict(generator=__file__.split(chr(92))[-1],
        generatorSha256=sha256(__file__), header=header, sha256=declared,
        reconstructedCodeChanged=False, compilerOrFlagsChanged=False, sourceCredit=0)
    write_json(path, report)
    print(dict(functions=3, exactBytes=352, headerDependencyDeclared=True, sourceCredit=0))


if __name__ == '__main__':
    main()
