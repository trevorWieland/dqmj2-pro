import copy
from project import ROOT,read_json,sha256
from elftools.elf.elffile import ELFFile
from wave20261106_arm7_wm_residual_next_third_build import LANE
CERTIFICATE=LANE/'callback-certificate.json'
CERTIFICATE_SHA='5966167fe93696584faa97998136a2cb8d3fa5a018d5583fb24057afba86d0fd'


def qualify(row,rel,functions,modules,record=None,binding=None):
    if sha256(CERTIFICATE)!=CERTIFICATE_SHA:raise ValueError('Frozen five-word ARM7 callback certificate changed')
    certificate=read_json(CERTIFICATE);expected=[r for r in certificate['callbacks']if r['callerAddress']==row['address']and r['symbol']==rel['symbol']and int(r['origin'],0)==int(row['address'],0)+rel['offset']]
    if len(expected)!=1:raise ValueError('Exact original ARM7 callback pointer site/name absent')
    expected=expected[0];record=expected if record is None else record
    if record!=expected:raise ValueError('Frozen original callback identity or literal evidence differs')
    if(row.get('sourceModule'),row['program'],row['processor'],row['module'],row['mode'],row['name'],row['targetSha256'])!=('arm7-main','','arm7','arm7-main','arm',record['callerName'],record['callerSpanSha256']):raise ValueError('Exact callback sourceModule/CPU/program/module/mode/span differs')
    target=int(record['address'],0);canonical=functions.get(target)
    if canonical is None:raise ValueError('No existing original canonical function entry at callback')
    binding=canonical if binding is None else binding
    if(binding['program'],binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'])!=('','arm7','arm7-main','arm','function',record['address']):raise ValueError('Exact callback existing ARM7 function/module/mode/entry differs')
    if rel['type']!=2 or rel['format']!='SHT_RELA'or rel['explicitAddend']!=0:raise ValueError('Exact unchanged original function-pointer ABS32/addend differs')
    image=(ROOT/certificate['binary']).read_bytes();origin=int(record['origin'],0)-0x027e0000
    if sha256(ROOT/certificate['binary'])!=certificate['inputModuleSha256']or image[origin:origin+4].hex()!=record['originalLiteralHex']or int.from_bytes(image[origin:origin+4],'little')!=target or target&3 or image[target-0x027e0000:target-0x027e0000+4].hex()!=record['entryWitnessHex']:raise ValueError('Original callback word and existing ARM entry witness differ')
    with(ROOT/row['object']).open('rb')as stream:
        elf=ELFFile(stream);symbols=[s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==rel['symbol']]
        if len(symbols)!=1 or symbols[0]['st_shndx']!='SHN_UNDEF'or symbols[0]['st_info']['type']!='STT_NOTYPE':raise ValueError('Actual unchanged MW external callback symbol convention differs')
    return binding,dict(status='passed',sourceCredit=0,origin=record['origin'],originalLiteralHex=record['originalLiteralHex'],symbol=record['symbol'],address=record['address'],kind='function',mode='arm',processor='arm7',module='arm7-main',sourceModule='arm7-main',originalCanonicalEntryRequired=True,actualExternalELFSymbolType='STT_NOTYPE',actualCFunctionDeclarationAndLinkedARMAnchorsRequired=True)


def controls(rows):
    from link_arm7_bulk_20261030 import namespace
    modules,functions=namespace('');positive=[];bad=[]
    for row in rows:
        certificate=next(c for c in read_json(LANE/'native-certificate.json')['functions']if c['name']==row['name'])
        for rel in row['relocations']:
            witnesses=[w for w in certificate['originalBindingWitnesses']if int(w['witness']['origin'],0)==int(row['address'],0)+rel['offset']and w['function']and w['type']==2]
            if not witnesses:continue
            binding,proof=qualify(row,rel,functions,modules);positive.append(proof);record=next(r for r in read_json(CERTIFICATE)['callbacks']if r['origin']==proof['origin'])
            for label,owner,key,value in [('sourceModule','row','sourceModule','main'),('CPU','binding','processor','arm9'),('program','binding','program','dwc/utility.bin/move/child.srl'),('module','binding','module','arm7-wram'),('mode','binding','mode','thumb'),('target-plus4','binding','address',hex(int(binding['address'],0)+4)),('provider-name','rel','symbol','native_host_arm7_arm_027e6054'),('kind','binding','kind','data'),('literal-origin','rel','offset',rel['offset']+4),('literal-addend','rel','explicitAddend',4),('entry-word','record','entryWitnessHex','00000000'),('caller-hash','row','targetSha256','0'*64)]:
                parts={n:copy.deepcopy(v)for n,v in [('row',row),('rel',rel),('binding',binding),('record',record)]};parts[owner][key]=value
                try:qualify(functions=functions,modules=modules,**parts)
                except ValueError as error:bad.append(dict(origin=record['origin'],case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original typed ARM7 callback admitted')
    if len(positive)!=5:raise ValueError('Exact five original ARM7 callback words required')
    return dict(status='passed',sourceCredit=0,positive=positive,negativeControls=bad,limits=['Only exact original ABS32 words and existing canonical ARM7 ARM function entries, with fresh actual C declarations and genuine STT_FUNC/$a zero-initialized-code anchors. Undefined production ELF symbols remain original MW STT_NOTYPE; no symbol/relocation/object rewrite or new entry aliases.'])
