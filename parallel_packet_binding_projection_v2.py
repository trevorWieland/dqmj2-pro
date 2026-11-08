import copy
import hashlib
from pathlib import Path, PurePosixPath
import re
import struct

RAW_FIELDS=('offset','type','symbol','format','explicitAddend','originalEncodedWord')
TOP_FIELDS={'nativeSymbols','nativeSymbolModules','nativeSymbolBindings','canonicalBindingProjection','program','processor'}
ROW_FIELDS={'relocations','nativeSymbolBindings'}


def local(root,name):
    if not isinstance(name,str) or not name or '\\'in name or PurePosixPath(name).is_absolute()or '..'in PurePosixPath(name).parts:
        raise ValueError('Canonical-repository-input-required')
    path=root/name
    if path.absolute()!=path.resolve()or not path.resolve().is_relative_to(root)or not path.is_file():
        raise ValueError('Physical-repository-input-required')
    return path


def checked(root,name,expected):
    raw=local(root,name).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected:
        raise ValueError('Actual-source-or-WHOLE-object-hash')
    return raw


def identity(row):
    return row.get('program')or'',row['processor'],row['module'],row['mode'],int(row['address'],0)


def number(value):
    if not isinstance(value,str)or not re.fullmatch('0x[0-9a-fA-F]+',value):
        raise ValueError('Explicit-native-address-string')
    return int(value,0)


def typed(value,owner):
    if not isinstance(value,dict):raise ValueError('Typed-binding-must-be-mapping')
    for field in ('program','processor','module','kind','mode','address'):
        if field not in value or not isinstance(value[field],str):raise ValueError('Complete-explicit-physical-binding')
    program,cpu,module,kind,mode=(value[x]for x in('program','processor','module','kind','mode'))
    if (program,cpu)!=(owner.get('program')or'',owner['processor']):raise ValueError('Binding-crosses-program-or-CPU')
    if program:
        if program!='dwc/utility.bin/move/child.srl'or not module.startswith('utility-child-'+cpu+'-'):raise ValueError('Exact-physical-child-module')
    elif cpu=='arm9':
        if module not in ('main','itcm','dtcm')and not re.fullmatch('ov00[0-7]',module):raise ValueError('Qualified-host-ARM9-module')
    elif cpu=='arm7':
        if module not in ('arm7-boot','arm7-main','arm7-wram'):raise ValueError('Qualified-host-ARM7-module')
    else:raise ValueError('Known-physical-processor')
    address=number(value['address'])
    if kind=='function':
        if mode not in ('arm','thumb')or address%(4 if mode=='arm'else 2):raise ValueError('Explicit-function-mode-and-address')
    elif kind!='data'or mode!='data':raise ValueError('Explicit-data-mode-and-kind')
    return copy.deepcopy(value)


def binding_map(value,owner):
    if isinstance(value,dict):
        rows=list(value.items())
    elif isinstance(value,list):
        rows=[]
        for item in value:
            if not isinstance(item,dict)or'name'not in item:raise ValueError('Named-binding-list-required')
            rows.append((item['name'],{k:v for k,v in item.items()if k!='name'}))
    else:raise ValueError('Binding-schema-map-or-named-list')
    result={}
    for name,definition in rows:
        if not isinstance(name,str)or not re.fullmatch('[A-Za-z_]\\w*',name)or name in result:raise ValueError('Unique-qualified-binding-name')
        if 'name'in definition:raise ValueError('No-conflicting-embedded-binding-name')
        result[name]=typed(definition,owner)
    return result


def exact_value(left,right):
    if type(left)is not type(right):return False
    if isinstance(left,dict):return left.keys()==right.keys()and all(exact_value(left[key],right[key])for key in left)
    if isinstance(left,list):return len(left)==len(right)and all(exact_value(a,b)for a,b in zip(left,right))
    return left==right


def declared_bindings_same(value,expected,owner):
    actual=binding_map(value,owner)
    if not owner.get('program')or not isinstance(value,list):return exact_value(actual,expected)
    if actual.keys()!=expected.keys():return False
    for name,left in actual.items():
        right=expected[name]
        if left.keys()!=right.keys():return False
        for field,observed in left.items():
            wanted=right[field]
            if field=='address':
                if number(observed)!=number(wanted):return False
            elif not exact_value(observed,wanted):return False
    return True


