import copy
from project import ROOT,read_json
import match_runtime as C


def verify(row,rel,binding,certificate,image,functions,modules):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],row['address'],row['bytes'],row['targetSha256'])!=('','arm7',certificate['module'],'arm',certificate['address'],certificate['bytes'],certificate['targetSha256']):raise ValueError('Exact ARM7 caller namespace/span differs')
    address=int(row['address'],0);base=certificate['base']
    if C.sha(image[address-base:address-base+certificate['bytes']])!=certificate['targetSha256']:raise ValueError('Original whole ARM7 caller changed')
    matches=[w for w in certificate['originalBindingWitnesses'] if int(w['witness']['origin'],0)==address+rel['offset']]
    if len(matches)!=1:raise ValueError('Unique original relocation word/origin absent')
    expected=matches[0]
    if (rel['symbol'],rel['type'],rel['format'],rel['explicitAddend'])!=(expected['renamed'],expected['type'],'SHT_RELA',expected['witness'].get('addend',-8)):raise ValueError('Original C symbol/relocation kind/explicit addend differs')
    raw=image[address-base+rel['offset']:address-base+rel['offset']+4]
    if raw.hex()!=expected['witness']['hex']:raise ValueError('Exact original ARM branch/literal bytes differ')
    target=int(expected['target'],0)
    if expected['function']:
        canonical=functions.get(target)
        if canonical is None or (binding['program'],binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=(canonical['program'],canonical['processor'],canonical['module'],'arm','function',hex(target)):raise ValueError('Exact same-program ARM7 function/mode entry differs')
    else:
        from link_arm7_bulk_20261030 import data_binding
        canonical=data_binding(row,target,modules)
        if any(binding.get(k)!=canonical.get(k) for k in ['program','processor','module','mode','kind','address','region']):raise ValueError('Exact original ARM7 data/BSS/module identity differs')
    return dict(origin=hex(address+rel['offset']),symbol=rel['symbol'],target=hex(target),kind='function' if expected['function'] else 'data',mode=binding['mode'],originalHex=raw.hex(),addend=rel['explicitAddend'],sourceCredit=0)


def controls(row):
    from link_arm7_bulk_20261030 import namespace
    from wave20261106_arm7_peripheral_next_source_first_build import LANE
    certificate=next(r for r in read_json(LANE/'native-certificate.json')['functions'] if r['name']==row['name']);image=(ROOT/certificate['binary']).read_bytes();modules,functions=namespace('');proofs=[];bad=[]
    for rel in row['relocations']:
        binding=row['nativeSymbolEntries'][rel['symbol']];proofs.append(verify(row,rel,binding,certificate,image,functions,modules))
        for label,owner,key,value in [('CPU','binding','processor','arm9'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','arm7-boot'),('mode','binding','mode','thumb'),('target-plus4','binding','address',hex(int(binding['address'],0)+4)),('kind','binding','kind','function' if binding['kind']=='data' else 'data'),('origin-plus4','rel','offset',rel['offset']+4),('addend-plus4','rel','explicitAddend',rel['explicitAddend']+4),('symbol-name','rel','symbol','native_host_arm7_arm_027e089c'),('format','rel','format','SHT_REL'),('caller-mode','row','mode','thumb')]:
            objects={k:copy.deepcopy(v) for k,v in [('row',row),('rel',rel),('binding',binding)]};objects[owner][key]=value
            try:verify(objects['row'],objects['rel'],objects['binding'],certificate,image,functions,modules)
            except (ValueError,KeyError) as error:bad.append(dict(origin=rel['offset'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong exact original ARM7 relocation witness admitted')
    return dict(status='passed',sourceCredit=0,actualOriginalRelocationWitnesses=proofs,negativeControls=bad,calleeOrStorageCredit=0)
