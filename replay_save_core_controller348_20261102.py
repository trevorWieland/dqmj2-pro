import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module


def sha(raw):return hashlib.sha256(raw).hexdigest()


def current(job):
    row,index=job;spec=importlib.util.spec_from_file_location('controller348_'+str(index),ROOT/'evidence/application/save_core_historical_link_20261031.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    b.ENTRY,b.LENGTH,b.NAME=0x020CB490,308,'native_main_020cb490';b.SOURCE,b.FLAGS=row['source'],row['flags'];b.COMPILER,b.COMPILER_HASH=row['compilerPath'],row['compilerSha256'];b.WORK='work/save-core/controller348/replay/'+str(index)
    arm=measured_module('main')[1];result,body=b.build(arm[0xCB490:0xCB5C4]);assert (result['compiledBytes'],result['sameOffsetBytes'])==(row['compiledBytes'],row['sameOffsetBytes']) and sha(body)==row['linkedBinarySha256'] and not result['exactByteEqual'];return result


def main():
    p='evidence/lanes/save-core/controller348-history-20261102.json';d=json.loads((ROOT/p).read_text());s=d['sidecar'];packed=(ROOT/s['path']).read_bytes();raw=gzip.decompress(packed);assert sha(packed)==s['sha256'] and sha(raw)==s['contentSha256'];rows=json.loads(raw)
    for source in d['sourceRows']:assert sha((ROOT/source['path']).read_bytes())==source['sha256']
    assert len(rows)==14
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(current,[(row,i) for i,row in enumerate(rows)]))
    raw=(json.dumps(results,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-controller348-current-20261102.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));out=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueNativeFunctions=1,uniqueNativeBytes=308,sourceHypotheses=10,genuineLinkedProfiles=14,bestSameOffsetBytes=291,exactSourceUnits=0,actualNativeReturns=0,actualCompiledReturns=0,sources=d['sourceRows'],history=dict(path=p,sha256=sha((ROOT/p).read_bytes())),historicalCompilerArchive=s,currentCompilerProvenance=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),contentSha256=sha(raw)),generatorSha256=sha(Path(__file__).read_bytes()),limits=d['limits']);path=ROOT/'evidence/lanes/save-core/controller348-20261102.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(hypotheses=10,profiles=14,best='291/308',exact=0,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
