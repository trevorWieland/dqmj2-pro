import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
import unicorn
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_setter932_fixture_20261102 as F

SOURCE = ROOT / 'src/overlays/ov000_20261102_raw_setter931'
WORK = ROOT / 'work/ol933-proof'


def build(source, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov000', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('933 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        proof = validate(row, bindings, directory)
        return dict(**row, realLink=proof), (directory / 'caller.bin').read_bytes()
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'}


def main():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('933 pinned runtime differs')
    pins=read_json(ROOT/'evidence/verification/ov000-setter933-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('933 input differs',row['path']))
    mainInfo,arm,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov000')
    match,body=build(SOURCE/'source.c','source')
    byteProof,byteBody=build(ROOT/'nonmatching/overlay-lane/20261102-setter931-byte-domain/source.c','byte-domain')
    controls=[]
    images={}
    template=(SOURCE/'source.c').read_text()
    variants=[('wrong-sign-return',template.replace('return value;', 'return (u32)(signed char)value;')),('wrong-truncated-return',template.replace('return value;', 'return (u8)value;')),('wrong-byte-store',template.replace('= (u8)value;', '= (u8)(value ^ 1U);'))]
    for index,(name,text)in enumerate(variants):
        if text==template:raise ValueError('933 control mutation site absent')
        directory=ROOT/'nonmatching/overlay-lane/20261102-setter933-controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('933 frozen control differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE/'context.h').read_bytes())
        origin=0x02650000+index*0x2000
        proof,image=build(source,name,origin)
        images[origin]=image
        controls.append(dict(name=name,origin=origin,proof=proof,actualTopReturns=0,rejected=0,positive=0))
    traces=[]
    pcs=set()
    totals=dict(pairs=0,actualTopReturns=0,byteFacadeDomainReturns=0,actualNativeHelperReturns=0,suppliedCalls=0)
    for p in F.profiles():
        results=[]
        failures=[]
        for kind,start in [('native',F.ENTRY),('source',F.ENTRY)]+[(r['name'],r['origin'])for r in controls]:
            installed=images|({F.ENTRY:body}if kind=='source'else{})
            vm=F.Machine(arm,overlay,installed,p)
            result=vm.run(start)
            result['kind']=kind
            results.append(result)
            failures.append(F.model(vm,result))
        if failures[0]or failures[1]:raise ValueError(('933 independent raw-word model',p['ordinal'],failures[:2]))
        fields=['registers','cpsr','memory','outputBytes','writes','ownPcs','properTopReturnPc']
        differences=[k for k in fields if results[0][k]!=results[1][k]]
        if differences:raise ValueError(('933 full physical state differs',p['ordinal'],differences))
        if p['word']<256:
            vm=F.Machine(arm,overlay,images|{F.ENTRY:byteBody},p)
            byteResult=vm.run(F.ENTRY)
            if F.model(vm,byteResult):raise ValueError('933 zero-extended byte facade differs')
            totals['byteFacadeDomainReturns']+=1
        totals['pairs']+=1
        totals['actualTopReturns']+=2
        pcs.update(results[0]['ownPcs'])
        for index,control in enumerate(controls):
            control['actualTopReturns']+=1
            control['rejected'if failures[index+2]else'positive']+=1
        traces.append(dict(profile=p,results=[compact(r)|dict(completeRamSha256=hashlib.sha256(r['memory']).hexdigest())for r in results],modelFailures=failures,physicalDifferences=differences))
    if pcs!=set(range(F.ENTRY,F.ENTRY+12,4))or any(not r['rejected']for r in controls):raise ValueError('933 instruction coverage/controls incomplete')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov000-setter933-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],matches=[match],alreadyAcceptedFunction=True,sourceCredit=0,newMatchedFunctions=0,newMatchedBytes=0,canonicalMatchedFunctions=1,canonicalMatchedBytes=16,proposedApi='u32(u32)',byteDomainAlternative=byteProof,totals=totals,negativeEvidence=controls,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allOwnCodeObserved=dict(codeBytes=12,literalBytes=4,unclassifiedBytes=0),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Existing16-byte function has zero new source/function/byte credit. New raw-word C matches complete original bytes/relocations through genuine MWLD and requires coordinated preference/interface review before adoption. Old selected s8 source is unchanged.','Original LDR R1,global; STRB R0,[R1,#0x7C0]; BX LR stores low8 and preserves ALL incoming R0 bits. Profiles exhaust low8 values and seven high-word patterns, including zero-extension and canonical sign-extension words. No original formal typedef or complete game input domain is inferred.','Separate u8 facade also compiles to16 matching bytes and is checked only on the zero-extended0..255 domain. Main0203DB58 LDRB caller evidence is external Root-owned and not reexecuted here. The wider raw facade avoids inventing required sign/zero extension.','Full physical register/CPSR/RAM including stack, exact onebyte store/canaries and actual BX LR/SP/callee-saved return are checked. Three independently compiled wrong-C bodies properly return and reject, while valid positives remain labeled.','No lower providers, heap/hardware/scene/persistence meaning, application edits or host/device execution. Shared registry and accepted source remain unchanged.'])
    write_json(ROOT/'evidence/matches/ov000-20261102-raw-setter933.json',report)
    print(dict(totals=totals,newSourceCredit=0,controls=[{k:r[k]for k in ['name','actualTopReturns','rejected','positive']}for r in controls]),flush=True)

if __name__=='__main__':main()
