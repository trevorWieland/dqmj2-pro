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
import source_current_callee338_20261101 as N
from source_word_inputs_20261031 import apply_context as apply_words,calibrate
from link_runtime_unit import measured_module


def sha(raw):return hashlib.sha256(raw).hexdigest()


def controls():
    count=calibrate();catalogue=N.catalogue()
    context='extern u32 func_0203694c();\n'
    changed,edits=apply_words(context,catalogue)
    assert changed=='extern u32 func_0203694c(u32 arg0, u32 arg1);\n' and len(edits)==1
    for text in ('extern u32 func_0203694c(void);\n','extern u32 func_0203694c(u32 a, u32 b);\n'):
        assert apply_words(text,catalogue)==(text,[])
    assert apply_words(context,catalogue,processor='arm7')==(context,[])
    assert apply_words(context,catalogue,program='utility-child')==(context,[])
    assert all(r['identity']['address']!=0x01FFF610 for r in catalogue['functions'])
    assert any(r['identity'][4]==0x01FFF610 and not all(r.get('used',[])) for r in catalogue['excluded'])
    return count+6,catalogue


def compile_current(job):
    prior,index=job
    spec=importlib.util.spec_from_file_location('callee345_'+str(index),ROOT/'evidence/application/save_core_historical_link_20261031.py')
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    b.ENTRY,b.LENGTH,b.NAME=int(prior['address'],0),prior['bytes'],prior['name']
    b.SOURCE,b.FLAGS=prior['source'],prior['flags'];b.COMPILER,b.COMPILER_HASH=prior['compilerPath'],prior['compilerSha256']
    b.WORK='work/save-core/callee345/'+str(index)
    arm=measured_module('main')[1];row,body=b.build(arm[b.ENTRY-0x02000000:b.ENTRY-0x02000000+b.LENGTH])
    assert (row['compiledBytes'],row['sameOffsetBytes'])==(prior['compiledBytes'],prior['sameOffsetBytes'])
    assert sha(body)==prior['linkedBinarySha256'] and not row['exactByteEqual']
    return row


def main():
    calibrated,catalogue=controls();report_path='evidence/lanes/save-core/app-large339-20261101.json';d=json.loads((ROOT/report_path).read_text())
    sidecar=d['fullProvenanceSidecar'];packed=(ROOT/sidecar['path']).read_bytes();raw=gzip.decompress(packed)
    assert sha(packed)==sidecar['sha256'] and sha(raw)==sidecar['uncompressedSha256']
    rows=json.loads(raw);jobs=[];sources={}
    for row in rows:
        if row.get('source'):
            assert sha((ROOT/row['source']).read_bytes())==row['sourceSha256'];sources[row['source']]=row['sourceSha256']
            for fragment in row.get('decompilation',{}).get('flatFragments',[]):
                assert sha((ROOT/fragment['path']).read_bytes())==fragment['sha256'];sources[fragment['path']]=fragment['sha256']
        for p in row.get('compileAttempts',[]):
            if p.get('realLinkSucceeded'):jobs.append((p,len(jobs)))
    assert len(rows)==38 and len(jobs)==52
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:current=list(pool.map(compile_current,jobs))
    raw=(json.dumps(current,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-callee345-current-20261102.json.gz';path.write_bytes(gzip.compress(raw,mtime=0))
    result=dict(schema=1,sourceCredit=0,newFunctions=0,newBytes=0,selectedFunctions=38,selectedNativeBytes=29508,
        sourceHypotheses=36,compiledHypotheses=26,genuineLinkedProfiles=52,nearUnits=0,exactSourceUnits=0,nativeQualifiedUnits=0,
        calibrationControls=calibrated,currentSourceViews=len(catalogue['functions']),newViewsRelativeTo83=catalogue['newRelativeTo83'],excludedCurrentViews=len(catalogue['excluded']),
        sources=[dict(path=p,sha256=h) for p,h in sorted(sources.items())],
        inputReport=dict(path=report_path,sha256=sha((ROOT/report_path).read_bytes())),historicalCompilerArchive=sidecar,
        catalogue=dict(path=N.CATALOGUE,sha256=sha((ROOT/N.CATALOGUE).read_bytes()),references=catalogue['referenceSidecar']),
        comparison=dict(path='evidence/lanes/save-core/current-callee345-comparison-20261102.json',sha256=sha((ROOT/'evidence/lanes/save-core/current-callee345-comparison-20261102.json').read_bytes())),
        currentCompilerProvenance=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),contentSha256=sha(raw)),generatorSha256=sha(Path(__file__).read_bytes()),
        limits=catalogue['limits']+['These38 identities reuse earlier drafts.36 source hypotheses and26 compiles are stage counts,not new recovery coverage.',
        'The new320-byte68C14 compile has only85 same-offset bytes.6CCB4 regresses136to133;no blanket current-catalogue improvement is claimed.',
        'All original accepted and prior preferred sources remain unchanged. Opaque source input counts do not establish native arity,pointed layout,return signatures or coherent selected C interfaces.',
        'The replay uses frozen private reference blobs/current source and actual compiler/link outputs,not Root paths,historical work objects or live mutable registry state.'])
    path=ROOT/'evidence/lanes/save-core/callee345-20261102.json';path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(selected=38,drafts=36,compiled=26,profiles=52,exact=0,sourceCredit=0,reportSha256=sha(path.read_bytes()))))


if __name__=='__main__':main()
