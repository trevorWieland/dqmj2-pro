import copy
import re
from project import ROOT,read_json,sha256
import match_runtime as C

PATH=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-driver-timing-next/first/table-certificate.json'
SHA='c0d686677b63adf173289d5b94858ab31890d14a8c231ec8d9ff4d612a3bb325'
TYPES={'def_WepKey':('u16',40,0x027f730c),'def_SsidMask':('u16',16,0x027f72ac),'c_RateSet':('RATE_SET',1,0x027f72a8)}


def load():
    if sha256(PATH)!=SHA:raise ValueError('Immutable typed native table certificate changed')
    result=read_json(PATH)
    if len(result['records'])!=3 or result['sourceCredit'] or result['storageCredit']:raise ValueError('Exact three-table zero-credit scope differs')
    return result


def record(pin,image,binding,entry,relocation,source):
    name=pin['semanticName']
    if name not in TYPES:raise ValueError('Unknown semantic constant table')
    typ,count,address=TYPES[name];width=4 if typ=='RATE_SET'else 2
    if (pin['program'],pin['processor'],pin['module'],pin['mode'],pin['kind'])!=('','arm7','arm7-main','data','data'):raise ValueError('Typed table namespace/mode/kind differs')
    if (pin['elementType'],pin['elementCount'],pin['bytes'],int(pin['address'],0),pin['sourceCredit'],pin['storageCredit'])!=(typ,count,count*width,address,0,0):raise ValueError('Actual primary table type/count/full extent differs')
    if (binding['program'],binding['processor'],binding['module'],binding['mode'],binding['kind'],int(binding['address'],0))!=('','arm7','arm7-main','data','data',address):raise ValueError('Actual data binding namespace/type/address differs')
    if pin['symbol']!=relocation['symbol'] or pin['symbol']!='native_host_arm7_data_'+format(address,'08x'):raise ValueError('Typed original table symbol differs')
    at=int(pin['origin'],0)-int(entry['address'],0)
    if pin['caller']!=entry['address'] or at!=relocation['offset'] or relocation['type']!=2 or relocation['format']!='SHT_RELA' or relocation['explicitAddend']!=pin['explicitAddend']:raise ValueError('Actual table caller/literal origin/ABS32/addend differs')
    offset=int(pin['origin'],0)-0x027e0000;word=image[offset:offset+4]
    if word.hex()!=pin['originalWord'] or int.from_bytes(word,'little')-pin['explicitAddend']!=address:raise ValueError('Actual original literal word/addend/table target differs')
    offset=address-0x027e0000
    if len(image[offset:offset+pin['bytes']])!=pin['bytes'] or C.sha(image[offset:offset+pin['bytes']])!=pin['nativeSha256']:raise ValueError('Complete original table bytes/hash differ')
    suffix=r'\s*;'if typ=='RATE_SET'else r'\s*\[\s*'+str(count)+r'\s*\]\s*__attribute__\(\(aligned\(4\)\)\)\s*;'
    pattern=r'\bextern\s+const\s+'+typ+r'\s+'+re.escape(pin['symbol'])+suffix
    if len(re.findall(pattern,source))!=1 or re.search(r'\b'+re.escape(pin['symbol'])+r'\s*\([^;{}]*\)',source):raise ValueError('Exact natural typed extern-array declaration missing or function-confused')


def verify(entry,image,bindings):
    certificate=load()
    if C.sha(image)!=certificate['inputModuleSha256']:raise ValueError('Actual full ARM7 table module changed')
    source='\n'.join((ROOT/p).read_text()for p in [entry['source']]+[r['path']for r in entry['sourceDependencies']]);proof=[]
    for relocation in entry['relocations']:
        binding=bindings[relocation['symbol']]
        if binding['kind']!='data':continue
        pins=[p for p in certificate['records']if p['caller']==entry['address'] and p['symbol']==relocation['symbol']]
        if len(pins)!=1:raise ValueError('Imported table lacks unique original typed certificate')
        record(pins[0],image,binding,entry,relocation,source);proof.append(dict(symbol=relocation['symbol'],bytes=pins[0]['bytes'],origin=pins[0]['origin'],storageCredit=0,sourceCredit=0))
    return proof


def controls(rows):
    certificate=load();image=(ROOT/certificate['binary']).read_bytes();results=[]
    for pin in certificate['records']:
        row=next(r for r in rows if r['address']==pin['caller']);rel=next(r for r in row['relocations']if r['symbol']==pin['symbol']);binding=row['nativeSymbolEntries'][pin['symbol']];source='\n'.join((ROOT/p).read_text()for p in [row['source']]+[r['path']for r in row['sourceDependencies']]);record(pin,image,binding,row,rel,source)
        for label in ['cpu','program','module','mode','function','address','extent','count','element-type','table-hash','origin','word','addend','declaration-count','declaration-type','declaration-signedness','declaration-function']:
            p,b,r,s=copy.deepcopy(pin),copy.deepcopy(binding),copy.deepcopy(rel),source
            if label=='cpu':b['processor']='arm9'
            elif label=='program':b['program']='utility-child'
            elif label=='module':b['module']='arm7-wram'
            elif label=='mode':b['mode']='arm'
            elif label=='function':b['kind']='function'
            elif label=='address':b['address']=hex(int(b['address'],0)+2)
            elif label=='extent':p['bytes']-=2
            elif label=='count':p['elementCount']-=1
            elif label=='element-type':p['elementType']='u32'
            elif label=='table-hash':p['nativeSha256']='0'*64
            elif label=='origin':p['origin']=hex(int(p['origin'],0)+4)
            elif label=='word':p['originalWord']='00000000'
            elif label=='addend':r['explicitAddend']+=2
            else:
                old='extern const '+p['elementType']+' '+p['symbol']+(';'if p['elementType']=='RATE_SET'else'['+str(p['elementCount'])+'] __attribute__((aligned(4)));')
                new=old.replace('['+str(p['elementCount'])+']','['+str(p['elementCount']-1)+']')if label=='declaration-count'and p['elementType']!='RATE_SET'else old.replace(p['elementType'],'unsigned long')if label in ['declaration-type','declaration-count']else old.replace(p['elementType'],'signed short')if label=='declaration-signedness'else 'extern unsigned long '+p['symbol']+'(void);'
                if s.count(old)!=1:raise ValueError('Actual source table declaration not unique')
                s=s.replace(old,new)
            try:record(p,image,b,row,r,s)
            except ValueError as error:results.append(dict(table=pin['semanticName'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError(('Incorrect typed native table admitted',pin['semanticName'],label))
    return dict(status='passed',sourceCredit=0,storageCredit=0,negativeControls=results)
