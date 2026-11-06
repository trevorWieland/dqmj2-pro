import copy
import json
import os
import shutil
import subprocess
from pathlib import Path
from project import ROOT,configuration,read_json,sha256,write_json
import qualify_arm9_overlay_reference_inputs_20261105 as Q
from qualify_explicit_c_frontend_20261102 import signature
from recovery_registry import batches

WORK=ROOT/'work/overlay-reference-v13/controls'
OUTPUT=ROOT/'evidence/lanes/parallel-wave20261105/overlay-reference-input-v13/controls.json'


def main():
    WORK.mkdir(parents=True,exist_ok=True)
    before={p:sha256(ROOT/p) for p in ['recovery.json','source-preferences.json','manifest.json',Q.REPORT,'verify_committed_source_inputs_v8_20261101.py','verify_committed_source_inputs_v12_20261105.py','logs/integration/cohort157-source-input-audit-20261101.txt','evidence/verification/cohort157-committed-source-inputs-v12-20261105.json']}
    report=Q.committed(Q.REPORT)
    seed=Q.committed('provenance/seed-manifest.json')
    manifest=Q.committed(Q.MANIFEST)
    declared={p['path']:p['sha256'] for p in manifest['privateComparisonInputs']}
    actual=batches()
    serialized=json.dumps(actual,sort_keys=True)
    projected,consumers=Q.project_batches(actual,report,declared)
    Q.require(json.dumps(actual,sort_keys=True)==serialized,'Projection mutated its input')
    for old,new in zip(actual,projected):
        expected=copy.deepcopy(old)
        if old['report']==Q.REPORT:del expected['sourceHashes'][Q.REFERENCE]
        Q.require(expected==new,'Unrelated registered input changed by projection')
    checks=[]

    def reject(label,callback):
        try:callback()
        except (ValueError,AssertionError) as error:checks.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid overlay reference policy accepted: '+label)

    for index,label in enumerate(['id','base','initialized','bss','ctor-start','ctor-end','file-id','compression-flags']):
        wrong=list(Q.ENTRY);wrong[index]^=4
        reject('wrong-overlay-'+label,lambda value=wrong:Q.validate_entry(value))
    rom=configuration()['rom'].read_bytes()
    reference=(ROOT/Q.REFERENCE).read_bytes()
    positive=Q.derive(rom,reference,seed)
    wrong=bytearray(rom);wrong[0x50]^=4
    reject('tampered-original-ROM',lambda:Q.derive(bytes(wrong),reference,seed))
    del wrong
    wrong_reference=bytearray(reference);wrong_reference[-1]^=1
    reject('tampered-extracted-overlay',lambda:Q.derive(rom,bytes(wrong_reference),seed))
    reject('truncated-extracted-overlay',lambda:Q.derive(rom,reference[:-4],seed))
    wrong_seed=copy.deepcopy(seed)
    next(m for m in wrong_seed['modules'] if m['name']=='ov000')['base']='0x21d7244'
    reject('wrong-measured-overlay-mapping',lambda:Q.derive(rom,reference,wrong_seed))
    batch=next(b for b in actual if b['report']==Q.REPORT)
    for label,modify in [('unknown-consumer',lambda b:b.update(report='evidence/matches/unqualified.json')),
                         ('changed-overlay-pin',lambda b:b['sourceHashes'].update({Q.REFERENCE:'0'*64})),
                         ('extra-unknown-overlay',lambda b:b['sourceHashes'].update({'extract/arm9_overlays/ov001.bin':Q.REFERENCE_SHA})),
                         ('missing-exact-overlay',lambda b:b['sourceHashes'].pop(Q.REFERENCE))]:
        value=copy.deepcopy(batch);modify(value)
        reject(label,lambda value=value:Q.project_batches([value],report,declared))
    reject('duplicate-overlay-consumer',lambda:Q.project_batches([batch,batch],report,declared))
    bad_declared=copy.deepcopy(declared);bad_declared[Q.REFERENCE]='f'*64
    reject('wrong-private-reference-declaration',lambda:Q.project_batches([batch],report,bad_declared))
    row=report['matches'][0]
    mutations=[('wrong-CPU','processor','arm7'),('wrong-program','program','child'),('wrong-module','module','ov000'),('unqualified-Thumb-caller','mode','thumb'),('unknown-address','address','0x207a16c'),('partial-span','bytes',68),('original-executable-source','source',Q.REFERENCE),('changed-source-pin','sourceSha256','0'*64),('unproven-native-match','exactAfterDeclaredRelocation',False)]
    for label,key,value in mutations:
        changed=copy.deepcopy(row);changed[key]=value
        reject(label,lambda changed=changed:Q.row_inputs(changed))
    for flag in ['@hidden-options','-Iextract/arm9_overlays','extract/arm9_overlays/ov000.bin','-thumb']:
        changed=copy.deepcopy(row);changed['compilerFlags'].append(flag)
        reject('injected-compiler-input-'+flag,lambda changed=changed:Q.row_inputs(changed))
    for name in ['src/../extract/image.h','src/a/../foreign.h','src/../../foreign.h','C:/foreign.h','src/a\\foreign.h','extract/arm9_overlays/ov000.bin']:
        reject('invalid-header-'+name,lambda name=name:Q.repository_path(name,'.h'))
    from verify_committed_source_inputs_v13_20261105 import output_path
    for name in ['recovery.json','manifest.json','evidence/verification/cohort157-committed-source-inputs-v12-20261105.json','../outside.json']:
        reject('unsafe-output-'+name,lambda name=name:output_path(157,name))
    reject('mislabelled-cohort',lambda:output_path(158,'evidence/lanes/parallel-wave20261105/overlay-reference-input-v13/wrong.json'))
    source=row['source']
    documents={source:(ROOT/source).read_text(),**{p['path']:(ROOT/p['path']).read_text() for p in row['sourceDependencies']}}
    Q.text_closure(documents,source)
    for label,text in [('spaced-unclosed-include','# include "unknown.h"'),('macro-include','#include UNKNOWN'),('angle-include','#include <unknown.h>'),('prefix-directive','#pragma once'),('asm','asm { nop; }'),('incbin','.incbin "extract/arm9_overlays/ov000.bin"'),('digraph-include','%:include "unknown.h"'),('trigraph-include','??=include "unknown.h"'),('continued-include','#include '+chr(92)+'\n "context000.h"'),('embedded-binary',chr(0))]:
        changed=dict(documents);changed[source]=text
        reject(label,lambda changed=changed:Q.text_closure(changed,source))
    body_controls=[]
    original=signature(ROOT/row['object'],row['name'])
    text=(ROOT/row['source']).read_text()
    header=(ROOT/row['sourceDependencies'][0]['path']).read_text()
    cases=[('wrong-C-constant',text.replace('point.x=16','point.x=17'),header,[]),('wrong-relocation-symbol',text.replace('native_fn_ov000_02215698','native_fn_wrong_getter'),header.replace('native_fn_ov000_02215698','native_fn_wrong_getter'),[]),('actual-Thumb-object',text,header,['-thumb'])]
    for label,body,includes,extra in cases:
        directory=WORK/label;directory.mkdir(parents=True,exist_ok=True)
        source_path=directory/'source.c';source_path.write_text(body)
        (directory/'context000.h').write_text(includes)
        output=directory/'source.o'
        command=[str(ROOT/row['compiler']),*row['compilerFlags'],*extra,'-c',str(source_path),'-o',str(output)]
        process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=120)
        Q.require(process.returncode==0,('Actual negative compile failed',label,process.stdout,process.stderr))
        current=signature(output,row['name'])
        if label=='actual-Thumb-object':reject(label,lambda:Q.arm_mapping(output,row['name']))
        else:
            Q.require(original!=current,'Whole function/relocation comparison failed to reject real wrong object')
            if label=='wrong-C-constant':Q.require(original['bytes']==current['bytes'] and original['relocations']==current['relocations'] and original['bodySha256']!=current['bodySha256'],'Real wrong constant control was not same-sized with unchanged relocations')
            else:Q.require(original['bodySha256']==current['bodySha256'] and original['relocations']!=current['relocations'],'Relocation-only real negative did not isolate original symbol identity')
            checks.append(dict(case=label,rejected=True,original=original,wrong=current))
        body_controls.append(dict(case=label,compilerSha256=sha256(ROOT/row['compiler']),sourceSha256=sha256(source_path),objectSha256=sha256(output),command=command,exitCode=process.returncode,sourceCredit=0))
    Q.require(before=={p:sha256(ROOT/p) for p in before},'Controls changed original source/registry/evidence scope')
    write_json(OUTPUT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),qualifier=dict(path=Path(Q.__file__).name,sha256=sha256(Q.__file__)),acceptedSourceCommit=Q.SOURCE_COMMIT,negativeControls=checks,negativeControlCount=len(checks),actualCompilerNegativeObjects=body_controls,positiveDerivation=positive,projection=dict(consumers=consumers,inputBatches=len(actual),unchangedOutsideExactlyOneReferencePin=True,inputDocumentUnmodified=True),preservedOriginalHashes=before,limits=['Positive production C99/function/relocation/native link proof is in the separate v13 audit.','All negatives run in memory or new work paths, with no original source/object/report/registry edits, no hash bypass or original verifier monkeypatching.','Thumb is an actual compiled negative for this ARM-only contract; this does not qualify any Thumb consumer.']))
    print(dict(passed=True,negativeControls=len(checks),actualCompilerNegativeObjects=len(body_controls),report=OUTPUT.relative_to(ROOT).as_posix()))


if __name__=='__main__':main()
