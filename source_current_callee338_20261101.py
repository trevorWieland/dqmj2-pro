import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT)]
from audit_zero_argument_calls_20261031 import signature
from source_word_inputs_20261031 import split_parameters,word_parameter,apply_context as apply_words

CATALOGUE='evidence/lanes/save-core/current-callee338-20261101.json'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def definition(text,row):
    address=f"{row['address']:08x}"
    names=[row['name']]
    names+=sorted(set(re.findall(r'\b([A-Za-z_]\w*'+address+r'\w*)\s*\(',text)))
    parsed=[(name,signature(text,name)) for name in dict.fromkeys(names)]
    parsed=[(name,value) for name,value in parsed if value is not None]
    if len(parsed)==1:return parsed[0][0],parsed[0][1],'address-or-record-name'
    if len(parsed)>1:return None
    candidates=[]
    for name in re.findall(r'(?m)^[^;{}\n]+?\b([A-Za-z_]\w*)\s*\([^;{}]*?\)\s*\{',text):
        if name in ('if','for','while','switch'):continue
        value=signature(text,name)
        if value is not None:candidates.append((name,value))
    if len(candidates)==1:return candidates[0][0],candidates[0][1],'single-definition-source-hypothesis'
    return None


def catalogue():
    d=json.loads((ROOT/CATALOGUE).read_text());packed=(ROOT/d['referenceSidecar']['path']).read_bytes()
    assert sha(packed)==d['referenceSidecar']['sha256'];raw=gzip.decompress(packed)
    assert sha(raw)==d['referenceSidecar']['contentSha256'];refs=json.loads(raw)
    for row in d['functions']:
        text=refs['sources'][row['source']]
        assert sha(text.encode('utf-8'))==row['sourceSha256']
        parsed=signature(text,row['definition']);assert parsed and parsed[0]==row['parameterView']
        parts=split_parameters(parsed[0]);assert len(parts)==row['wordSlots'] and all(word_parameter(p) for p in parts)
        assert all(re.search(r'\b'+re.escape(re.search(r'\b([A-Za-z_]\w*)\s*$',p)[1])+r'\b',parsed[1]) for p in parts)
    return d


def apply(context,processor='arm9',program=''):
    d=catalogue();return apply_words(context,d,processor=processor,program=program)


def main():
    integrator=Path('C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp')
    snapshot_path=ROOT/'evidence/verification/accepted-cohort130-identities-v2-20261101.json'
    raw=snapshot_path.read_bytes();snapshot=json.loads(raw)
    assert sha(raw)=='bde4ac375c06bad0fb7d0df0801e6dd7cf461d02afe532540521ec635dbbca24'
    targets=set();assemblies={};jobs=[]
    for tag in ('314','315','316'):
        q=json.loads((ROOT/f'evidence/lanes/save-core/app-large{tag}-20261101.json').read_text())['queue']['jobs']
        for row in q:
            path=ROOT/row['work']/'input.s'
            if not path.exists():continue
            text=path.read_text();assemblies[row['address']]=text;jobs.append(row)
            targets|={int(v,16) for v in re.findall(r'\bbl\s+func_([0-9a-f]{8})\b',text)}
    functions=[];excluded=[];sources={};seen=set()
    for row in snapshot['functions']:
        if row['processor']!='arm9' or row['program'] or row['module'] not in ('main','itcm','dtcm') or row['address'] not in targets or not row['source'].endswith('.c'):continue
        identity=tuple(row[k] for k in ('processor','program','module','mode','address'));assert identity not in seen;seen.add(identity)
        raw=(integrator/row['source']).read_bytes();assert sha(raw)==row['sourceSha256']
        text=raw.decode('utf-8-sig');found=definition(text,row)
        if found is None:excluded.append(dict(identity=identity,reason='unresolved-definition',source=row['source']));continue
        name,(parameters,body),resolution=found
        if parameters in ('','void'):continue
        parts=split_parameters(parameters)
        names=[re.search(r'\b([A-Za-z_]\w*)\s*$',p) for p in parts]
        used=[bool(n and re.search(r'\b'+re.escape(n[1])+r'\b',body)) for n in names]
        if len(parts)>8 or not all(word_parameter(p) for p in parts) or not all(used):
            excluded.append(dict(identity=identity,reason='unsupported-or-unused-formal',definition=name,parameters=parameters,used=used,source=row['source']));continue
        sources[row['source']]=text
        assert sha(text.encode())==row['sourceSha256']
        functions.append(dict(identity={k:row[k] for k in ('processor','program','module','mode','address')},source=row['source'],sourceSha256=row['sourceSha256'],definition=name,resolution=resolution,parameterView=parameters,wordSlots=len(parts),allFormalsLexicallyUsed=True,originalPrototypeProven=False,nativeRegisterInputProofAdded=False,sourceCredit=0))
    reference=dict(sources=sources,assemblies=assemblies)
    raw=(json.dumps(reference,sort_keys=True,separators=(',',':'))+'\n').encode();path=ROOT/'evidence/vectors/save-core-current-callee338-references-20261101.json.gz';path.write_bytes(gzip.compress(raw,mtime=0))
    old=json.loads((ROOT/'evidence/verification/source-word-inputs83-20261031.json').read_text());oldids={tuple(r['identity'][k] for k in ('processor','program','module','mode','address')) for r in old['functions']}
    missing=sum(tuple(r['identity'][k] for k in ('processor','program','module','mode','address')) not in oldids for r in functions)
    out=dict(schema=1,sourceCredit=0,acceptedCohort=130,snapshotSha256=sha(snapshot_path.read_bytes()),queriedJobs=len(jobs),queriedTargets=len(targets),functions=functions,excluded=excluded,newRelativeTo83=missing,referenceSidecar=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path.read_bytes()),contentSha256=sha(raw)),generatorSha256=sha(Path(__file__).read_bytes()),limits=['Frozen selected C formal lists are caller-drafting hypotheses only,never proof of original ABI or acceptable source-interface closure.', 'Only empty generated extern lists are filled;float/wide/aggregate/variadic and unused-formal placeholders are excluded,not trimmed or reinterpreted.', 'Canonical address aliases and single-definition source fallback are recorded;CPU/program/module scopes remain explicit and ambiguous overlays excluded.', 'Private unmodified current source references and generated assembly are compressed evidence,not new reconstructed/source credit. No Root file is changed.'])
    (ROOT/CATALOGUE).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(jobs=len(jobs),targets=len(targets),wordViews=len(functions),newRelativeTo83=missing,excluded=len(excluded),sourceCredit=0)))


if __name__=='__main__':main()