def canonical_named_bindings(bindings):
    result=[]
    for name,value in sorted(bindings.items()):
        row=copy.deepcopy(value)
        row['address']=hex(number(row['address']))
        result.append(dict(name=name,**row))
    return result


def raw_relocations(data,name,extent,mode=None):
    if len(data)<52 or data[:7]!=b'\x7fELF\x01\x01\x01':raise ValueError('ELF32-little-endian-required')
    h=struct.unpack_from('<16sHHIIIIIHHHHHH',data)
    if h[1:3]!=(1,40)or h[11]!=40 or not 0<h[12]<65536 or h[6]+h[11]*h[12]>len(data):raise ValueError('Actual-ARM-relocatable-object')
    sections=[struct.unpack_from('<IIIIIIIIII',data,h[6]+i*40)for i in range(h[12])]
    def payload(index):
        if not 0<=index<len(sections):raise ValueError('ELF-section-index')
        s=sections[index]
        if s[4]+s[5]>len(data):raise ValueError('ELF-section-bounds')
        return data[s[4]:s[4]+s[5]]
    tables={}
    for index,s in enumerate(sections):
        if s[1]!=2:continue
        if s[9]!=16 or s[5]%16:raise ValueError('Actual-ELF-symbol-table')
        strings=payload(s[6]);symbols=[]
        for offset in range(0,s[5],16):
            item=struct.unpack_from('<IIIBBH',payload(index),offset)
            if item[0]>=len(strings)or b'\0'not in strings[item[0]:]:raise ValueError('ELF-symbol-name')
            end=strings.index(b'\0',item[0])
            symbols.append(dict(name=strings[item[0]:end].decode(),value=item[1],bytes=item[2],kind=item[3]&15,section=item[5]))
        tables[index]=symbols
    selected=[x for table in tables.values()for x in table if x['name']==name]
    if len(selected)!=1 or selected[0]['kind']!=2 or selected[0]['bytes']!=extent:raise ValueError('Unique-complete-STT_FUNC-extent')
    symbol=selected[0];start=symbol['value']&~1;body=payload(symbol['section'])
    mappings={('thumb'if x['name']=='$t'else'arm')for table in tables.values()for x in table if x['section']==symbol['section']and x['value']==start and x['name']in('$a','$t')}
    if mode is not None and mappings!={mode}:raise ValueError('Actual-mapping-symbol-instruction-mode')
    if start+extent>len(body):raise ValueError('Whole-function-object-bounds')
    rows=[]
    for index,s in enumerate(sections):
        if s[1]not in(4,9)or s[7]!=symbol['section']:continue
        if s[1]!=4 or s[9]!=12 or s[5]%12:raise ValueError('Explicit-SHT_RELA-only-no-inferred-addends')
        symbols=tables.get(s[6])
        if symbols is None:raise ValueError('Relocation-symbol-table')
        for offset in range(0,s[5],12):
            location,info,addend=struct.unpack_from('<IIi',payload(index),offset)
            relative=location-start
            if not 0<=relative<extent:continue
            if info>>8>=len(symbols)or relative+4>extent:raise ValueError('Actual-relocation-bounds')
            if symbols[info>>8]['section']!=0:raise ValueError('Only-explicit-external-typed-relocations')
            rows.append(dict(offset=relative,type=info&255,symbol=symbols[info>>8]['name'],format='SHT_RELA',explicitAddend=addend,originalEncodedWord=body[location:location+4].hex()))
    return rows


def agree(existing,wanted,field):
    if field in('target','targetAddress'):
        return number(existing)==number(wanted)
    return type(existing)is type(wanted)and existing==wanted


def raw_same(declared,actual,partial=False):
    if not isinstance(declared,list)or len(declared)!=len(actual):return False
    for before,after in zip(declared,actual):
        if not isinstance(before,dict)or not all(k in before for k in(('offset','type','symbol')if partial else RAW_FIELDS)):return False
        if any(type(before[k])is not type(after[k])or before[k]!=after[k]for k in RAW_FIELDS if k in before):return False
    return True


