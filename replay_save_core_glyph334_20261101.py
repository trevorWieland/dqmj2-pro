import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT),str(ROOT/'deps/native')]
from link_runtime_unit import measured_module
CASE329='7de845799d3c5c7243f78c4b0fdc4a3c48d070f160f0445dc345e5d47564c4c6'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def compile_current(job):
    row,index=job
    spec=importlib.util.spec_from_file_location('glyph334_'+str(index),ROOT/'evidence/application/save_core_historical_link_20261031.py')
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    b.ENTRY,b.LENGTH,b.NAME=0x020471A0,620,'native_main_020471a0'
    b.SOURCE,b.FLAGS=row['source'],row['flags'];b.COMPILER,b.COMPILER_HASH=row['compilerPath'],row['compilerSha256']
    b.WORK='work/save-core/glyph-replay334/'+str(index)
    arm=measured_module('main')[1];current,body=b.build(arm[0x471A0:0x4740C])
    assert (current['compiledBytes'],current['sameOffsetBytes'])==(row['compiledBytes'],row['sameOffsetBytes'])
    assert sha(body)==row['linkedBinarySha256'] and not current['exactByteEqual']
    return current


def main():
    archive_path='evidence/lanes/save-core/glyph-layout334-history-20261101.json'
    history=json.loads((ROOT/archive_path).read_text());sidecar=history['sidecar']
    packed=(ROOT/sidecar['path']).read_bytes();raw=gzip.decompress(packed)
    assert sha(packed)==sidecar['sha256'] and sha(raw)==sidecar['contentSha256']
    historical=json.loads(raw);jobs=[]
    for row in historical:
        assert sha((ROOT/row['source']).read_bytes())==row['sourceSha256']
        for profile in row['compileAttempts']:
            assert profile['realLinkSucceeded'] and not profile['byteExact']
            jobs.append((profile,len(jobs)))
    assert len(historical)==12 and len(jobs)==14
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:current=list(pool.map(compile_current,jobs))
    raw=(json.dumps(current,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-glyph334-current-20261101.json.gz';path.write_bytes(gzip.compress(raw,mtime=0))
    reports=[]
    for tag in ('layout329','best333'):
        script='evidence/application/save_core_glyph_'+tag+'_fixtures_20261101.py'
        process=subprocess.run([sys.executable,'-I','-S',str(ROOT/script)],cwd=ROOT,capture_output=True,text=True,timeout=600)
        assert process.returncode==0,(script,process.stdout[-500:],process.stderr[-2000:])
        p='evidence/application/save-core-glyph-'+tag+'-20261101.json';d=json.loads((ROOT/p).read_text())
        packed=(ROOT/d['sidecar']['path']).read_bytes();assert sha(packed)==d['sidecar']['sha256'] and sha(gzip.decompress(packed))==d['sidecar']['caseSha256']
        reports.append(dict(path=p,sha256=sha((ROOT/p).read_bytes()),producer=script,producerSha256=sha((ROOT/script).read_bytes()),sidecar=d['sidecar']))
    a=json.loads((ROOT/reports[0]['path']).read_text());b=json.loads((ROOT/reports[1]['path']).read_text())
    assert a['sidecar']['caseSha256']==CASE329 and a['nativeOwnCodeOffsets']==list(range(0,616,4))
    assert (a['cases'],a['actualTopReturns'],a['actualNativeHelperReturns'],a['providers'])==(630,1260,25692,0)
    assert (b['cases'],b['actualCompiledTopReturns'],b['actualNativeHelperReturns'],b['actualWrongCReturns'],b['wrongRejects'],b['wrongPositives'])==(630,630,12846,6,5,1)
    result=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,uniqueNativeFunctions=1,uniqueNativeBytes=620,
        sourceHypotheses=12,compilingHypotheses=12,genuineCompilerLinkProfiles=14,exactSourceUnits=0,
        actualOriginalTopReturns=630,actualCompiledTopReturns=1260,actualTopReturns=1890,actualNativeHelperReturns=38538,
        actualWrongCReturns=6,wrongRejects=5,wrongPositives=1,providers=0,observedNativeCodeInstructions=154,
        preferredSource=history['bestSource'],bestSameOffsetBytes=560,
        history=dict(path=archive_path,sha256=sha((ROOT/archive_path).read_bytes())),reports=reports,
        currentCompilerProvenance=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),contentSha256=sha(raw)),
        generatorSha256=sha(Path(__file__).read_bytes()),limits=history['limits']+a['limits']+b['limits'])
    path=ROOT/'evidence/lanes/save-core/glyph334-20261101.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(hypotheses=12,profiles=14,exact=0,actualTopReturns=1890,wrongReturns=6,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
