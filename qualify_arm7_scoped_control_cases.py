import copy
import hashlib
import struct

import match_runtime
from project import ROOT,configuration,read_json,write_json,sha256
from qualify_arm7_scoped_control import walk
from wave20261106_arm7_accepted_source_reuse_flow import analyze


def qualify(image,base,entries):
    results=[]
    for kind,lane,address,size in [('channel','arm7-wl-channel-next-proposal',0x027e990c,652),('rtc','arm7-rtc-loop-next-proposal',0x027f60b4,1156)]:
        proposal=read_json(ROOT/f'evidence/lanes/parallel-wave20261106/{lane}/proposal.json')
        original_flow=proposal['nativeBoundary']['flow']
        assert analyze(image,base,address,'arm',entries)==original_flow
        def run(data,mode='arm',length=size,foreign=None):
            assert not any(address<a<address+length for a in entries|set(foreign or []))
            flow=analyze(data,base,address,'arm',entries)
            path=ROOT/f'work/scoped-control-qualification/{kind}-flow.json'
            write_json(path,flow)
            row=dict(address=hex(address),mode=mode,bytes=length,flow=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),
                entryReachableInstructionBytes=flow['reachableInstructionBytes'],actualLiteralReadBytes=flow['literalReadBytes'],
                nativeSpanSha256=hashlib.sha256(data[address-base:address-base+length]).hexdigest())
            return walk(row,data,base,kind)
        positive=run(image)
        cases=[]
        def reject(label,data=image,**kwargs):
            try:run(data,**kwargs)
            except (AssertionError,ValueError)as error:cases.append(dict(case=label,rejected=True,error=type(error).__name__))
            else:raise AssertionError(('Unsafe scoped native control accepted',label))
        def changed(at,word):
            data=bytearray(image);struct.pack_into('<I',data,at-base,word);return data
        reject('thumb-mode',mode='thumb')
        reject('foreign-interior-entry',foreign=[address+4])
        if kind=='channel':
            reject('thumb-callback-target',changed(0x027e9b8c,0x027f4e7d))
            reject('interior-callback-target',changed(0x027e9b8c,0x027f4e80))
            reject('unknown-callback-target',changed(0x027e9b90,0x027f4df0))
            reject('callback-register-clobber',changed(0x027e9934,0xe3a09000))
            reject('wrong-BX-register',changed(0x027e99d4,0xe12fff18))
            branch=0xea000000|(((0x027e9930-(0x027e9914+8))//4)&0xffffff)
            reject('entry-into-predicate-middle',changed(0x027e9914,branch))
            reject('unbounded-computed-PC',changed(0x027e9934,0xe08ff100))
        else:
            reject('injected-return',changed(0x027f6524,0xe12fff1e))
            outside=address+size+16
            branch=0xea000000|(((outside-(0x027f6524+8))//4)&0xffffff)
            reject('unknown-external-edge',changed(0x027f6524,branch))
            switch=original_flow['boundedExecutableSwitches'][0];at=int(switch['dispatch'],0)
            compare=struct.unpack_from('<I',image,at-base-4)[0]
            reject('unbounded-switch',changed(at-4,(compare&~4095)|0x401))
            case=int(switch['tableAddresses'][0],0);word=struct.unpack_from('<I',image,case-base)[0]
            reject('call-in-place-of-case-edge',changed(case,word|0x01000000))
            first=original_flow['literalReads'][0];origin=int(first['origin'],0);word=struct.unpack_from('<I',image,origin-base)[0]
            reject('code-literal-overlap',changed(origin,(word&~4095)))
            reject('wrong-loop-envelope',length=size+4)
        results.append(dict(kind=kind,address=hex(address),bytes=size,positive=positive,negativeCases=cases,
            noSharedCollectorNamespaceOrReturnGuardModified=True))
    return results


if __name__=='__main__':
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    raw=config['rom'].read_bytes()[624640:624640+160048];image=raw[63636:160024];base=0x027e0000
    import link_arm7_bulk_20261030 as linker
    modules,functions=linker.namespace('');entries={a for a,r in functions.items()if r['module']=='arm7-main'}
    results=qualify(image,base,entries)
    output=ROOT/'evidence/verification/arm7-channel-rtc-scoped-native-control-qualification-20261106.json'
    write_json(output,dict(passed=True,sourceCredit=0,positiveCases=2,negativeCases=sum(len(r['negativeCases'])for r in results),records=results,
        originalReturnValidatorSha256=sha256(ROOT/'qualify_arm7_pm_mic_boundaries_v1_20261106.py'),
        scopedQualifierSha256=sha256(ROOT/'qualify_arm7_scoped_control.py'),caseGeneratorSha256=sha256(__file__),
        originalValidatorsChanged=False,newSourceOrStorageCredit=0))
    print(dict(passed=True,positive=2,negative=sum(len(r['negativeCases'])for r in results)))
