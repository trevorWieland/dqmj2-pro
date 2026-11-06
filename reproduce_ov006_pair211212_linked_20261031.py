import hashlib
import match_ov006_snapshot211_20261031 as snapshot
import match_ov006_loop212_20261031 as loop
from project import ROOT,read_json,write_json,sha256
from link_runtime_unit import measured_module
from seal_recovery_sources_20261031 import seal_sources


def linked(producer,stem):
    producer.run()
    raw=f'evidence/matches/ov006-20261031-{stem}.json'
    output=f'evidence/matches/ov006-20261031-{stem}-linked.json'
    report=read_json(ROOT/raw);metadata,native,config=measured_module('ov006')
    assert hashlib.sha256(native).hexdigest()==report['moduleInputSha256'] and len(report['matches'])==1
    for row in report['matches']:
        assert row['mode']=='thumb' and row['exactAfterDeclaredRelocation'] is False
        validation=read_json(ROOT/row['isolatedCallerLinkValidation']);payload=(ROOT/row['isolatedCallerBinary']).read_bytes()
        for key in ['isolatedCallerBinary','isolatedCallerLinkValidation','isolatedCallerLinkSnapshotManifest','isolatedCallerLinkedElf','isolatedCallerLinkLcf']:
            assert sha256(ROOT/row[key])==row[key+'Sha256']
        assert validation['exactCallerBytes'] and validation['linkerAttempt']['exitCode']==0
        assert validation['sourceObjectSha256']==row['objectSha256'] and validation['sourceSha256']==row['sourceSha256']
        address=int(row['address'],0);size=row['bytes'];target=native[address-0x021D7240:address-0x021D7240+size]
        assert len(payload)==len(target)==size and hashlib.sha256(target).hexdigest()==row['targetSha256']
        matching=sum(a==b for a,b in zip(payload,target));assert payload==target and matching==row['linkedMatchingBytes']==124
        row['compilerObjectPrelinkComparison']={key:row[key] for key in ['compiledBytes','matchingBytes','exactAfterDeclaredRelocation','outputSha256']}
        row.update(exactBytes=True,exactAfterRealMwLink=True,matchingBytes=matching,outputSha256=hashlib.sha256(payload).hexdigest(),linked=True,
            comparisonStage='independently-measured-genuine-MWLD-caller',linkedOutputSha256=hashlib.sha256(payload).hexdigest())
    report['sourceWorkerReport']={'path':raw,'sha256':sha256(ROOT/raw),'originalPrelinkFieldsUnchanged':True}
    report['replayDependencies']=[*report.get('replayDependencies',[]),{'path':raw,'sha256':sha256(ROOT/raw)}]
    report['acceptedSourceCredit']=0
    write_json(ROOT/output,report);seal_sources(output,['reproduce_ov006_pair211212_linked_20261031.py'])
    print(dict(report=output,linkedMatchingBytes=124,prelinkComparisonStillFalse=True,sourceCredit=0))


def main():
    linked(snapshot,'snapshot211')
    linked(loop,'loop212')


if __name__=='__main__':main()
