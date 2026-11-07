import copy
import hashlib
import re
import json
import utility_runtime
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,read_json,sha256
from wave20261106_child_snd_resume_paths import EVIDENCE

PROGRAM='dwc/utility.bin/move/child.srl'
TARGETS={28:0x2005884,56:0x200577c,84:0x2006d70,100:0x2005878,140:0x2005820,152:0x2005bb4,164:0x2005b8c,180:0x2005b64}


def qualify(row):
    claim=read_json(EVIDENCE/'claim.json');entry=claim['claimedFunctions'][0]
    if(row.get('program'),row['processor'],row['module'],row['mode'],row['address'],row['bytes'],row['targetSha256'])!=(PROGRAM,'arm9','utility-child-arm9-main','arm','0x2006eb8',196,entry['targetSha256']):raise ValueError('Exact child caller program/CPU/module/mode/whole extent differs')
    layout,files=utility_runtime.derive();module=next(m for m in layout['modules']if m['id']=='utility-child-arm9-main');image=files[ROOT/module['binary']];base=int(module['base'],0);a=int(row['address'],0);native=image[a-base:a-base+196]
    if module['sha256']!=row['inputModuleSha256']or hashlib.sha256(native).hexdigest()!=row['targetSha256']:raise ValueError('Whole original child image/caller changed')
    inventory=read_json(ROOT/'evidence/utility/ghidra-arm9.json')
    if inventory['program']!=PROGRAM or inventory['processor']!='arm9':raise ValueError('Actual imported-entry inventory namespace changed')
    if len(row['relocations'])!=8 or{r['offset']for r in row['relocations']}!=set(TARGETS):raise ValueError('Actual eight original caller relocations differ')
    canonical={};bindings={};proof=[];decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for rel in row['relocations']:
        target=TARGETS[rel['offset']];name='native_fn_utility_child_arm9_main_%08x'%target
        if(rel['symbol'],int(rel['target'],0),rel['targetMode'],rel['type'],rel['addend'])!=(name,target,'arm',1,-8):raise ValueError('Actual original child import/type/addend/mode differs')
        word=native[rel['offset']:rel['offset']+4];instruction=list(decoder.disasm(word,a+rel['offset']))
        if len(instruction)!=1 or instruction[0].mnemonic!='bl'or instruction[0].op_str!='#'+hex(target):raise ValueError('Actual original ARM BL destination/word differs')
        callee=next((f for f in inventory['functions']if int(f['address'],0)==target),None)
        if callee is None or(callee['module'],callee['processor'],callee['mode'])!=('utility-child-arm9-main','arm9','arm')or not callee['ranges']or int(callee['ranges'][0][0],0)!=target:raise ValueError('Genuine same-program/cpu/mode imported entry absent')
        canonical['arm9',target]=dict(processor='arm9',program=PROGRAM,module=callee['module'],address=target,mode='arm')
        bindings[name]=dict(program=PROGRAM,processor='arm9',module=callee['module'],address=hex(target),mode='arm',kind='function')
        proof.append(dict(offset=rel['offset'],originalNativeBLAddress=hex(a+rel['offset']),originalNativeWord=word.hex(),originalTarget=hex(target),program=PROGRAM,processor='arm9',module=callee['module'],mode='arm',originalGhidraEntry=callee,calleeFunctionOrCodeCredit=0,calleeTypeAndBehaviorProvedByCaller=False))
    return canonical,bindings,proof


def negatives(rows):
    cases=[]
    for row in rows:
        mutations=[('program','program','host'),('processor','processor','arm7'),('module','module','main'),('mode','mode','thumb'),('extent','bytes',192),('native-body','targetSha256','0'*64)]
        for name,key,bad in mutations:
            wrong=copy.deepcopy(row);wrong[key]=bad
            try:qualify(wrong)
            except ValueError as e:cases.append(dict(case=name,rejected=True,reason=str(e)))
            else:raise ValueError('Wrong caller identity passed')
        for index,rel in enumerate(row['relocations']):
            for name,key,bad in[('interior','target',hex(int(rel['target'],0)+4)),('mode','targetMode','thumb'),('type','type',2),('addend','addend',0),('origin','offset',rel['offset']+4),('foreign-symbol','symbol','native_fn_main_%08x'%int(rel['target'],0))]:
                wrong=copy.deepcopy(row);wrong['relocations'][index][key]=bad
                try:qualify(wrong)
                except(ValueError,KeyError)as e:cases.append(dict(case=name,offset=rel['offset'],rejected=True,reason=str(e)))
                else:raise ValueError('Wrong original native import passed')
    return dict(passed=True,negativeCases=cases,globalIndicesAndNormalizersUnchanged=True)
