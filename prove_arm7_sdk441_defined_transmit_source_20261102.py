import hashlib
import json
import re
from pathlib import Path
import match_runtime
import compile_arm7_sdk435_intr_transmit_compiler_20261102 as compiler
import compile_arm7_core133_large1272_virtual_20261101 as diagnostic
from project import ROOT,sha256,write_json

def main():
    seed=next(r for r in json.loads(compiler.linker.PROFILE.read_text(encoding='utf-8'))['units']if r['name']=='TxqEndData');work=ROOT/'work/arm7-bulk-20261030/sdk441-defined-transmit-source';row,link,current=compiler.compile_unit(seed,ROOT/seed['source'],work/'current');p=ROOT/seed['source'];text=p.read_text(encoding='utf-8');text=re.sub(r'(?m)^#include "([^"]+)"\s*$',lambda m:(p.parent/m[1]).read_text(encoding='utf-8'),text);statement='    pCounter += LoadHigh(&pFrm->MacHeader.Tx.rsv_RetryCount);';marker='    IssueMaDataConfirm(pBufMan, pReq);'
    if statement in text or text.count(marker)!=1:raise ValueError('Defined source/dead-expression comparison shape changed')
    original_reference=ROOT/'deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/libraries/wl_arm7/src/TxCtrl.c'
    if statement not in original_reference.read_text(encoding='utf-8',errors='replace'):raise ValueError('Raw pinned reference no longer contains this dead statement')
    historical,proof=diagnostic.build(seed,text.replace(marker,statement+'\n'+marker),work/'historical-comparison',link['bindings'])
    if historical!=current:raise ValueError('Removing only unused pointer arithmetic changes current native bytes')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),referenceSource=original_reference.relative_to(ROOT).as_posix(),referenceSourceSha256=sha256(original_reference),removedReferenceStatement=statement.strip(),reason='An unused pointer increment can exceed the C object; preserve defined source without inventing retry-counter effects.',currentSource=seed['source'],currentSourceDependencies=seed['sourceDependencies'],currentObject=row['object'],currentObjectSha256=row['objectSha256'],currentRealLink=link,historicalComparison=proof,genuineLinkedExact=True,bytes=len(current),targetSha256=seed['targetSha256'],behavioralReturnCredit=0,rawAndPriorClosedReferenceUnchanged=True);write_json(ROOT/'evidence/attempts/arm7-sdk441-defined-transmit-source-20261102.json',result);print(json.dumps(dict(definedSourceByteExact=True,bytes=len(current),behavioralReturns=0)),flush=True)

if __name__=='__main__':main()