def assert_allowed_delta(before,after):
    left=copy.deepcopy(before);right=copy.deepcopy(after)
    for document in(left,right):
        for field in TOP_FIELDS:document.pop(field,None)
        for row in document['matches']:
            for field in ROW_FIELDS:row.pop(field,None)
    if left!=right:raise ValueError('Delta-outside-generated-metadata-allowlist')
    for old,new in zip(before['matches'],after['matches']):
        if not old.get('program')and old.get('nativeSymbolBindings')!=new.get('nativeSymbolBindings'):
            raise ValueError('Host-binding-map-must-remain-unchanged')
    child=bool(before['matches'][0].get('program'))
    if not child and before.get('nativeSymbolBindings')!=after.get('nativeSymbolBindings'):
        raise ValueError('Host-report-binding-map-must-remain-unchanged')
    for field in('program','processor'):
        if before.get(field)!=after.get(field)and(not child or before.get(field)):
            raise ValueError('Only-missing-child-report-namespace-completion')
        if child and after.get(field)!=before['matches'][0][field]:raise ValueError('Completed-child-namespace-must-equal-row')


def project(root,report,expected):
    root=Path(root).resolve();result=copy.deepcopy(report)
    if report.get('failed')or report.get('allPassed')is False or not isinstance(report.get('matches'),list)or not report['matches']:
        raise ValueError('Original-qualified-worker-report-required')
    wanted={identity(x):x for x in expected}
    actual={identity(x):x for x in report['matches']}
    if len(wanted)!=len(expected)or len(actual)!=len(report['matches'])or set(actual)!=set(wanted):raise ValueError('Exact-descriptor-identity-set')
    union={};count=0
    for original,row in zip(report['matches'],result['matches']):
        contract=wanted[identity(row)]
        for field in('bytes','source','sourceSha256','targetSha256'):
            if row[field]!=contract[field]:raise ValueError('Original-source-native-contract')
        if type(row['bytes'])is not int or row['bytes']<=0 or row['compiledBytes']!=row['bytes']or not row['exactAfterDeclaredRelocation']or not row['realLink']['exactCallerBytes']:
            raise ValueError('Complete-existing-genuine-match-required')
        checked(root,row['source'],row['sourceSha256'])
        for dependency in row.get('sourceDependencies',[]):checked(root,dependency['path'],dependency['sha256'])
        data=checked(root,row['object'],row['objectSha256'])
        raw=raw_relocations(data,row['name'],row['bytes'],row['mode'])
        declarations=[row[x]for x in('rawRelocations','relocations')if x in row]
        if not declarations:raise ValueError('Existing-raw-relocation-proof-required')
        for declared in declarations:
            if not raw_same(declared,raw):raise ValueError('Actual-ELF-raw-relocation-proof-differs')
        if 'originalRelocations'in row['realLink']:
            linked=row['realLink']['originalRelocations']
            if not raw_same(linked,raw,True):raise ValueError('Existing-link-relocation-fields')
        if not isinstance(row.get('nativeSymbolEntries'),dict):raise ValueError('Host-typed-entry-map-convention')
        bindings=binding_map(row['nativeSymbolEntries'],row)
        if not declared_bindings_same(row['nativeSymbolBindings'],bindings,row):raise ValueError('Raw-binding-alias-map-roundtrip')
        if set(bindings)!={x['symbol']for x in raw}:raise ValueError('Exact-external-symbol-binding-union')
        anchors=row['realLink'].get('bindingOnlyProbes',row['realLink'].get('bindings',[]))
        proof={}
        for anchor in anchors:
            name=anchor['name']
            if name in proof or anchor.get('initializedCodeBytes')!=0 or any(anchor.get(x,0)!=0 for x in('calleeSourceCredit','sourceCredit')):raise ValueError('Unique-existing-zero-code-link-witness')
            proof[name]={k:anchor[k]for k in('program','processor','module','kind','mode','address')}
        if proof!={name:{k:value[k]for k in('program','processor','module','kind','mode','address')}for name,value in bindings.items()if value['kind']=='function'}:raise ValueError('Typed-binding-differs-from-existing-genuine-link-witness')
        for name,value in bindings.items():
            if value['kind']!='data':continue
            witnesses=[x['binding']for x in row['realLink'].get('originalRelocations',[])if x.get('symbol')==name and 'binding'in x]
            if name in report.get('nativeSymbolEntries',{}):witnesses.append(report['nativeSymbolEntries'][name])
            if not any(all(x.get(k)==value[k]for k in('program','processor','module','kind','mode','address'))for x in witnesses):raise ValueError('Existing-explicit-data-binding-witness-required')
        if row['realLink'].get('sourceObjectSha256',row['objectSha256'])!=row['objectSha256']or row['realLink'].get('nativeSpanSha256')!=row['targetSha256']or row['realLink'].get('linkedCallerSha256')!=row['targetSha256']:raise ValueError('Existing-genuine-source-native-hash-contract')
        normalized=[]
        existing=row.get('relocations',raw)
        for i,item in enumerate(raw):
            binding=bindings[item['symbol']]
            if item['type']not in(1,2,10,15,28,29)or binding['kind']=='data'and item['type']!=2:raise ValueError('Explicit-supported-typed-relocation')
            value=copy.deepcopy(existing[i]);enrich=dict(target=binding['address'],targetAddress=binding['address'],targetMode=binding['mode'],addend=item['explicitAddend'])
            for field,target in enrich.items():
                if field in value and not agree(value[field],target,field):raise ValueError('Conflicting-standard-relocation-field')
                value.setdefault(field,target)
            normalized.append(value)
        row['relocations']=normalized;count+=len(raw)
        if row.get('program'):row['nativeSymbolBindings']=canonical_named_bindings(bindings)
        for name,value in bindings.items():
            if name in union and not exact_value(union[name],value):raise ValueError('Conflicting-full-physical-binding-union')
            union[name]=value
    owners={(x.get('program')or'',x['processor'])for x in result['matches']}
    if len(owners)!=1:raise ValueError('One-physical-program-CPU-per-report')
    owner=result['matches'][0]
    for field in('program','processor'):
        if report.get(field)and report[field]!=(owner.get(field)or''):raise ValueError('Existing-report-namespace-disagrees-with-rows')
    for field in('nativeSymbolBindings','nativeSymbolEntries'):
        if field=='nativeSymbolEntries'and field in report and not isinstance(report[field],dict):raise ValueError('Report-typed-entry-map-convention')
        if field in report and not declared_bindings_same(report[field],union,owner):raise ValueError('Existing-report-binding-union-disagrees')
    if owner.get('program'):
        if {(x.get('program')or'',x['processor'])for x in expected}!={(owner['program'],owner['processor'])}:raise ValueError('Unanimous-descriptor-child-namespace')
        for field in('program','processor'):
            if report.get(field)and report[field]!=owner[field]:raise ValueError('Existing-child-report-namespace-conflict')
            result[field]=owner[field]
        result['nativeSymbolBindings']=canonical_named_bindings(union)
    for field in('nativeSymbols','nativeSymbolModules'):
        values=copy.deepcopy(report.get(field,{}))
        if not isinstance(values,dict):raise ValueError('Report-symbol-address-and-module-maps')
        if set(values)-set(union):raise ValueError('No-untyped-extra-report-native-export')
        for name,binding in union.items():
            target=binding['address'if field=='nativeSymbols'else'module']
            if name in values and (number(values[name])!=number(target)if field=='nativeSymbols'else values[name]!=target):raise ValueError('Conflicting-report-native-export')
            values.setdefault(name,target)
        result[field]=values
    result['canonicalBindingProjection']=dict(version=2,sourceCredit=0,sourceObjectAndLinkBytesUnchanged=True,rawRelocationsUnchanged=True,actualELFRelocations=count,
        childNamedListsOnly=True,childListAddressesCanonicalHex=True,hostMapsPreserved=True,explicitRELAAddends=True)
    assert_allowed_delta(report,result)
    return result
