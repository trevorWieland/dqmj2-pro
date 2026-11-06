import gzip
import hashlib
import json
import sys

from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import measured_module
import wave20261102_battle_fifth_packet01 as P
import unicorn
import wave20261102_battle_fifth_fixture02 as F

LANE=ROOT/'evidence/lanes/parallel-wave20261102/battle-fifth'
SOURCE=ROOT/'src/ov001/parallel_wave20261102/battle-fifth/packet01'


def negative_sources(template,entry):
    if entry==0x21DF680:
        wrong_return=template.replace('return 0U;','return 2U;').replace('return 1U;','return 0U;').replace('return 2U;','return 1U;')
        return[('wrong-return',wrong_return),('wrong-handle-word',template.replace('handle = native_fn_ov001_021dcfa0(','handle = 255U & native_fn_ov001_021dcfa0(')),('wrong-counter-sign',template.replace('s8 *, 0x30) >= 0x1E','u8 *, 0x30) >= 0x1E'))]
    return[('wrong-return',template.replace('return 0U;','return 1U;')),('wrong-raw-byte',template.replace('field_1 = 0x33;','field_1 = 0x34;')),('wrong-counter-width',template.replace('field_38 = (s32)','field_38 = (s8)'))]


def main():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':
        raise ValueError('Battle adjacent pinned runtime differs')
    inputs=LANE/'packet02-inputs.json'
    for pin in read_json(inputs)['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:
            raise ValueError(('Battle adjacent frozen input changed',pin['path']))
    main_info,main,unused=measured_module('main')
    module_info,overlay,unused=measured_module('ov001')
    matches=[]
    functions=[]
    all_traces=[]
    top_returns=0
    for entry,size in F.SIZES.items():
        address=format(entry,'08x')
        path=SOURCE/address/('native_ov001_'+address+'.c')
        match,body=P.build(path,'adjacent-'+address)
        matches.append(match)
        images={}
        controls=[]
        template=path.read_text()
        for ordinal,(label,text)in enumerate(negative_sources(template,entry)):
            if text==template:
                raise ValueError('Battle adjacent control source site missing')
            full_label='a'+address[-4:]+'-'+str(ordinal)
            directory=P.WORK/'controls'/full_label
            directory.mkdir(parents=True,exist_ok=True)
            source=directory/path.name
            source.write_text(text)
            source.with_name('context.h').write_bytes(path.with_name('context.h').read_bytes())
            origin=0x2650000+ordinal*0x2000
            proof,image=P.build(source,full_label,origin)
            images[origin]=image
            controls.append(dict(label=label,origin=origin,proof=proof,rejected=0,positive=0,actualTopReturns=0))
        pcs=set()
        cases=0
        for profile in F.profiles(entry):
            original_vm=F.Machine(main,overlay,images,profile)
            original=original_vm.run(entry)
            source_vm=F.Machine(main,overlay,images|{entry:body},profile)
            source=source_vm.run(entry)
            errors=[F.model(original_vm,original),F.model(source_vm,source)]
            differences=[key for key in ['registers','cpsr','stateHex','writes','provided','memory','rngState','nativeEntries','nativePhysicalReturns','topReturn']if original[key]!=source[key]]
            if any(errors)or differences:
                write_json(LANE/'packet02-failure.json',dict(profile=profile,modelErrors=errors,differences=differences,original=P.compact(original),source=P.compact(source)))
                raise ValueError(('Battle adjacent model/physical difference',address,profile['ordinal'],errors,differences))
            results=[dict(kind='native',**P.compact(original)),dict(kind='source',**P.compact(source))]
            top_returns+=2
            if profile['controlCase']:
                for control in controls:
                    vm=F.Machine(main,overlay,images,profile)
                    result=vm.run(control['origin'])
                    model_errors=F.model(vm,result)
                    control['actualTopReturns']+=1
                    control['rejected'if model_errors else'positive']+=1
                    results.append(dict(kind=control['label'],modelErrors=model_errors,**P.compact(result)))
                    top_returns+=1
            all_traces.append(dict(profile=profile,results=results,originalAndSourceAll8MiBPhysicalStateEqual=True,independentRawStateModelPassed=True))
            pcs.update(original['ownPcs'])
            cases+=1
            if cases%64==0:
                print('battle adjacent',address,cases,flush=True)
        if any(not row['rejected']for row in controls):
            raise ValueError(('Battle adjacent negative control never rejected',address))
        functions.append(dict(address=hex(entry),bytes=size,cases=cases,source=match['source'],negativeEvidence=controls,nativeInstructionAddresses=sorted(pcs)))
    raw=json.dumps(all_traces,sort_keys=True,separators=(',',':')).encode()
    trace=LANE/'packet02-traces.json.gz'
    trace.write_bytes(gzip.compress(raw,mtime=0))
    write_json(LANE/'packet02-match.json',dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=module_info['sha256'],mainSha256=main_info['sha256'],allPassed=True,matches=matches,functions=functions,canonicalMatchedFunctions=2,canonicalMatchedBytes=780,sourceCreditPendingSharedAcceptance=True,producer='wave20261102_battle_fifth_packet02.py',producerSha256=sha256(__file__),inputs=dict(path=inputs.relative_to(ROOT).as_posix(),sha256=sha256(inputs)),cases=len(all_traces),actualNativeAndSourceCallerReturns=len(all_traces)*2,actualTopReturnsIncludingControls=top_returns,actualNativeHelperReturns=0,completePhysicalRegistersCpsrRawCallsOrderedWritesAndAll8MiBRamEqual=True,independentRawStateModelPassed=True,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Two complete ordinary C controller extents and genuine pinned MW links, qualified nativeSymbolEntries and fresh objects on every replay.','All256 raw phase bytes per controller plus bounded signed counter rollover, full-word sentinel/low16 argument and sequential raw-byte phase transitions are independently modeled.','Native/source pairs compare all physical registers/CPSR/raw call words/writes/all8MiB RAM. Focused whole-C controls run only on marked active/boundary profiles.','External callees are supplied word boundaries with no memory effects and adversarial caller-saved/NZCV clobbers; original callee execution/source credit remains zero. Raw byte/word fields carry no inferred game meaning.']))
    print(dict(functions=2,bytes=780,pairs=len(all_traces),actualTopReturns=top_returns),flush=True)


if __name__=='__main__':
    main()
