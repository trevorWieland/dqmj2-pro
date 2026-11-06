import ast
from unittest.mock import patch
import oracle_source_closure_20261031 as closure
from static_json_reads_20261031 import required_json_reads
from project import ROOT,write_json,sha256


def main():
    directory=ROOT/'work/batch-static-input-controls-20261031';directory.mkdir(parents=True,exist_ok=True)
    files={'run_checks.py':'pass\n','configure.py':'pass\n','validate_clean_checkout.py':'pass\n',
        'batch_fixture.py':"PINS=ROOT/'evidence/verification/frozen-inputs.json'\nOUTPUT=ROOT/'evidence/history.json'\ndef run():\n    PINS.read_text()\n    OUTPUT.write_text('{}')\n",
        'nonmatching/unit/source.c':'int sample(void){return 1;}\n','not_an_input.py':'pass\n'}
    for name,text in files.items():
        path=directory/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    pins=directory/'evidence/verification/frozen-inputs.json'
    write_json(pins,dict(files=[dict(path='nonmatching/unit/source.c',sha256=sha256(directory/'nonmatching/unit/source.c'))]))
    write_json(directory/'evidence/batch.json',dict(sourceCredit=0))
    write_json(directory/'evidence/history.json',dict(source='not_an_input.py'))
    write_json(directory/'recovery.json',dict(oracles=[],batches=[dict(report='evidence/batch.json',reproduce=['batch_fixture.py'],sourceHashes={})]))
    with patch.object(closure,'ROOT',directory),patch.object(closure,'SEARCH',[directory]):
        report=closure.collect();assert not report['missingRequiredPaths']
        assert all(path in report['sourceAndEvidenceHashes']for path in ['batch_fixture.py','evidence/verification/frozen-inputs.json','nonmatching/unit/source.c'])
        assert 'not_an_input.py'not in report['sourceAndEvidenceHashes']
        for path in [pins,directory/'nonmatching/unit/source.c']:
            content=path.read_bytes();path.unlink()
            try:assert path.relative_to(directory).as_posix()in closure.collect()['missingRequiredPaths']
            finally:path.write_bytes(content)
    tree=ast.parse("INFILE=ROOT/'evidence/data.json'\nOUTFILE=ROOT/'evidence/out.json'\nread_json(INFILE)\nOUTFILE.open('w')\n")
    assert required_json_reads(tree,directory)=={'evidence/data.json'}
    current=closure.collect();known='evidence/verification/ov000-buffer178-inputs-20261031.json'
    assert known in current['sourceAndEvidenceHashes'] and known in current['staticJsonReads']
    write_json(ROOT/'evidence/verification/batch-static-input-controls-20261031.json',dict(sourceCredit=0,generatorSha256=sha256(__file__),
        batchRootsIncluded=True,missingReadInputRejected=True,missingNestedPinRejected=True,outputOnlyHistoryNotExpanded=True,
        readWriteModesDistinguished=True,knownCleanWFailureIncluded=True,knownInput=known,knownInputSha256=current['sourceAndEvidenceHashes'][known],
        missingRequired=current['missingRequiredPaths']))
    print(dict(controls=6,knownInputIncluded=True,missingRequired=current['missingRequiredPaths'],paths=len(current['sourceAndEvidenceHashes'])))
    assert not current['missingRequiredPaths']


if __name__=='__main__':main()
