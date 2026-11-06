import json
from unittest.mock import patch
import oracle_source_closure_20261031 as closure
from project import ROOT,write_json,sha256


def main():
    directory=ROOT/'work/oracle-static-input-controls-20261031';directory.mkdir(parents=True,exist_ok=True)
    files={
        'run_checks.py':'pass\n','configure.py':'pass\n','validate_clean_checkout.py':'pass\n',
        'static_oracle_fixture.py':"PROFILE='nonmatching/unit/profile.json'\n",
        'nonmatching/unit/source.c':'#include "extra.h"\nint fixture(void) { return VALUE; }\n',
        'nonmatching/unit/extra.h':'#define VALUE 7\n',
        'not_a_runtime_input.py':'pass\n',
    }
    for name,text in files.items():
        path=directory/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    write_json(directory/'nonmatching/unit/generator-pins.json',dict(files=[dict(path='nonmatching/unit/extra.h',sha256=sha256(directory/'nonmatching/unit/extra.h'))]))
    write_json(directory/'nonmatching/unit/profile.json',dict(definition=dict(source='nonmatching/unit/source.c',sourceSha256=sha256(directory/'nonmatching/unit/source.c'),pins='nonmatching/unit/generator-pins.json'),historicalReport='evidence/history.json'))
    write_json(directory/'evidence/history.json',dict(source='not_a_runtime_input.py'))
    write_json(directory/'evidence/oracle.json',dict(profile='nonmatching/unit/profile.json'))
    write_json(directory/'recovery.json',dict(oracles=[dict(report='evidence/oracle.json',reproduce=['static_oracle_fixture.py'])]))
    with patch.object(closure,'ROOT',directory),patch.object(closure,'SEARCH',[directory]):
        current=closure.collect()
        needed=['nonmatching/unit/source.c','nonmatching/unit/extra.h','nonmatching/unit/profile.json','nonmatching/unit/generator-pins.json']
        assert not current['missingRequiredPaths'] and all(name in current['sourceAndEvidenceHashes'] for name in needed)
        assert 'not_a_runtime_input.py' not in current['sourceAndEvidenceHashes']
        header=directory/'nonmatching/unit/extra.h';content=header.read_bytes();header.unlink()
        try:missing=closure.collect();assert 'nonmatching/unit/extra.h' in missing['missingRequiredPaths']
        finally:header.write_bytes(content)
    report=closure.collect();needed='nonmatching/arm7-bulk/20261030/seq-main-final01/native_arm7_wram_037fff54.c'
    assert needed in report['sourceAndEvidenceHashes'] and report['sourceAndEvidenceHashes'][needed]=='830288c663af1edf3a81c357df69da0e2f40668c377b39848611a182a95fd181'
    write_json(ROOT/'evidence/verification/oracle-static-input-closure-controls-20261031.json',dict(generator=__file__.split('\\')[-1],generatorSha256=sha256(__file__),sourceCredit=0,nestedStaticInputsIncluded=True,missingHashedInputRejected=True,historicalEvidenceNotExpanded=True,knownCleanUFailureInputIncluded=True,knownInput=needed,knownInputSha256=report['sourceAndEvidenceHashes'][needed],actualMissingRequired=report['missingRequiredPaths']))
    assert not report['missingRequiredPaths'];print(dict(controls=4,allPassed=True,paths=len(report['sourceAndEvidenceHashes'])))


if __name__=='__main__':main()
