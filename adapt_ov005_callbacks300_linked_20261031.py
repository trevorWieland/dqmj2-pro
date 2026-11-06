import copy
import hashlib
import json
from project import ROOT, configuration, read_json, write_json, sha256
import match_ov005_callbacks300_20261031 as worker
from link_runtime_unit import measured_module

RAW = ROOT / 'evidence/matches/ov005-20261031-callbacks300.json'
OUTPUT = ROOT / 'evidence/matches/ov005-20261031-callbacks300-linked.json'


def main():
    worker.run()
    raw = read_json(RAW)
    metadata, original, unused = measured_module('ov005')
    assert raw['romSha256'] == configuration()['romSha256']
    assert raw['moduleInputSha256'] == metadata['sha256']
    report = copy.deepcopy(raw)
    evidence = []
    assert len(report['matches']) == 2
    expected = {0x021E19B8: 180, 0x021E1A6C: 56}
    for row in report['matches']:
        address = int(str(row['address']), 0)
        size = expected[address]
        assert row['processor'] == 'arm9' and row['module'] == 'ov005' and row['mode'] == 'arm'
        assert row['bytes'] == row['compiledBytes'] == row['linkedMatchingBytes'] == size
        assert row['exactAfterGenuineLink'] is True
        for path_key, hash_key in [
            ('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256'),
            ('isolatedCallerLinkLcf', 'isolatedCallerLinkLcfSha256'),
            ('isolatedCallerLinkedElf', 'isolatedCallerLinkedElfSha256'),
        ]:
            assert sha256(ROOT / row[path_key]) == row[hash_key]
        base = int(metadata['base'], 0)
        assert base == 0x021D7240
        offset = address - base
        native = original[offset:offset + size]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        assert len(linked) == size and linked == native
        comparison = dict(address=hex(address), bytes=size, matchingBytes=sum(a == b for a, b in zip(linked, native)),
                          nativeSha256=hashlib.sha256(native).hexdigest(), linkedSha256=hashlib.sha256(linked).hexdigest(),
                          comparisonStage='fresh genuine mwldarm-linked caller', exactBytes=linked == native)
        row['preLinkComparison'] = {key: row[key] for key in ['matchingBytes', 'exactAfterDeclaredRelocation']}
        row['exactBytes'] = comparison['exactBytes']
        row['exactBytesComparison'] = comparison
        evidence.append(comparison)
    report['functionMatchesCount'] = report.pop('functionMatches')
    report['rawWorkerDeterministicContentSha256'] = report.pop('deterministicContentSha256')
    report['rawProducer'] = dict(path='match_ov005_callbacks300_20261031.py',
                                sha256=sha256(ROOT / 'match_ov005_callbacks300_20261031.py'),
                                report=RAW.relative_to(ROOT).as_posix(), reportSha256=sha256(RAW))
    report['genuineLinkComparisons'] = evidence
    report['generator'] = 'adapt_ov005_callbacks300_linked_20261031.py'
    report['generatorSha256'] = sha256(__file__)
    report['reproductionCommand'] = 'python adapt_ov005_callbacks300_linked_20261031.py'
    report['volatileIdentityFields'] = ['createdUtc', 'rawProducer.reportSha256']
    stable = copy.deepcopy(report)
    stable.pop('createdUtc')
    stable['rawProducer'].pop('reportSha256')
    report['deterministicContentSha256'] = hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()
    write_json(OUTPUT, report)
    print(dict(functions=2, genuineLinkedBytes=sum(item['bytes'] for item in evidence),
               preLinkComparisonsPreserved=True, sourceCredit=0))


if __name__ == '__main__':
    main()
