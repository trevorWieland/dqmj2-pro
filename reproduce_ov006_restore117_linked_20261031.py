import hashlib
import match_ov006_restore117_20261031 as producer
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import measured_module
from seal_recovery_sources_20261031 import seal_sources

RAW='evidence/matches/ov006-20261031-restore117.json'
OUTPUT='evidence/matches/ov006-20261031-restore117-linked.json'


def main():
    producer.run();report=read_json(ROOT/RAW);metadata,native,config=measured_module('ov006')
    assert hashlib.sha256(native).hexdigest()==report['moduleInputSha256']
    assert len(report['matches'])==1
    for row in report['matches']:
        assert row['mode']=='thumb' and row['exactAfterDeclaredRelocation'] is False
        validation=read_json(ROOT/row['isolatedCallerLinkValidation']);payload=(ROOT/row['isolatedCallerBinary']).read_bytes()
        for key in ['isolatedCallerBinary','isolatedCallerLinkValidation','isolatedCallerLinkSnapshotManifest','isolatedCallerLinkedElf','isolatedCallerLinkLcf']:
            assert sha256(ROOT/row[key])==row[key+'Sha256']
        assert validation['exactCallerBytes'] and validation['linkerAttempt']['exitCode']==0
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==row['sourceSha256']
        address=int(row['address'],0);size=row['bytes'];target=native[address-0x021D7240:address-0x021D7240+size]
        assert len(payload)==len(target)==size and hashlib.sha256(target).hexdigest()==row['targetSha256']
        matching=sum(a==b for a,b in zip(payload,target));exact=payload==target
        assert exact and matching==row['linkedMatchingBytes']
        row['compilerObjectPrelinkComparison']={key:row[key] for key in ['compiledBytes','matchingBytes','exactAfterDeclaredRelocation','outputSha256']}
        row.update(exactBytes=exact,exactAfterRealMwLink=exact,matchingBytes=matching,outputSha256=hashlib.sha256(payload).hexdigest(),linked=exact,comparisonStage='independently-measured-genuine-MWLD-caller',linkedOutputSha256=hashlib.sha256(payload).hexdigest())
    report['sourceWorkerReport']={'path':RAW,'sha256':sha256(ROOT/RAW),'originalPrelinkFieldsUnchanged':True}
    report['replayDependencies']=[*report.get('replayDependencies',[]),{'path':RAW,'sha256':sha256(ROOT/RAW)}]
    report['acceptedSourceCredit']=0
    write_json(ROOT/OUTPUT,report);seal_sources(OUTPUT,['reproduce_ov006_restore117_linked_20261031.py'])
    print({'linkedMatchingBytes':matching,'exactLinkedBytes':exact,'prelinkComparisonStillFalse':row['exactAfterDeclaredRelocation'] is False,'sourceCredit':0})


if __name__=='__main__':main()
