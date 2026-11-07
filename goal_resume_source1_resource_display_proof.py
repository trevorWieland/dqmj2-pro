import copy
import gzip
import hashlib
import json
import struct
import sys
from project import ROOT, configuration, read_json, sha256, write_json
from goal_resume_source1_compile import compare
import link_runtime_unit as linker
import match_runtime as compiler
import unicorn
from unicorn import arm_const as R

LANE=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/resource-display'
SOURCE=ROOT/'src/runtime/goal_resume20261106/source_1/tail'
WORK=ROOT/'work/goal-resume-20261106/source-1/resource-display-proof'
ADDRESS,RESOURCE,VALUES=0x020724f4,0x021c9698,0x021c4f78
SP,STOP,CELLS,WIDGET,RENDER,OBSERVER=0x027f0000,0x027d0000,0x02102a18,0x02702000,0x02703000,0x02705000
HELPERS={0x02061dcc:24,0x02049ad0:20,0x02049ffc:20,0x0204abd4:76}
SERVICES={0x02087e44:2,0x02048f9c:1,0x0204a858:6}


def original(row,image,symbols,records):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],int(row['address'],0),row['bytes'])!=('','arm9','main','arm',ADDRESS,116):
        raise ValueError('Whole claimed resource-display identity differs')
    native=image[ADDRESS-0x02000000:ADDRESS-0x02000000+116]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or 'func_020724f4 kind:function(arm,size=0x74) addr:0x020724f4' not in symbols.splitlines():
        raise ValueError('Whole original resource-display bytes or boundary differs')
    expected=[(20,1,'native_fn_02061dcc',0x02061dcc,-8),(48,1,'native_fn_02049ffc',0x02049ffc,-8),
        (96,1,'native_fn_0204abd4',0x0204abd4,-8),(108,2,'native_data_021c9698',RESOURCE,0),(112,2,'native_data_021c4f78',VALUES,0)]
    actual=[(r['offset'],r['type'],r['symbol'],int(r['target'],0),r['addend']) for r in row['relocations']]
    if actual!=expected:
        raise ValueError('Original function/data origins or raw addends differ')
    for offset,target in [(108,RESOURCE),(112,VALUES)]:
        if struct.unpack_from('<I',native,offset)[0]!=target or f'from:0x{ADDRESS+offset:08x} kind:load to:0x{target:08x} module:main' not in records.splitlines():
            raise ValueError('Original physical literal word or load provenance differs')
        if f'data_{target:08x} kind:bss addr:0x{target:08x}' not in symbols.splitlines():
            raise ValueError('Referenced physical BSS origin lacks original identity')
    for address,extent in HELPERS.items():
        if f'func_{address:08x} kind:function(arm,size={hex(extent)}) addr:0x{address:08x}' not in symbols.splitlines():
            raise ValueError('Executed original helper boundary differs')
    for origin,target in [(0x02061de0,0x02049ad0),(0x0204a00c,0x02087e44)]:
        if struct.unpack_from('<I',image,origin-0x02000000)[0]!=target or f'from:0x{origin:08x} kind:load to:0x{target:08x} module:main' not in records.splitlines():
            raise ValueError('Original native tail-call target provenance differs')
    if struct.unpack_from('<I',image,0x49ae0)[0]!=CELLS or f'from:0x02049ae0 kind:load to:0x{CELLS:08x} module:main' not in records.splitlines():
        raise ValueError('Real native dispatcher table origin differs')
    return native


