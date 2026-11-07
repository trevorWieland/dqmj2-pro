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

LANE=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/detail-display'
SOURCE=ROOT/'src/runtime/goal_resume20261106/source_1/tail'
WORK=ROOT/'work/goal-resume-20261106/source-1/detail-display-proof'
ADDRESS,MENU,CELLS=0x020721b4,0x021c4f60,0x02102a18
SP,STOP,WIDGET,RENDER,DETAIL,SECOND,OBSERVER=0x027f0000,0x027d0000,0x02702000,0x02703000,0x02704000,0x02704100,0x02705000
HELPERS={0x02061dcc:24,0x02049ad0:20,0x02049ffc:20,0x0206dc54:28,0x0206dca4:44}
SERVICES={0x02087e44:2,0x020602ec:6,0x02087a48:6,0x0204aaf0:7}


def original(row,image,symbols,records):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],int(row['address'],0),row['bytes'])!=('','arm9','main','arm',ADDRESS,456):
        raise ValueError('Whole claimed detail-display identity differs')
    native=image[ADDRESS-0x02000000:ADDRESS-0x02000000+456]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256'] or 'func_020721b4 kind:function(arm,size=0x1c8) addr:0x020721b4' not in symbols.splitlines():
        raise ValueError('Whole original detail-display bytes or boundary differs')
    expected=[(12,1,0x02061dcc,-8),(52,1,0x02049ffc,-8),(60,1,0x0206dc54,-8),(68,1,0x0206dca4,-8),
        (168,1,0x020602ec,-8),(224,1,0x020602ec,-8),(268,1,0x02087a48,-8),(324,1,0x020602ec,-8),
        (368,1,0x02087a48,-8),(432,1,0x0204aaf0,-8),(444,2,MENU,0),(448,2,0x020de3c4,0),(452,2,0x020de3d8,0)]
    actual=[(r['offset'],r['type'],int(r['target'],0),r['addend']) for r in row['relocations']]
    if actual!=expected:
        raise ValueError('Original function/data origins or addends differ')
    for offset,target in [(444,MENU),(448,0x020de3c4),(452,0x020de3d8)]:
        if struct.unpack_from('<I',native,offset)[0]!=target or f'from:0x{ADDRESS+offset:08x} kind:load to:0x{target:08x} module:main' not in records.splitlines():
            raise ValueError('Complete original literal word or load provenance differs')
    for address,extent in HELPERS.items():
        if f'func_{address:08x} kind:function(arm,size={hex(extent)}) addr:0x{address:08x}' not in symbols.splitlines():
            raise ValueError('Executed original helper extent lacks configured boundary')
    for origin,target in [(0x02061de0,0x02049ad0),(0x02049ae0,CELLS),(0x0204a00c,0x02087e44),(0x0206dc6c,MENU),(0x0206dccc,MENU)]:
        if struct.unpack_from('<I',image,origin-0x02000000)[0]!=target or f'from:0x{origin:08x} kind:load to:0x{target:08x} module:main' not in records.splitlines():
            raise ValueError('Original helper data/tail-target provenance differs')
    return native


