import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module

REPORTS=['broad-family199','broad-family200','broad-family207','broad-family208']


def sha(raw):return hashlib.sha256(raw).hexdigest()


def jobs():
    result={}
    for name in REPORTS:
        p=json.loads((ROOT/f'evidence/lanes/save-core/{name}-20261101.json').read_text())
        side=p['fullProvenanceSidecar']
        packed=(ROOT/side['path']).read_bytes()
        raw=gzip.decompress(packed)
        assert sha(packed)==side['sha256'] and sha(raw)==side['uncompressedSha256']
        for row in json.loads(raw):
            if not row.get('drafted'):continue
            assert sha((ROOT/row['source']).read_bytes())==row['sourceSha256']
            for attempt in row.get('compileAttempts',[]):
                if not attempt.get('realLinkSucceeded'):continue
                key=(row['address'],row['sourceSha256'],tuple(attempt['flags']))
                result.setdefault(key,dict(entry=int(row['address'],0),bytes=row['bytes'],source=row['source'],sourceSha256=row['sourceSha256'],flags=attempt['flags'],compiler=attempt['compilerPath'],compilerSha256=attempt['compilerSha256'],linkedBodySha256=attempt['linkedBinarySha256'],exactByteEqual=attempt['exactByteEqual'],compiledBytes=attempt['compiledBytes']))
    return sorted(result.values(),key=lambda row:(row['entry'],row['source'],row['flags']))


def run(job,index,arm):
    spec=importlib.util.spec_from_file_location('breadth_replay215_'+str(index),ROOT/'evidence/application/save_core_historical_link_20261031.py')
    b=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    b.ENTRY,b.LENGTH,b.MODE,b.NAME=job['entry'],job['bytes'],'arm',f"native_main_{job['entry']:08x}"
    b.SOURCE,b.WORK,b.FLAGS,b.COMPILER,b.COMPILER_HASH=job['source'],f'work/save-core/breadth-replay215/{index:03}',job['flags'],job['compiler'],job['compilerSha256']
    row,body=b.build(arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH])
    assert sha(body)==job['linkedBodySha256'] and row['exactByteEqual']==job['exactByteEqual'] and row['compiledBytes']==job['compiledBytes']
    return dict(entry=hex(b.ENTRY),source=b.SOURCE,sourceSha256=row['sourceSha256'],compilerPath=b.COMPILER,compilerSha256=b.COMPILER_HASH,flags=b.FLAGS,compiledBytes=len(body),linkedBodySha256=sha(body),exactByteEqual=row['exactByteEqual'],sourceCredit=0)


def main():
    metadata,arm,_=measured_module('main')
    assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    tasks=jobs()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run,job,i,arm) for i,job in enumerate(tasks)]
        results=[future.result() for future in futures]
    raw=(json.dumps(results,indent=2)+'\n').encode()
    packed=gzip.compress(raw,mtime=0)
    path=ROOT/'evidence/vectors/save-core-breadth-replay215-20261101.json.gz'
    path.write_bytes(packed)
    output=dict(schemaVersion=1,sourceCreditAdded=0,counts=dict(successfulGenuineLinkReplays=len(results),uniqueSourceIdentities=len({(r['entry'],r['sourceSha256']) for r in results})),
        resultSidecar=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(packed),uncompressedSha256=sha(raw),contexts=len(results)),limitations=[
            'Only previously successful compiler/link profiles are replayed from frozen C and declared current compilerPath/flags. Native code hashes and linked body hashes are checked;old-root object/debug hashes are not treated as portable identities.',
            'Recorded failed drafting/compilation attempts remain preserved reports,not successful replay counts. Selection/redrafting generators are archival experiments that depend on repository candidate state;this command repeats their successful source builds.',
            'No native semantic,module orROM acceptance is implied;all new archive source credit remains0. Exact C8B18 hypothesis hasseparate typed source/proof packet205.'])
    target=ROOT/'evidence/lanes/save-core/breadth-replay215-20261101.json'
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(output['counts'],sha(target.read_bytes()))


if __name__=='__main__':main()