def build(source,directory,negative=False):
    rows,unused=compare(source,directory/'compile')
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError('One genuine compiled resource-display function is required')
    row=dict(rows[0],program='')
    info,image,symbols=linker.measured_module('main')
    if not negative:
        original(row,image,symbols,(ROOT/'config/arm9/relocs.txt').read_text())
    bindings={name:dict(program='',processor='arm9',module='main',mode=mode,kind=kind,address=hex(address))
        for name,address,mode,kind in [('native_fn_02061dcc',0x02061dcc,'arm','function'),
            ('native_fn_02049ffc',0x02049ffc,'arm','function'),('native_fn_0204abd4',0x0204abd4,'arm','function'),
            ('native_data_021c9698',RESOURCE,'data','data'),('native_data_021c4f78',VALUES,'data','data')]}
    try:
        proof=linker.validate(row,bindings,directory/'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):
            raise
        proof=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Wrong C unexpectedly matched the whole original caller')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):
        raise ValueError('Real link changed original source relocation payloads')
    row.update(realLink=proof,nativeSymbolEntries=bindings,sourceLanguage='C',ordinaryCBytes=0 if negative else 116,
        justifiedAssemblyBytes=0,sourceDependencies=[dict(path=source.with_name('resource_display.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('resource_display.h')))])
    return row,(directory/'link/caller.bin').read_bytes(),image


def fixtures():
    return [dict(index=index,selection=selection,mutate=mutate,flags=flags)
        for index in [-36,-1,0,91,92] for selection in range(4) for mutate in [False,True] for flags in [0,15]]


def run(body,fixture,image,ordinal):
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000)
    vm.mem_write(0x02000000,image)
    vm.mem_write(ADDRESS,body)
    initial_values=[0,1,0x80000000,0xffffffff]
    changed_values=[7,0,2,0x80000001]
    vm.mem_write(VALUES,struct.pack('<4I',*initial_values))
    slot=((fixture['index']+36+128)%256)-128
    vm.mem_write(CELLS+12*slot,struct.pack('<I',WIDGET))
    vm.mem_write(WIDGET,struct.pack('<2I',0x11223344,RENDER))
    vm.mem_write(RENDER,bytes((i*7+31)&255 for i in range(80)))
    handle=0x12340000+ordinal
    vm.mem_write(RENDER+0x44,struct.pack('<I',handle))
    initial_render=bytes(vm.mem_read(RENDER,80))
    vm.mem_write(SP-512,bytes((i*19+ordinal*11+7)&255 for i in range(768)))
    initial=[0x11220000+n*0x1234+ordinal for n in range(15)]
    initial[0],initial[1],initial[13],initial[14]=fixture['index']&0xffffffff,fixture['selection'],SP,STOP
    vm.reg_write(R.UC_ARM_REG_CPSR,fixture['flags']<<28|0x10)
    for register,value in zip(compiler.REGISTERS,initial):
        vm.reg_write(register,value)
    calls,writes,frames,returns=[],[],[],[]
    returned=False
    def memory(vm,access,address,size,value,user):
        writes.append([address,size,value])
    def code(vm,address,size,user):
        nonlocal returned
        while frames and address==frames[-1][0]:
            returns.append(hex(frames.pop()[1]))
        if address==STOP:
            returned=True
            vm.emu_stop()
            return
        if address in HELPERS:
            frames.append((vm.reg_read(R.UC_ARM_REG_LR),address))
        if address==0x02049ad0:
            calls.append(dict(address=hex(address),arguments=[vm.reg_read(R.UC_ARM_REG_R0)]))
        if address in SERVICES:
            width=SERVICES[address]
            args=[vm.reg_read(register) for register in compiler.REGISTERS[:min(width,4)]]
            if width>4:
                args.extend(struct.unpack('<'+'I'*(width-4),bytes(vm.mem_read(vm.reg_read(R.UC_ARM_REG_SP),4*(width-4)))))
            call=dict(address=hex(address),arguments=args)
            result=0
            if address==0x02087e44 and fixture['mutate']:
                vm.mem_write(VALUES+4*fixture['selection'],struct.pack('<I',changed_values[fixture['selection']]))
            elif address==0x0204a858:
                call['coordinates']=list(struct.unpack('<2h',bytes(vm.mem_read(args[2],4))))
                vm.mem_write(OBSERVER,struct.pack('<6I2hI',*args,*call['coordinates'],ordinal))
            calls.append(call)
            for index,register in enumerate(compiler.REGISTERS[:4]):
                vm.reg_write(register,result if index==0 else 0xa5000000+ordinal*16+index+len(calls)*256)
            vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10)
            vm.reg_write(R.UC_ARM_REG_PC,vm.reg_read(R.UC_ARM_REG_LR))
            return
        if ADDRESS<=address<ADDRESS+len(body)-8:
            return
        if any(start<=address<start+extent-(4 if start in (0x02061dcc,0x02049ad0,0x02049ffc) else 0) for start,extent in HELPERS.items()):
            return
        raise ValueError('Resource display entered an unowned instruction or literal pool')
    vm.hook_add(unicorn.UC_HOOK_CODE,code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    vm.emu_start(ADDRESS,STOP+4,count=500)
    if not returned or frames:
        raise ValueError('Caller or actual original helper did not return')
    selected=fixture['selection']
    value=(changed_values if fixture['mutate'] else initial_values)[selected]
    slot=((fixture['index']+36+128)%256)-128
    expected=[dict(address='0x2049ad0',arguments=[slot&0xffffffff]),dict(address='0x2087e44',arguments=[handle,0])]
    if value:
        expected.extend([dict(address='0x2048f9c',arguments=[0]),
            dict(address='0x204a858',arguments=[fixture['index']&0xffffffff,RESOURCE,SP-24,1,value,1],coordinates=[0,0])])
    registers=[vm.reg_read(register) for register in compiler.REGISTERS]
    failures=[]
    if calls!=expected:
        failures.append('Independent signed-byte delegated slot, reset handle, live selection and six-word render model')
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:
        failures.append('Original callee-saved ABI and stack depth')
    wanted_values=list(initial_values)
    if fixture['mutate']:
        wanted_values[selected]=changed_values[selected]
    if bytes(vm.mem_read(VALUES,16))!=struct.pack('<4I',*wanted_values) or bytes(vm.mem_read(RENDER,80))!=initial_render:
        failures.append('Only supplied reset service mutates selection snapshot; renderer prefix untouched')
    wanted=struct.pack('<6I2hI',*expected[-1]['arguments'],0,0,ordinal) if value else bytes(32)
    if bytes(vm.mem_read(OBSERVER,32))!=wanted:
        failures.append('Independent renderer observation record')
    if len(returns)!=(4 if value else 3):
        failures.append('Actual getter/reset/wrapper return closure')
    return dict(modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,
        actualHelperReturns=returns,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())


def main():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':
        raise ValueError('Pinned fixture runtime differs')
    if (LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:
                raise ValueError('Frozen resource-display input changed: '+pin['path'])
    LANE.mkdir(parents=True,exist_ok=True)
    row,body,image=build(SOURCE/'020724f4.c',WORK/'positive')
    symbols=(ROOT/'config/arm9/symbols.txt').read_text()
    records=(ROOT/'config/arm9/relocs.txt').read_text()
    native=original(row,image,symbols,records)
    traces=[]
    for ordinal,fixture in enumerate(fixtures()):
        a,b=run(native,fixture,image,ordinal),run(body,fixture,image,ordinal)
        if a!=b or a['modelFailures']:
            write_json(WORK/'failed-vector.json',dict(fixture=fixture,native=a,source=b))
            raise ValueError('Actual resource display/source or independent model differs')
        traces.append(dict(fixture=fixture,result=a))
    variants=[('wrong-resource-origin','resource=native_data_021c9698;','resource=native_data_021c9698+1;'),
        ('wrong-zero-condition','if(value!=0)','if(value==0)'),
        ('wrong-coordinate-y','native_fn_02049ffc(target);','native_fn_02049ffc(target); point.y=1;')]
    negative=[]
    text=(SOURCE/'020724f4.c').read_text()
    for index,(name,before,after) in enumerate(variants):
        if before not in text:
            raise ValueError('Wrong-C control did not alter source')
        directory=WORK/'n'/str(index)
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'020724f4.c'
        source.write_text(text.replace(before,after))
        source.with_name('resource_display.h').write_bytes((SOURCE/'resource_display.h').read_bytes())
        wrong,code,image=build(source,directory,negative=True)
        rejected=[]
        for ordinal,fixture in enumerate(fixtures()):
            result=run(code,fixture,image,ordinal)
            if result['modelFailures']:
                rejected.append(ordinal)
        if not rejected:
            raise ValueError('Meaningful wrong C escaped independent fixture models')
        negative.append(dict(name=name,rejectedVectors=rejected,source=wrong['source'],sourceSha256=wrong['sourceSha256'],object=wrong['object'],objectSha256=wrong['objectSha256'],realLink=wrong['realLink']))
    rejected=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(ADDRESS+4)),('bytes',112),('targetSha256','0'*64)]:
        wrong=copy.deepcopy(row)
        wrong[key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append(key)
        else:
            raise ValueError('Wrong physical identity or partial caller escaped gate')
    for key,value in [('offset',104),('addend',2),('target',hex(RESOURCE+2))]:
        wrong=copy.deepcopy(row)
        wrong['relocations'][-2][key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append('resource-'+key)
        else:
            raise ValueError('Wrong resource origin escaped gate')
    write_json(LANE/'binding-controls.json',dict(passed=True,rejected=rejected,sourceCredit=0))
    directory=WORK/'prototype'
    directory.mkdir(parents=True,exist_ok=True)
    source=directory/'020724f4.c'
    source.write_bytes((SOURCE/'020724f4.c').read_bytes())
    source.with_name('resource_display.h').write_text((SOURCE/'resource_display.h').read_text().replace('native_main_020724f4(s32,u32)','native_main_020724f4(unsigned short,u32)'))
    bad,unused=compare(source,directory/'compile')
    if len(bad)!=1 or not bad[0].get('compileFailed'):
        raise ValueError('Conflicting public16-bit prototype escaped real compiler')
    write_json(LANE/'prototype-control.json',dict(passed=True,actualCompilerRejected=True,sourceCredit=0))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    (LANE/'traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    info,unused,unused=linker.measured_module('main')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=info['sha256'],
        allPassed=True,matches=[dict(row,behaviorQualified=True)],canonicalMatchedFunctions=1,canonicalMatchedBytes=116,cases=len(traces),
        acceptedSourceCredit=0,actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=4,
        actualNativeHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns']) for t in traces),externalStorageCredit=0,
        nativeSymbols={name:binding['address'] for name,binding in row['nativeSymbolEntries'].items()},nativeSymbolBindings=row['nativeSymbolEntries'],
        negativeEvidence=negative,bindingLayoutControls=dict(path=(LANE/'binding-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-controls.json')),
        generatedTrace=dict(path=(LANE/'traces.json.gz').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest()),
        producer=__file__.split('\\')[-1].split('/')[-1],producerSha256=sha256(__file__),
        limits=['Whole original116-byte caller and genuinely compiled/MW-linked116-byte ordinary C match including complete literal pool and unchanged raw relocations; acceptance remains pending shared gates.',
            '80 original/source pairs include signed-byte getter delegation, zero/high-bit values and reset-service mutation before the live selection load; fullGPR/CPSR/orderedCPUwrites/8MiBRAM equality.',
            'Actual original24-byte getter,20-byte dispatcher,20-byte reset tail and76-byte resource wrapper execute unchanged on both sides; supplied services terminate at reset-handle/state/renderer boundaries.',
            'Four selector cells, five caller-index stress values and valid bounded pointer prefixes are fixture state; unsupported objects/indices, full scenes and hardware are not qualified.',
            'All external BSS, resources, helpers and original callee bodies have zero new data/source credit.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=1,bytes=116,pairs=len(traces),actualReturns=2*len(traces),actualHelperReturnsPerSide=report['actualNativeHelperReturnsPerSide'],sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
