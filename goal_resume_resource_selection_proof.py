import copy
import gzip
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from goal_resume_resource_selection_compile import LANE,SOURCE,WORK,compare
from goal_resume_resource_selection_oracle import HELPERS,SERVICES,fixtures,run
import link_runtime_unit as linker


def original(reference,image,symbols):
    key=((reference.get('program')or''),reference['processor'],reference['module'],reference['mode'],int(reference['address'],0),reference['bytes'])
    expected=('', 'arm9','main','arm',int(reference['address'],0),432 if int(reference['address'],0)==0x02061088 else 268)
    if key!=expected or expected[4]not in(0x02061088,0x02061470):raise ValueError('Wrong claimed physical resource identity')
    body=image[key[4]-0x02000000:key[4]-0x02000000+key[5]]
    if hashlib.sha256(body).hexdigest()!=reference['targetSha256']:raise ValueError('Whole original resource span changed')
    record=f"func_{key[4]:08x} kind:function(arm,size={hex(key[5])}) addr:0x{key[4]:08x}"
    if record not in symbols.splitlines():raise ValueError('Whole original resource boundary differs')
    return body


def build(source,directory,negative=False):
    rows,unused=compare(source,directory/'compile')
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('Genuine resource compile failed',rows))
    row=dict(rows[0],program='',sourceLanguage='C',sourceCredit=0,matched=False)
    ref=next(r for r in read_json(LANE/'claim.json')['claimedFunctions']if int(r['address'],0)==int(row['address'],0))
    info,image,symbols=linker.measured_module('main');native=original(ref,image,symbols)
    bindings={r['symbol']:dict(program='',processor='arm9',module='main',mode='data'if r['type']==2 else'arm',kind='data'if r['type']==2 else'function',address=r['target'])for r in row['relocations']}
    try:real=linker.validate(row,bindings,directory/'link')
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],dict):raise
        real=dict(exactCallerBytes=False,comparison=error.args[0])
    body=(directory/'link/caller.bin').read_bytes()
    if len(body)!=row['compiledBytes']or linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):raise ValueError('Native source link altered genuine extent or raw relocations')
    if not negative:
        records=(ROOT/'config/arm9/relocs.txt').read_text().splitlines();expected=[]
        for line in records:
            m=re.match(r'from:(0x[0-9a-f]+) kind:(arm_call|load) to:(0x[0-9a-f]+) module:main$',line)
            if m and int(ref['address'],0)<=int(m[1],0)<int(ref['address'],0)+ref['bytes']:expected.append((1 if m[2]=='arm_call'else 2,int(m[3],0)))
        if sorted(expected)!=sorted((r['type'],int(r['target'],0))for r in row['relocations']):raise ValueError('Original complete function/callee/literal identity multiset differs')
    row.update(realLink=real,nativeSymbolEntries=bindings,sourceDependencies=[dict(path=source.with_name('resource_selection.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('resource_selection.h')))],ordinaryCBytes=row['compiledBytes'],justifiedAssemblyBytes=0)
    return row,body,native,image


def helper_contracts(image):
    symbols=(ROOT/'config/arm9/symbols.txt').read_text().splitlines();result=[]
    for address,(extent,code,args)in HELPERS.items():
        record=f'func_{address:08x} kind:function(arm,size={hex(extent)}) addr:0x{address:08x}'
        if record not in symbols:raise ValueError('Real executed helper lacks original configured extent')
        result.append(dict(program='',processor='arm9',module='main',mode='arm',address=hex(address),bytes=extent,codeBytes=code,wordArguments=args,targetSha256=hashlib.sha256(image[address-0x02000000:address-0x02000000+extent]).hexdigest(),sourceCredit=0))
    for address in SERVICES:
        if not any(re.match(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x'+f'{address:08x}'+r'$',line)for line in symbols):raise ValueError('Supplied leaf interface lacks a native boundary')
    return result


def main():
    if sys.version_info[:3]!=(3,13,5):raise ValueError('Pinned Python runtime differs')
    if(LANE/'inputs.json').exists():
        for p in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/p['path'])!=p['sha256']:raise ValueError('Frozen resource proof input changed')
    rows=[];traces=[];raw_differences=[];by_address={}
    for source in sorted(SOURCE.glob('*.c')):
        row,body,native,image=build(source,WORK/'proof/positive'/source.stem)
        for ordinal,f in enumerate(fixtures()):
            if f['address']!=int(row['address'],0):continue
            span=max(len(native),len(body))
            a=run(native,f,image,ordinal,span);b=run(body,f,image,ordinal,span)
            if a['modelFailures']or b['modelFailures']or a['observation']!=b['observation']:
                write_json(WORK/'proof/failed-vector.json',dict(fixture=f,native=a,source=b));raise ValueError(('Native/source C ABI observations or independent models differ',source.stem,ordinal))
            delta=[i for i,(x,y)in enumerate(zip(a['rawRegisters'],b['rawRegisters']))if x!=y]
            if delta or a['cpsr']!=b['cpsr']:raw_differences.append(dict(address=row['address'],ordinal=ordinal,registers=delta,nativeCpsr=a['cpsr'],sourceCpsr=b['cpsr']))
            traces.append(dict(fixture=f,observation=a['observation'],nativeRegisters=a['rawRegisters'],sourceRegisters=b['rawRegisters'],nativeCpsr=a['cpsr'],sourceCpsr=b['cpsr']))
        rows.append(row);by_address[int(row['address'],0)]=(row,body,native,image)
        print('qualified resource observations',row['address'],row['compiledBytes'],flush=True)
    negatives=[]
    variants=[('wrong-sentinel',0x02061088,'code==-1','code==-2'),
        ('unsigned-format-code',0x02061088,'(s32)code','(s32)(u8)code'),
        ('wrong-free-heap',0x02061088,'native_fn_0202a498(2,resource)','native_fn_0202a498(3,resource)'),
        ('wrong-palette-zero',0x02061470,'u16 zero=0','u16 zero=1'),
        ('wrong-signed-flag-gate',0x02061470,'[0x273]!=0','[0x273]==1'),
        ('wrong-bitmap-length',0x02061470,'0,0x900','0,0x800'),
        ('wrong-final-flag',0x02061470,'[1]=1','[1]=0')]
    for label,address,before,after in variants:
        source=SOURCE/(f'{address:08x}'+'.c');text=source.read_text()
        if before not in text:raise ValueError('Wrong resource C mutation missing')
        folder=WORK/'proof/negative'/label;folder.mkdir(parents=True,exist_ok=True);bad=folder/source.name
        bad.write_text(text.replace(before,after));bad.with_name('resource_selection.h').write_bytes((SOURCE/'resource_selection.h').read_bytes())
        wrong,body,unused,image=build(bad,folder/'build',True);rejected=[]
        for ordinal,f in enumerate(fixtures()):
            if f['address']!=address:continue
            try:outcome=run(body,f,image,ordinal)
            except (ValueError,AssertionError)as error:rejected.append(dict(ordinal=ordinal,reason=type(error).__name__));continue
            if outcome['modelFailures']:rejected.append(dict(ordinal=ordinal,failures=outcome['modelFailures']))
        if not rejected:raise ValueError(('Actual wrong C escaped bounded models',label))
        negatives.append(dict(name=label,proof=wrong,rejected=rejected))
    controls=[]
    info,image,symbols=linker.measured_module('main')
    for ref in read_json(LANE/'claim.json')['claimedFunctions']:
        rejected=[]
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(int(ref['address'],0)+4)),('bytes',ref['bytes']-4),('targetSha256','0'*64)]:
            wrong=copy.deepcopy(ref);wrong[key]=value
            try:original(wrong,image,symbols)
            except ValueError:rejected.append(key)
            else:raise ValueError('Wrong resource namespace/complete boundary escaped')
        folder=WORK/'proof/prototype'/f"{int(ref['address'],0):08x}";folder.mkdir(parents=True,exist_ok=True)
        source=SOURCE/(f"{int(ref['address'],0):08x}"+'.c');bad=folder/source.name;bad.write_bytes(source.read_bytes())
        header=(SOURCE/'resource_selection.h').read_text()
        before='native_main_02061088(u32,u32,u32)'if int(ref['address'],0)==0x02061088 else'native_main_02061470(void)'
        after='native_main_02061088(u32,u32,u16)'if int(ref['address'],0)==0x02061088 else'native_main_02061470(u32)'
        if header.count(before)!=1:raise ValueError('Actual public prototype mutation ambiguous')
        bad.with_name('resource_selection.h').write_text(header.replace(before,after))
        failed,unused=compare(bad,folder/'compile')
        if len(failed)!=1 or not failed[0].get('compileFailed'):raise ValueError('Actual contradictory resource prototype escaped compiler')
        controls.append(dict(address=ref['address'],namespaceRejected=rejected,actualCompilerPrototypeRejected=True,diagnostic=failed[0]))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();(LANE/'traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    helpers=helper_contracts(image)
    report=dict(schemaVersion=1,status='behavior-qualified-C-API-nonmatching',romSha256=configuration()['romSha256'],sourceCredit=0,matched=False,functions=rows,originalFunctions=2,originalBytes=700,compiledBytes=sum(r['compiledBytes']for r in rows),pairs=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),actualNativeHelperReturnsPerSide=sum(len(t['observation']['actualHelperReturns'])for t in traces),realHelpers=helpers,realHelperBytes=sum(h['bytes']for h in helpers),nativeWholeFunctionMatch=False,rawRegisterDifferences=raw_differences,negativeEvidence=negatives,generatedTrace=dict(path=(LANE/'traces.json.gz').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest()),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=['Canonical u32 path APIs remain unchanged. Two readable ordinary C functions compile/link genuinely to436/272B versus432/268B originals; four-byte path-address cache residuals are preserved, with zero source credit.','The tested projection is the C ABI: return word, callee-saved registers/SP, complete supplied-interface arguments/order, CPU writes outside owned512B stack, actual helper returns and8MiB RAM excluding source-code/private-stack ranges.','Full raw GPR/CPSR are retained. Caller-clobbered r1/r2/r3/r12/LR and NZCV differences are reported rather than claimed equal. This is not exact machine-state or all actual native-caller continuation closure.','Ten original helper bodies execute. Formatter/file/archive/allocator/video-transfer leaves remain explicit supplied interfaces; no real filesystem, assets, hardware, global object extent or helper/data source credit.','Distinct identical format literals remain distinct; signed numeric default arguments,2-byte selector rows,8-byte buffer rows,4-byte word lanes, late buffer-cell reload, rounded word copy and palette halfword/clamp models are bounded measured contracts.'])
    report['bindingPrototypeControls']=controls
    write_json(LANE/'working-report.json',report)
    print(dict(functions=2,originalBytes=700,compiledBytes=report['compiledBytes'],pairs=len(traces),actualHelperReturnsPerSide=report['actualNativeHelperReturnsPerSide'],sourceCredit=0),flush=True)


if __name__=='__main__':main()
