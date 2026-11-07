import copy
import re
from project import ROOT,read_json,sha256

PATH=ROOT/'evidence/lanes/parallel-wave20261106/arm7-peripheral-next/second/data-interface-certificate.json'
SHA='d2bb97ae96da995d6e12a646482c327d8e905ef677616364b26c7b69e5ffbef0'
TYPES={'last_touch_flg':('u16',2,0x03809ea8)}


def load():
    if sha256(PATH)!=SHA:raise ValueError('Immutable exact typed touch BSS interface certificate changed')
    result=read_json(PATH)
    if len(result['records'])!=2 or result['sourceCredit']or result['storageCredit']:raise ValueError('Exact two caller-qualified imported BSS interfaces acquired credit')
    return result


def record(pin,row,rel,binding,image,module,source):
    if pin['semanticName']not in TYPES:raise ValueError('Unknown touch BSS source object')
    typ,size,address=TYPES[pin['semanticName']]
    if (pin['program'],pin['processor'],pin['module'],pin['mode'],pin['kind'],pin['region'],pin['sourceType'],pin['bytes'],int(pin['address'],0),pin['sourceCredit'],pin['storageCredit'])!=('','arm7','arm7-wram','data','data','bss',typ,size,address,0,0):raise ValueError('Original typed BSS namespace/type/extent differs')
    if (binding['program'],binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['region'],int(binding['address'],0))!=('','arm7','arm7-wram','data','data','bss',address):raise ValueError('Actual original BSS binding module/mode/type differs')
    if not int(module['bssStart'],0)<=address<address+size<=int(module['bssEnd'],0):raise ValueError('Complete source object exceeds actual ARM7-wram BSS')
    if (row['program'],row['processor'],row['module'],row['mode'],row['address'],row['targetSha256'])!=('','arm7','arm7-wram','arm',pin['callerAddress'],pin['callerSha256']):raise ValueError('Exact original touch caller namespace/hash differs')
    if (rel['symbol'],rel['type'],rel['format'],rel['explicitAddend'],int(row['address'],0)+rel['offset'])!=(pin['symbol'],2,'SHT_RELA',pin['explicitAddend'],int(pin['origin'],0)):raise ValueError('Original touch ABS32 symbol/origin/addend differs')
    base=int(module['base'],0);at=int(pin['origin'],0)-base;word=image[at:at+4]
    if word.hex()!=pin['originalWord']or int.from_bytes(word,'little')-pin['explicitAddend']!=address:raise ValueError('Actual original touch literal word/address differs')
    declaration=r'\bextern\s+'+r'\s*'.join(map(re.escape,typ.split()))+r'\s*'+re.escape(pin['symbol'])+r'\s*;'
    if len(re.findall(declaration,source))!=1:raise ValueError('Actual owned typed external BSS object declaration differs')
    return dict(symbol=pin['symbol'],type=typ,bytes=size,origin=pin['origin'],sourceCredit=0,storageCredit=0)


def verify(row,image,modules,bindings):
    source='\n'.join((ROOT/name).read_text()for name in [row['source']]+[r['path']for r in row['sourceDependencies']]);proof=[]
    for rel in row['relocations']:
        if bindings[rel['symbol']]['kind']!='data':continue
        pins=[p for p in load()['records']if p['symbol']==rel['symbol']and p['callerAddress']==row['address']]
        if len(pins)!=1:raise ValueError('Unknown imported data interface in exact touch caller')
        proof.append(record(pins[0],row,rel,bindings[rel['symbol']],image,modules['arm7-wram'],source))
    if len(proof)!=1:raise ValueError('Exact two caller-qualified touch BSS interfaces missing')
    return proof


def controls(row):
    from link_arm7_bulk_20261030 import namespace
    modules,functions=namespace('');module=modules['arm7-wram'];image=(ROOT/module['binary']).read_bytes();source='\n'.join((ROOT/name).read_text()for name in [row['source']]+[r['path']for r in row['sourceDependencies']]);results=[]
    for pin in [p for p in load()['records']if p['callerAddress']==row['address']]:
        rel=next(r for r in row['relocations']if r['symbol']==pin['symbol']);binding=row['nativeSymbolEntries'][pin['symbol']];record(pin,row,rel,binding,image,module,source)
        for label in ['cpu','program','module','mode','function','address','extent','type','origin','addend','word','bss-limit','declaration']:
            p,r,b,m,s=copy.deepcopy(pin),copy.deepcopy(rel),copy.deepcopy(binding),copy.deepcopy(module),source
            if label=='cpu':b['processor']='arm9'
            elif label=='program':b['program']='dwc/utility.bin/move/child.srl'
            elif label=='module':b['module']='arm7-main'
            elif label=='mode':b['mode']='arm'
            elif label=='function':b['kind']='function'
            elif label=='address':b['address']=hex(int(b['address'],0)+4)
            elif label=='extent':p['bytes']+=4
            elif label=='type':p['sourceType']='unsigned char'
            elif label=='origin':r['offset']+=4
            elif label=='addend':r['explicitAddend']+=4
            elif label=='word':p['originalWord']='00000000'
            elif label=='bss-limit':m['bssEnd']=hex(int(p['address'],0)+p['bytes']-1)
            else:s=s.replace(p['symbol']+';',p['symbol']+'[2];')
            try:record(p,row,r,b,image,m,s)
            except ValueError as error:results.append(dict(symbol=pin['symbol'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError(('Wrong touch BSS interface admitted',pin['symbol'],label))
    return dict(status='passed',sourceCredit=0,storageCredit=0,negativeControls=results)
