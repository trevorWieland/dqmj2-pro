import argparse,hashlib,json,subprocess
from project import ROOT,write_json


def main():
    parser=argparse.ArgumentParser();parser.add_argument('commit');parser.add_argument('manifest');parser.add_argument('sha256');parser.add_argument('label');args=parser.parse_args()
    payload=subprocess.run(['git','show',args.commit+':'+args.manifest],capture_output=True,check=True).stdout
    assert hashlib.sha256(payload).hexdigest()==args.sha256
    manifest=json.loads(payload);records=manifest['files']+[{'path':args.manifest,'sha256':args.sha256}];prepared=[]
    for row in records:
        target=(ROOT/row['path']).resolve();assert target.is_relative_to(ROOT)
        data=subprocess.run(['git','show',args.commit+':'+row['path']],capture_output=True,check=True).stdout
        assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
        if target.exists():assert target.read_bytes()==data,('Existing content conflict',row['path'])
        prepared.append((target,data))
    archive=ROOT/'provenance/handoffs'/args.label;assert not archive.exists();archive.mkdir(parents=True)
    for target,data in prepared:
        if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        if target.suffix=='.json' and target.relative_to(ROOT).parts[0] in ['evidence','provenance']:
            name=target.relative_to(ROOT).as_posix().replace('/','__');(archive/name).write_bytes(data)
    report={'commit':args.commit,'manifest':args.manifest,'manifestSha256':args.sha256,'verifiedPaths':len(prepared),'registryMutated':False,'sourceCredit':0,'originalWorkerEvidenceArchive':archive.relative_to(ROOT).as_posix()}
    write_json(ROOT/f'evidence/verification/{args.label}-import-20261031.json',report);print(report)


if __name__=='__main__':
    main()
