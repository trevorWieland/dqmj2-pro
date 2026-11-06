from pathlib import Path
import copy
import json
from types import SimpleNamespace
import arm7_host_callee_word_context_v3_20261101 as context
from project import ROOT,sha256,write_json

def main():
    ref=json.loads(context.REFERENCE.read_text());expected={0x03804c00:2,0x03804c7c:1,0x03804c58:1,0x037fbb78:1}
    if context.validate(ref)!=expected:raise ValueError('Positive complete typed/native proof contexts differ')
    child=SimpleNamespace(ARGUMENTS={'arm7':{0x100:7},'arm9':{0x200:9}});before=copy.deepcopy(child.ARGUMENTS)
    if context.apply(child,'child.srl')['applied']or child.ARGUMENTS!=before:raise ValueError('Child-program draft namespace was modified')
    context.apply(child,'')
    if child.ARGUMENTS!={'arm7':{0x100:7,**expected},'arm9':{0x200:9}}:raise ValueError('Atomic bounded host argument update or unrelated preservation differs')
    controls=[]
    def reject(name,path,value):
        bad=copy.deepcopy(ref);target=bad
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value
        try:context.validate(bad)
        except(ValueError,KeyError,StopIteration)as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Unqualified draft callee hint survived '+name)
    for name,path,value in [('credit',('sourceCredit',),1),('accepted-edit',('acceptedSourceOverridesPermitted',),True),('program-scope',('qualifiedHostOnly',),False),('version',('schemaVersion',),2),('missing-proof',('proofs',),ref['proofs'][:-1])]:reject(name,path,value)
    for i in range(4):
        for name,path,value in [('callee',('calleeAddress',),'0x3804c60'),('words',('semanticWords',),4),('report',('proofReportSha256',),'0'*64),('controls',('controlsSha256',),'0'*64),('generator',('proofGeneratorSha256',),'0'*64),('source',('nativeRowIdentity','sourceSha256'),'0'*64),('mode',('nativeRowIdentity','mode'),'thumb'),('module',('nativeRowIdentity','module'),'arm7-main'),('processor',('nativeRowIdentity','processor'),'arm9'),('program',('nativeRowIdentity','program'),'child.srl'),('size',('nativeRowIdentity','bytes'),4),('module-hash',('nativeRowIdentity','inputModuleSha256'),'0'*64),('native-hash',('nativeRowIdentity','targetSha256'),'0'*64)]:reject(str(i)+'-'+name,('proofs',i)+path,value)
    result=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),context=Path(context.__file__).name,contextSha256=sha256(context.__file__),referenceSha256=sha256(context.REFERENCE),qualifiedWordCounts={hex(k):v for k,v in expected.items()},negativeControlCount=len(controls),negativeControls=controls,childNamespaceUnchanged=True,unrelatedExistingHintsAndArm9Preserved=True,sourceCredit=0,acceptedEdits=0)
    output=ROOT/'evidence/verification/arm7-host-callee-word-context-v3-controls-20261101.json';write_json(output,result);print(json.dumps(dict(controls=len(controls),sha256=sha256(output),sourceCredit=0)),flush=True)
if __name__=='__main__':main()