def build(source,directory,negative=False):
    rows,unused=compare(source,directory/'compile')
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError('One genuine compiled detail-display function is required')
    row=dict(rows[0],program='')
    info,image,symbols=linker.measured_module('main')
    if not negative:
        original(row,image,symbols,(ROOT/'config/arm9/relocs.txt').read_text())
    bindings={rel['symbol']:dict(program='',processor='arm9',module='main',address=rel['target'],
        mode='data' if rel['type']==2 else 'arm',kind='data' if rel['type']==2 else 'function') for rel in row['relocations']}
    try:
        proof=linker.validate(row,bindings,directory/'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):
            raise
        proof=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Wrong C unexpectedly matched the whole original function')
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):
        raise ValueError('Genuine caller split changed source relocation payloads')
    row.update(realLink=proof,nativeSymbolEntries=bindings,sourceLanguage='C',ordinaryCBytes=0 if negative else 456,
        justifiedAssemblyBytes=0,sourceDependencies=[dict(path=source.with_name('detail_display.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('detail_display.h')))])
    return row,(directory/'link/caller.bin').read_bytes(),image


def fixtures():
    states=[('absent',False,0,0,0,0,None),('zero',True,0,13,-27,0,None),
        ('filled',True,71,123,-7,0,None),('missing',True,71,0,0,0,None),
        ('blocked',True,71,123,-7,-128,None),('mutated-blocked',True,71,124,-8,0,9),
        ('mutated-open',True,71,124,-8,1,9),('mutated-zero',True,71,124,-8,0,0)]
    return [dict(index=index,label=label,present=present,value18=value18,value40=value40,value42=value42,
        flag=flag,newValue18=new_value) for index in [-1,0,5,6,7,8,9,10,11]
        for label,present,value18,value40,value42,flag,new_value in states]


def run(body,fixture,image,ordinal):
    f=fixture
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000)
    vm.mem_write(0x02000000,image)
    vm.mem_write(ADDRESS,body)
    slot=((f['index']+36+128)%256)-128
    cell=CELLS+12*slot
    vm.mem_write(cell,struct.pack('<I',WIDGET))
    vm.mem_write(WIDGET,struct.pack('<2I',0x11223344,RENDER))
    vm.mem_write(RENDER,bytes((i*7+31)&255 for i in range(80)))
    handle=0x12340000+ordinal
    vm.mem_write(RENDER+0x44,struct.pack('<I',handle))
    vm.mem_write(MENU+0x20,struct.pack('<I',DETAIL if f['present'] else 0))
    vm.mem_write(MENU+0x2f,bytes([f['flag']&255]))
    for pointer,values in [(DETAIL,(f['value18'],f['value40'],f['value42'])),(SECOND,(f['newValue18'] or 0,201,202))]:
        vm.mem_write(pointer,bytes((i*11+ordinal*3)&255 for i in range(128)))
        for offset,value in zip([0x18,0x40,0x42],values):
            vm.mem_write(pointer+offset,struct.pack('<h',value))
    vm.mem_write(SP-512,bytes((i*19+ordinal*11+7)&255 for i in range(768)))
    initial=[0x11220000+n*0x1234+ordinal for n in range(15)]
    initial[0],initial[13],initial[14]=f['index']&0xffffffff,SP,STOP
    vm.reg_write(R.UC_ARM_REG_CPSR,(15 if ordinal%2 else 0)<<28|0x10)
    for register,value in zip(compiler.REGISTERS,initial):
        vm.reg_write(register,value)
    calls,writes,frames,returns=[],[],[],[]
    returned=False
    def memory(vm,access,address,size,value,user):
        writes.append([address,size,value])
    def code(vm,address,size,user):
        nonlocal returned
        while frames and address==frames[-1][0]:
            returns.append(dict(address=hex(frames.pop()[1]),value=vm.reg_read(R.UC_ARM_REG_R0)))
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
            result=0x80000000+ordinal
            if address==0x02087e44:
                if f['newValue18'] is not None:
                    vm.mem_write(MENU+0x20,struct.pack('<I',SECOND))
                    vm.mem_write(MENU+0x2f,bytes([0 if f['flag'] else 1]))
            else:
                result={0x020602ec:0x80001000,0x02087a48:0x80002000,0x0204aaf0:0x80003000}[address]+ordinal
                if address==0x0204aaf0:
                    call['coordinates']=list(struct.unpack('<2h',bytes(vm.mem_read(args[1],4))))
                record=json.dumps(call,sort_keys=True,separators=(',',':')).encode()
                vm.mem_write(OBSERVER,hashlib.sha256(record).digest())
            calls.append(call)
            for index,register in enumerate(compiler.REGISTERS[:4]):
                vm.reg_write(register,result if index==0 else 0xa5000000+ordinal*16+index+len(calls)*256)
            vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10)
            vm.reg_write(R.UC_ARM_REG_PC,vm.reg_read(R.UC_ARM_REG_LR))
            return
        if ADDRESS<=address<ADDRESS+len(body)-12:
            return
        if any(start<=address<start+extent-4 for start,extent in HELPERS.items()):
            return
        raise ValueError('Detail display entered an unowned instruction or literal pool')
    vm.hook_add(unicorn.UC_HOOK_CODE,code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    vm.emu_start(ADDRESS,STOP+4,count=1500)
    if not returned or frames:
        raise ValueError('Caller or actual native helper did not return')
    flag=(0 if f['flag'] else 1) if f['newValue18'] is not None else f['flag']
    active=f['newValue18']!=0 if f['newValue18'] is not None else f['present'] and f['value18']!=0
    expected=[dict(address='0x2049ad0',arguments=[slot&0xffffffff]),dict(address='0x2087e44',arguments=[handle,0])]
    result=1 if active else 0
    if active:
        if f['index']==6:
            expected.append(dict(address='0x20602ec',arguments=[WIDGET,f['value18']&0xffffffff,DETAIL,0,0,1]))
            result=0x80001000+ordinal
        elif f['index'] in (8,10):
            value=f['value40'] if f['index']==8 else f['value42']
            if flag==0 and value:
                expected.append(dict(address='0x20602ec',arguments=[WIDGET,value&0xffffffff,DETAIL+(0x52 if f['index']==8 else 0x66),0,0,1]))
                result=0x80001000+ordinal
            else:
                expected.append(dict(address='0x2087a48',arguments=[RENDER,0,0,0,1,0x020de3c4 if f['index']==8 else 0x020de3d8]))
                result=0x80002000+ordinal
        elif f['index'] in (7,9):
            expected.append(dict(address='0x204aaf0',arguments=[f['index'],SP-28,5,2,13 if f['index']==7 else 14,1,1],coordinates=[0,0]))
            result=0x80003000+ordinal
    registers=[vm.reg_read(register) for register in compiler.REGISTERS]
    failures=[]
    if calls!=expected or registers[0]!=result:
        failures.append('Independent captured-detail/live-mode flag, switch result and renderer register/stack argument model')
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:
        failures.append('Preserved original caller ABI and stack depth')
    helpers=[(0x02049ad0,cell),(0x02061dcc,cell),(0x02049ffc,0x80000000+ordinal),(0x0206dc54,1 if flag==0 else 0),(0x0206dca4,1 if active else 0)]
    if returns!=[dict(address=hex(address),value=value) for address,value in helpers]:
        failures.append('Actual native dispatcher/tails, ignored-input mode flag and live-null/value18 provider returns')
    wanted=hashlib.sha256(json.dumps(expected[-1],sort_keys=True,separators=(',',':')).encode()).digest() if len(expected)>2 else bytes(32)
    if bytes(vm.mem_read(OBSERVER,32))!=wanted:
        failures.append('Independent bounded renderer observation')
    if struct.unpack('<I',bytes(vm.mem_read(MENU+0x20,4)))[0]!=(SECOND if f['newValue18'] is not None else DETAIL if f['present'] else 0):
        failures.append('Only supplied handle service changes global detail pointer')
    return dict(modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,
        actualHelperReturns=returns,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())


def main():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':
        raise ValueError('Pinned fixture runtime differs')
    if (LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:
                raise ValueError('Frozen detail-display input changed: '+pin['path'])
    LANE.mkdir(parents=True,exist_ok=True)
    row,body,image=build(SOURCE/'020721b4.c',WORK/'positive')
    symbols=(ROOT/'config/arm9/symbols.txt').read_text()
    records=(ROOT/'config/arm9/relocs.txt').read_text()
    native=original(row,image,symbols,records)
    traces=[]
    for ordinal,fixture in enumerate(fixtures()):
        a,b=run(native,fixture,image,ordinal),run(body,fixture,image,ordinal)
        if a!=b or a['modelFailures']:
            write_json(WORK/'failed-vector.json',dict(fixture=fixture,native=a,source=b))
            raise ValueError('Actual detail-display/source or independent model differs')
        traces.append(dict(fixture=fixture,result=a))
    variants=[('wrong-selector','index==7?13:14','index==7?12:14'),
        ('wrong-mode-gate','available!=0 &&','available==0 &&'),
        ('stale-vs-live-detail','native_fn_02049ffc(renderer);','native_fn_02049ffc(renderer); detail=native_data_021c4f60.detail;')]
    negative=[]
    text=(SOURCE/'020721b4.c').read_text()
    for index,(name,before,after) in enumerate(variants):
        if before not in text:
            raise ValueError('Wrong-C control did not alter actual source')
        directory=WORK/'n'/str(index)
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'020721b4.c'
        source.write_text(text.replace(before,after))
        source.with_name('detail_display.h').write_bytes((SOURCE/'detail_display.h').read_bytes())
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
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(ADDRESS+4)),('bytes',444),('targetSha256','0'*64)]:
        wrong=copy.deepcopy(row)
        wrong[key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append(key)
        else:
            raise ValueError('Wrong physical identity or incomplete caller escaped gate')
    for key,value in [('offset',440),('addend',4),('target',hex(MENU+4))]:
        wrong=copy.deepcopy(row)
        wrong['relocations'][-3][key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append('menu-'+key)
        else:
            raise ValueError('Wrong menu-field origin escaped gate')
    write_json(LANE/'binding-controls.json',dict(passed=True,rejected=rejected,sourceCredit=0))
    directory=WORK/'prototype'
    directory.mkdir(parents=True,exist_ok=True)
    source=directory/'020721b4.c'
    source.write_bytes((SOURCE/'020721b4.c').read_bytes())
    source.with_name('detail_display.h').write_text((SOURCE/'detail_display.h').read_text().replace('native_main_020721b4(s32)','native_main_020721b4(unsigned short)'))
    bad,unused=compare(source,directory/'compile')
    if len(bad)!=1 or not bad[0].get('compileFailed'):
        raise ValueError('Conflicting public16-bit prototype escaped actual compiler')
    write_json(LANE/'prototype-control.json',dict(passed=True,actualCompilerRejected=True,sourceCredit=0))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    (LANE/'traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    info,unused,unused=linker.measured_module('main')
    abi=ROOT/'evidence/lanes/parallel-wave20261106/goal-resume-source-1/detail-display-abi-proposal/proposal.json'
    proposal=read_json(abi)
    if not proposal['bodyUnchanged'] or not proposal['allocatedObjectContractEqual'] or not proposal['rawFunctionRelocationsEqual'] or proposal['sourceCredit']:
        raise ValueError('Required coordinator ABI proposal lacks unchanged-body/object proof')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',moduleSha256=info['sha256'],
        allPassed=True,matches=[dict(row,behaviorQualified=True)],canonicalMatchedFunctions=1,canonicalMatchedBytes=456,cases=len(traces),
        acceptedSourceCredit=0,actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecuted=5,
        actualNativeHelperReturnsPerSide=sum(len(t['result']['actualHelperReturns']) for t in traces),externalStorageCredit=0,
        nativeSymbols={name:binding['address'] for name,binding in row['nativeSymbolEntries'].items()},nativeSymbolBindings=row['nativeSymbolEntries'],
        negativeEvidence=negative,bindingLayoutControls=dict(path=(LANE/'binding-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-controls.json')),
        generatedTrace=dict(path=(LANE/'traces.json.gz').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest()),
        producer=__file__.split('\\')[-1].split('/')[-1],producerSha256=sha256(__file__),
        acceptanceDependencies=[dict(owner='coordinator',status='unresolved',sourceCredit=0,
            proposal=abi.relative_to(ROOT).as_posix(),proposalSha256=sha256(abi),
            requirement='Repair accepted0206dc54 C parameter compatibility without code/relocation changes before accepting or publishing this456-byte caller.')],
        limits=['Whole original456-byte caller and genuinely compiled/MW-linked456-byte ordinary C match, preserving the full literal pool and raw source relocations; acceptance remains pending shared gates.',
            '72 paired cases cover nine switch indices, null/zero/live detail, availability flags and supplied handle-service mutation; actual getter/dispatcher/reset/mode providers execute136original bytes on both sides.',
            'Modeflag0206dc54 ignores forwardedR0 and reads menu.flag2f. Acceptance and publication are blocked until the coordinator applies the separately proposed zero-credit compatible unused-parameter ABI repair.',
            'Renderer arguments/returns and captured-detail versus live-global gating follow independent models; fullGPR/CPSR/orderedCPUwrites/8MiBRAM agree.',
            'Handle and three renderer services are bounded supplied interfaces; no complete UI, scenes or hardware claim, and no helper/BSS/data source credit.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=1,bytes=456,pairs=len(traces),actualReturns=2*len(traces),actualHelperReturnsPerSide=report['actualNativeHelperReturnsPerSide'],sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
