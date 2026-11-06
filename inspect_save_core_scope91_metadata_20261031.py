import argparse,copy,hashlib,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parent
NAMES={f'native_fn_{a:08x}' for a in [0x2096CF8,0x2096D9C,0x2096D4C,0x2096D6C,0x2096D24,0x2096D04,0x2096CE8]}
NEW={'evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi.json','evidence/matches/mechanics-save-20261031-lane-packed-classify.json'}


def normalize(report):
    report=copy.deepcopy(report);changes=[]
    for name in sorted(NAMES&report.get('nativeSymbols',{}).keys()):
        if name not in report.get('nativeSymbolModules',{}):continue
        entry=report.get('nativeSymbolEntries',{}).get(name,{});assert entry.get('processor')=='arm9' and entry.get('module')=='main' and entry.get('mode')=='thumb' and report['nativeSymbolModules'][name]=='main';address=int(name[-8:],16);assert int(report['nativeSymbols'][name],0)&~1==address and int(entry['address'],0)&~1==address
        changes.append(dict(symbol=name,originalScope=report['nativeSymbolModules'].pop(name),moduleEvidence=entry))
    return report,changes


def model(framework,reports):
    project=types.ModuleType('project');project.ROOT=framework;project.read_json=lambda path:reports[path];old=sys.modules.get('project');sys.modules['project']=project;namespace={'__name__':'private_scope91_model'}
    try:exec(compile((framework/'native_bindings.py').read_text(),str(framework/'native_bindings.py'),'exec'),namespace)
    finally:
        if old is None:sys.modules.pop('project',None)
        else:sys.modules['project']=old
    scoped=namespace['scoped_bindings'](list(reports));bindings={};pointers={};merges=0
    try:
        for path,report in reports.items():
            for name,value in report.get('nativeSymbols',{}).items():
                if name in NAMES:namespace['merge_target'](bindings,scoped[path].get(name,name),value);merges+=1
        for path,report in reports.items():
            for row in report.get('matches',[]):
                for relocation in row.get('relocations',[]):
                    name=relocation.get('symbol');value=relocation.get('targetAddress',relocation.get('target'))
                    if name not in NAMES:continue
                    alias=scoped[path].get(name,name);namespace['merge_target'](bindings,alias,value);merges+=1
                    if relocation.get('type')==2 and int(value,0)!=int(namespace['canonical_target'](name,value),0):pointers['__thumb_pointer_'+alias]=value
        return dict(success=True,merges=merges,bindingAliases=sum(name in NAMES for aliases in scoped.values() for name in aliases),bindings=bindings,thumbPointerAliases=pointers)
    except ValueError as error:return dict(success=False,merges=merges,failure=str(error))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--framework-root',type=Path,default=ROOT);args=parser.parse_args();framework=args.framework_root.resolve();reports={}
    for path in sorted((framework/'evidence/matches').glob('*.json')):
        try:report=json.loads(path.read_text())
        except (ValueError,UnicodeError):continue
        if NAMES&report.get('nativeSymbols',{}).keys():reports[path.relative_to(framework).as_posix()]=report
    reports={p:r for p,r in reports.items() if not p.endswith('host-scope-v2.json')};before=model(framework,reports);assert not before['success'] and '__binding_' in before['failure'];adapted=copy.deepcopy(reports);changes=[]
    for path in NEW:adapted[path],rows=normalize(reports[path]);changes.extend(dict(report=path,**r) for r in rows)
    assert len(changes)==7;after=model(framework,adapted);assert after['success'] and after['bindingAliases']==0 and after['thumbPointerAliases'];rejections=[]
    for label,field,value in [('processor','processor','arm7'),('module','module','ov001'),('mode','mode','arm')]:
        bad=copy.deepcopy(reports['evidence/matches/mechanics-save-20261031-lane-packed-pointer-abi.json']);name=next(n for n in NAMES if n in bad['nativeSymbolEntries']);bad['nativeSymbolEntries'][name][field]=value
        try:normalize(bad)
        except AssertionError:rejections.append(label)
        else:raise AssertionError('Unqualified normalization accepted')
    out=dict(schemaVersion=1,sourceCredit=0,scopeOnlyModel=True,frameworkFiles={name:hashlib.sha256((framework/name).read_bytes()).hexdigest() for name in ['native_bindings.py','build_modules.py']},participants={p:hashlib.sha256((framework/p).read_bytes()).hexdigest() for p in reports},before=before,after=after,changes=changes,qualificationRejections=rejections,frameworkAndFrozenReportsModified=False,moduleLinkClaim=False)
    target=ROOT/'evidence/attempts/save-core-packed-pointer-scope91-model-20261031.json';target.write_text(json.dumps(out,indent=2)+'\n');print(dict(before=before,after=dict(success=after['success'],merges=after['merges'],thumbPointers=len(after['thumbPointerAliases'])),changedScopes=len(changes),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))


if __name__=='__main__':main()
