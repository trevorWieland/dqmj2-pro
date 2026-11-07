import copy
import hashlib
import re
import match_runtime
from project import ROOT,read_json,write_json,sha256
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from wave20261106_ov000_large_actor_source_second_paths import EVIDENCE
from wave20261106_ov000_large_actor_source_second_bindings import inputs


def qualify(entry,main,inventory):
    if(entry.get('program')or'',entry['processor'],entry['module'],entry['mode'],int(entry['address'],0),entry['bytes'])!=('','arm9','main','arm',0x0202818c,44):raise ValueError('Vector return CPU/program/module/mode/entry/extent differs')
    raw=main[0x2818c:0x2818c+44]
    if hashlib.sha256(raw).hexdigest()!=entry['targetSha256']or not re.search(r'^\S+ kind:function\(arm,size=0x2c\) addr:0x0202818c$',inventory,re.M):raise ValueError('Complete original vector body/canonical boundary differs')
    path=ROOT/entry['sourceUnit']
    if sha256(path)!=entry['sourceSha256']or not re.search(r'void\s+native_main_0202818c\s*\(void\s*\*arg0,\s*void\s*\*arg1\)',path.read_text()):raise ValueError('Preserved accepted vector void declaration differs')
    decoded=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(raw,0x0202818c))
    if[(i.address,i.mnemonic,i.op_str)for i in decoded[-4:]]!=[(0x020281a8,'bl','#0x20028d8'),(0x020281ac,'mov','r1, #0x47'),(0x020281b0,'bl','#0x200235c'),(0x020281b4,'pop','{r3, pc}')]:raise ValueError('Original final serviceR0 forwarding/return changed')
    return decoded


def execute():
    value,image,inventory,records,main_inventory=inputs();main=(ROOT/value['mainImage']['path']).read_bytes();entry=next(e for e in value['executedAcceptedHelpers']if e['address']=='0x202818c');decoded=qualify(entry,main,main_inventory);caller=next(e for e in value['entries']if e['address']=='0x220cd28');origin=0x0220cd94;raw=image[origin-0x021d7240:origin-0x021d7240+8];instructions=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(raw,origin))
    if[(i.mnemonic,i.op_str)for i in instructions]!=[('bl','#0x202818c'),('bl','#0x2028158')]:raise ValueError('Actual vectorR0-consuming caller chain changed')
    fixture=read_json(EVIDENCE/'caller-fixtures.json');vectors=[]
    for case in fixture['records']:
        count=sum(e['vectorForwardingInvocations']for e in case['executions'])
        if count:vectors.append(dict(caller=case['address'],case=case['case'],actualNativeForwardingInvocations=count,suppliedAtanResult=case['input']['atan'],suppliedFinalDivisionSignedR0=case['input']['bearing'],actualR0CallerEffectsMatchedIndependentModel=True))
    if sum(v['actualNativeForwardingInvocations']for v in vectors)!=fixture['actualNativeVector44ForwardingInvocations']:raise ValueError('Actual vector forwarding accounting differs')
    negatives=[]
    for key,wrong in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address','0x2028190'),('bytes',40),('targetSha256','0'*64)]:
        bad=copy.deepcopy(entry);bad[key]=wrong
        try:qualify(bad,main,main_inventory)
        except ValueError as error:negatives.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Bad vector return identity accepted')
    changed=bytearray(main);changed[0x2818c]^=1
    try:qualify(entry,bytes(changed),main_inventory)
    except ValueError as error:negatives.append(dict(case='native-body',rejected=True,reason=str(error)))
    else:raise ValueError('Altered vector body accepted')
    report=dict(passed=True,kind='zero-byte-accepted-interface-debt',canonicalCallee=entry,sourceOrCalleeCredit=0,migratedAcceptedDefinition=False,actualNativeVectorForwardingInvocations=fixture['actualNativeVector44ForwardingInvocations'],standalonePureMathReturnsClaimed=0,caller=dict(address=caller['address'],nativeWords=[dict(address=hex(i.address),word=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in instructions]),originalBody=[dict(address=hex(i.address),word=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in decoded],boundedForwardingVectors=vectors,negativeControls=negatives,limitation='Actual44-byte body forwardsR0 from supplied atan/div services thenreturns;34 helperinvocations occurwithin original/C caller fixtures. Underlyingmath bodies execute0instructions. Existingaccepteddefinitionvoid remainsunchanged; observed32bit signedangle caller contract is a future explicit nominalinterface migration,not newsourcecredit.')
    write_json(EVIDENCE/'vector-return-interface-debt.json',report);return report
