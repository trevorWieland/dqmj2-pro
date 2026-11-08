import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


def identity(row):return row.get('program')or'',row['processor'],row['module'],row['mode'],int(row['address'],0),row['bytes'],row['name']


def checked(root,record):
    name=record['path']
    if not isinstance(name,str)or'\\'in name or PurePosixPath(name).is_absolute()or'..'in PurePosixPath(name).parts:raise ValueError('Repository-identity-proof-path')
    path=root/name
    if path.absolute()!=path.resolve()or not path.resolve().is_relative_to(root):raise ValueError('Physical-identity-proof-path')
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=record['sha256']:raise ValueError('Immutable-identity-proof-hash')
    return data


def configuration_path(module):
    if module=='main':return'config/arm9/symbols.txt'
    if module in('itcm','dtcm'):return'config/arm9/'+module+'/symbols.txt'
    if re.fullmatch('ov00[0-7]',module):return'config/arm9/overlays/'+module+'/symbols.txt'
    raise ValueError('Known-host-ARM9-physical-module')


def witness_name(root,row,witness):
    if identity(row)!=identity(witness)or row.get('program')or row['processor']!='arm9':raise ValueError('Exact-host-identity-witness')
    if not isinstance(row['bytes'],int)or isinstance(row['bytes'],bool)or row['bytes']<=0:raise ValueError('Complete-positive-function-extent')
    for field in('source','sourceSha256','targetSha256'):
        if row[field]!=witness[field]:raise ValueError('Identity-source-target-contract')
    checked(root,dict(path=row['source'],sha256=row['sourceSha256']))
    if witness['moduleManifest']['path']!='provenance/seed-manifest.json':raise ValueError('Canonical-original-module-manifest')
    manifest=json.loads(checked(root,witness['moduleManifest']))
    modules=[x for x in manifest['modules']if x['name']==row['module']]
    if len(modules)!=1:raise ValueError('Unique-original-physical-module')
    module=modules[0];native=witness['nativeModule']
    if(native['path'],native['sha256'],int(native['base'],0),native['bytes'])!=(module['binary'],module['sha256'],int(module['base'],0),module['bytes']):raise ValueError('Original-module-base-binary-hash-extent')
    data=checked(root,native)
    if len(data)!=native['bytes']:raise ValueError('Whole-original-image-length')
    start=int(row['address'],0);offset=start-int(module['base'],0)
    if offset<0 or offset+row['bytes']>len(data)or hashlib.sha256(data[offset:offset+row['bytes']]).hexdigest()!=row['targetSha256']:raise ValueError('Full-original-native-span')
    config=witness['config']
    if config['path']!=configuration_path(row['module']):raise ValueError('Module-qualified-config-path')
    text=checked(root,config).decode('utf8');name=witness['dsdSymbol']
    if not isinstance(name,str)or not re.fullmatch(r'[A-Za-z_]\w*',name):raise ValueError('Explicit-configured-function-name')
    named=[line for line in text.splitlines()if line.split(' ',1)[0]==name]
    if len(named)!=1:raise ValueError('Configured-alias-exactly-once')
    pattern=r'(\S+) kind:function\((arm|thumb),size=(0x[0-9a-fA-F]+)(?:,dsprot=(?:0x[0-9a-fA-F]+|\(0x[0-9a-fA-F]+,0x[0-9a-fA-F]+\)))?\) addr:(0x[0-9a-fA-F]+)'
    function=re.fullmatch(pattern,named[0])
    if not function or(function[2],int(function[3],0),int(function[4],0))!=(row['mode'],row['bytes'],start):raise ValueError('Configured-function-mode-size-address')
    candidates=[]
    for line in text.splitlines():
        entry=re.fullmatch(pattern,line)
        if entry and(entry[2],int(entry[3],0),int(entry[4],0))==(row['mode'],row['bytes'],start):candidates.append(entry[1])
        if not entry and' kind:function('in line:
            address=re.search(r'\baddr:(0x[0-9a-fA-F]+)(?:\s|$)',line)
            if address and int(address[1],0)==start:raise ValueError('Unparsed-function-declaration-at-target-address')
    if candidates!=[name]:raise ValueError('Unambiguous-physical-native-function-name')
    if named[0]!=witness['configEntry']:raise ValueError('Exact-pinned-config-entry')
    for field in('dsdSymbol','nativeAlias','originalSymbol'):
        if field in row and row[field]!=name:raise ValueError('Conflicting-recognized-original-alias')
    return name


def assert_allowed_delta(before,after,witnesses):
    original=copy.deepcopy(before);restored=copy.deepcopy(after)
    if len(original['matches'])!=len(restored['matches']):raise ValueError('No-identity-row-count-change')
    expected={identity(row):row['dsdSymbol']for row in witnesses}
    for old,new in zip(original['matches'],restored['matches']):
        if identity(old)!=identity(new):raise ValueError('No-function-identity-change')
        if old.get('program'):
            if old!=new:raise ValueError('Child-row-must-remain-exact')
            continue
        if new.get('dsdSymbol')!=expected[identity(old)]:raise ValueError('Only-proven-host-dsdSymbol')
        if'dsdSymbol'in old:new['dsdSymbol']=old['dsdSymbol']
        else:new.pop('dsdSymbol',None)
    if original!=restored:raise ValueError('Delta-outside-host-row-dsdSymbol')


def project(root,report,witnesses):
    root=Path(root).resolve();result=copy.deepcopy(report)
    expected={identity(row):row for row in witnesses}
    hosts={identity(row)for row in report['matches']if not row.get('program')}
    if len(expected)!=len(witnesses)or set(expected)!=hosts:raise ValueError('Exact-descriptor-host-witness-set')
    for row in result['matches']:
        if row.get('program'):continue
        witness=expected[identity(row)];name=witness_name(root,row,witness)
        for field in('dsdSymbol','nativeAlias','originalSymbol'):
            if field in report and report[field]!=name:raise ValueError('Conflicting-report-original-alias')
        row['dsdSymbol']=name
    assert_allowed_delta(report,result,witnesses)
    return result
