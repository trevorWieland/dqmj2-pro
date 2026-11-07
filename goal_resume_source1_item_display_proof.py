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

LANE = ROOT / 'evidence/lanes/parallel-wave20261106/goal-resume-source-1/item-display'
SOURCE = ROOT / 'src/runtime/goal_resume20261106/source_1/tail'
WORK = ROOT / 'work/goal-resume-20261106/source-1/item-display-proof'
ADDRESS, DATA, PROVIDER = 0x0207483c, 0x021c5df8, 0x02063144
SP, STOP, OBSERVER = 0x027f0000, 0x027d0000, 0x02705000
VALUES = [0, 1, 254, 255, 256, 0x7fff, 0x8000, 0xffff, 0x12345]


def original(row, image, symbols, records):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],int(row['address'],0),row['bytes']) != ('','arm9','main','arm',ADDRESS,148):
        raise ValueError('Whole claimed item-display identity differs')
    native = image[ADDRESS-0x02000000:ADDRESS-0x02000000+148]
    if hashlib.sha256(native).hexdigest()!=row['targetSha256']:
        raise ValueError('Original item-display bytes differ')
    if 'func_0207483c kind:function(arm,size=0x94) addr:0x0207483c' not in symbols.splitlines():
        raise ValueError('Whole item-display boundary is missing')
    expected=[(44,1,'native_fn_02063144',PROVIDER,-8),
        (88,1,'native_fn_0204a448',0x0204a448,-8),(132,1,'native_fn_0204a154',0x0204a154,-8),
        (144,2,'native_data_021c5df8',DATA,0)]
    actual=[(r['offset'],r['type'],r['symbol'],int(r['target'],0),r['addend']) for r in row['relocations']]
    if actual!=expected:
        raise ValueError('Original function entries or item-table origin/addends differ')
    if 'from:0x020748cc kind:load to:0x021c5df8 module:main' not in records.splitlines():
        raise ValueError('Original item-table literal record is missing')
    if struct.unpack_from('<I',native,144)[0]!=DATA:
        raise ValueError('Original item-table pointer word differs')
    if 'func_02063144 kind:function(arm,size=0x18) addr:0x02063144' not in symbols.splitlines():
        raise ValueError('Executed original provider boundary is missing')
    table=struct.unpack_from('<I',image,PROVIDER-0x02000000+20)[0]
    if f'from:0x02063158 kind:load to:0x{table:08x} module:main' not in records.splitlines():
        raise ValueError('Original provider table origin is missing')
    if f'data_{table:08x} kind:bss addr:0x{table:08x}' not in symbols.splitlines():
        raise ValueError('Provider fixture table lacks original BSS identity')
    return native,table


def build(source,directory,negative=False):
    rows,unused=compare(source,directory/'compile')
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError('One genuine compiled item-display function is required')
    row=dict(rows[0],program='')
    info,image,symbols=linker.measured_module('main')
    if not negative:
        native,table=original(row,image,symbols,(ROOT/'config/arm9/relocs.txt').read_text())
    bindings={name:dict(program='',processor='arm9',module='main',mode=mode,kind=kind,address=hex(address))
        for name,address,mode,kind in [('native_fn_02063144',PROVIDER,'arm','function'),
            ('native_fn_0204a448',0x0204a448,'arm','function'),('native_fn_0204a154',0x0204a154,'arm','function'),
            ('native_data_021c5df8',DATA,'data','data')]}
    try:
        proof=linker.validate(row,bindings,directory/'link')
    except ValueError as error:
        if not negative or not error.args or not isinstance(error.args[0],dict):
            raise
        proof=dict(exactCallerBytes=False,comparison=error.args[0])
    if negative and proof['exactCallerBytes']:
        raise ValueError('Wrong C unexpectedly matched the whole original function')
    body=(directory/'link/caller.bin').read_bytes()
    if linker.relocation_rows(ROOT/row['object'],row['name'])!=linker.relocation_rows(directory/'link/caller.o',row['name']):
        raise ValueError('Actual linker split changed source relocation payloads')
    row.update(realLink=proof,nativeSymbolEntries=bindings,sourceLanguage='C',ordinaryCBytes=0 if negative else 148,
        justifiedAssemblyBytes=0,sourceDependencies=[dict(path=source.with_name('item_display.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('item_display.h')))])
    return row,body,image


def fixtures():
    return [dict(index=index,flags=flags) for index in range(len(VALUES)) for flags in [0,2,6,15]]


def run(body,fixture,image,ordinal):
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000)
    vm.mem_write(0x02000000,image)
    vm.mem_write(ADDRESS,body)
    vm.mem_write(DATA,struct.pack('<9I',*VALUES))
    table=struct.unpack_from('<I',image,PROVIDER-0x02000000+20)[0]
    vm.mem_write(table-32768,bytes((i*7+ordinal*13+101)&255 for i in range(33024)))
    vm.mem_write(SP-256,bytes((i*19+ordinal*11+7)&255 for i in range(512)))
    initial=[0x11220000+n*0x1234+ordinal for n in range(15)]
    initial[0],initial[13],initial[14]=fixture['index'],SP,STOP
    vm.reg_write(R.UC_ARM_REG_CPSR,fixture['flags']<<28|0x10)
    for register,value in zip(compiler.REGISTERS,initial):
        vm.reg_write(register,value)
    calls,writes,provider_steps=[],[],[]
    returned=False
    provider_return=None
    helper_returns=0
    def memory(vm,access,address,size,value,user):
        writes.append([address,size,value])
    def code(vm,address,size,user):
        nonlocal returned,provider_return,helper_returns
        if provider_return==address:
            helper_returns+=1
            provider_return=None
        if address==STOP:
            returned=True
            vm.emu_stop()
            return
        if address==PROVIDER:
            calls.append(dict(address=hex(address),arguments=[vm.reg_read(R.UC_ARM_REG_R0)]))
            provider_return=vm.reg_read(R.UC_ARM_REG_LR)
        if PROVIDER<=address<PROVIDER+20:
            provider_steps.append(address-PROVIDER)
            return
        if address in (0x0204a448,0x0204a154):
            stack=vm.reg_read(R.UC_ARM_REG_SP)
            args=[vm.reg_read(register) for register in compiler.REGISTERS[:4]]
            args.extend(struct.unpack('<2I',bytes(vm.mem_read(stack,8))))
            coords=list(struct.unpack('<2h',bytes(vm.mem_read(args[1],4))))
            calls.append(dict(address=hex(address),arguments=args,coordinates=coords))
            record=struct.pack('<6I2hI',*args,*coords,ordinal)
            vm.mem_write(OBSERVER+(len(calls)-2)*32,record)
            for index,register in enumerate(compiler.REGISTERS[:4]):
                vm.reg_write(register,0xa5000000+ordinal*16+index+len(calls)*256)
            vm.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10)
            vm.reg_write(R.UC_ARM_REG_PC,vm.reg_read(R.UC_ARM_REG_LR))
            return
        if not ADDRESS<=address<ADDRESS+len(body)-4:
            raise ValueError('Item display entered an unowned instruction or literal pool')
    vm.hook_add(unicorn.UC_HOOK_CODE,code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory)
    vm.emu_start(ADDRESS,STOP+4,count=300)
    if not returned or provider_return is not None or helper_returns!=1:
        raise ValueError('Actual caller or original provider failed to return')
    selected=((VALUES[fixture['index']]+32768)%65536)-32768
    value=0 if selected>=255 else ((selected+32768)*7+ordinal*13+101)&255
    if value>=128:
        value-=256
    value&=0xffffffff
    expected=[dict(address=hex(PROVIDER),arguments=[selected&0xffffffff]),
        dict(address='0x204a448',arguments=[1,SP-16,1,selected&0xffffffff,0,1],coordinates=[16,0]),
        dict(address='0x204a154',arguments=[1,SP-16,1,value,4,0],coordinates=[184,0])]
    registers=[vm.reg_read(register) for register in compiler.REGISTERS]
    failures=[]
    if calls!=expected:
        failures.append('Independent signed-item/provider lookup, six-word renderer ABI and coordinate model')
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:
        failures.append('Preserved caller ABI and original stack depth')
    observer=b''.join(struct.pack('<6I2hI',*call['arguments'],*call['coordinates'],ordinal) for call in expected[1:])
    if bytes(vm.mem_read(OBSERVER,64))!=observer:
        failures.append('Independent bounded renderer observation records')
    return dict(modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),
        calls=calls,writes=writes,providerInstructions=provider_steps,actualProviderReturns=helper_returns,
        fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())


def controls(row,image):
    symbols=(ROOT/'config/arm9/symbols.txt').read_text()
    records=(ROOT/'config/arm9/relocs.txt').read_text()
    rejected=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','thumb'),('address',hex(ADDRESS+4)),('bytes',144),('targetSha256','0'*64)]:
        wrong=copy.deepcopy(row)
        wrong[key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append(key)
        else:
            raise ValueError('Wrong physical identity or partial function escaped scope gate')
    for key,value in [('offset',140),('addend',4),('target',hex(DATA+4))]:
        wrong=copy.deepcopy(row)
        wrong['relocations'][-1][key]=value
        try:
            original(wrong,image,symbols,records)
        except ValueError:
            rejected.append('data-'+key)
        else:
            raise ValueError('Wrong original data origin escaped scope gate')
    return rejected


def main():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':
        raise ValueError('Pinned fixture runtime differs')
    if (LANE/'inputs.json').exists():
        for pin in read_json(LANE/'inputs.json')['files']:
            if sha256(ROOT/pin['path'])!=pin['sha256']:
                raise ValueError('Frozen item-display input changed: '+pin['path'])
    LANE.mkdir(parents=True,exist_ok=True)
    row,body,image=build(SOURCE/'0207483c.c',WORK/'positive')
    native,table=original(row,image,(ROOT/'config/arm9/symbols.txt').read_text(),(ROOT/'config/arm9/relocs.txt').read_text())
    traces=[]
    for ordinal,fixture in enumerate(fixtures()):
        a,b=run(native,fixture,image,ordinal),run(body,fixture,image,ordinal)
        if a!=b or a['modelFailures']:
            write_json(WORK/'failed-vector.json',dict(fixture=fixture,native=a,source=b))
            raise ValueError('Actual item-display caller/source or independent model differs')
        traces.append(dict(fixture=fixture,result=a))
    variants=[('wrong-coordinate-y','point.x=16;','point.x=16; point.y=1;'),
        ('unsigned-item-id','s16 selected=(s16)','u16 selected=(u16)'),
        ('wrong-second-coordinate','point.x=184;','point.x=183;')]
    negative=[]
    text=(SOURCE/'0207483c.c').read_text()
    for index,(name,before,after) in enumerate(variants):
        if before not in text:
            raise ValueError('Wrong-C control did not change source')
        directory=WORK/'n'/str(index)
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'0207483c.c'
        source.write_text(text.replace(before,after))
        source.with_name('item_display.h').write_bytes((SOURCE/'item_display.h').read_bytes())
        wrong,code,image=build(source,directory,negative=True)
        rejected=[]
        for ordinal,fixture in enumerate(fixtures()):
            result=run(code,fixture,image,ordinal)
            if result['modelFailures']:
                rejected.append(ordinal)
        if not rejected:
            raise ValueError('Meaningful wrong C escaped fixture models')
        negative.append(dict(name=name,rejectedVectors=rejected,source=wrong['source'],sourceSha256=wrong['sourceSha256'],
            object=wrong['object'],objectSha256=wrong['objectSha256'],realLink=wrong['realLink']))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    (LANE/'traces.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    write_json(LANE/'binding-controls.json',dict(passed=True,rejected=controls(row,image),sourceCredit=0))
    directory=WORK/'prototype'
    directory.mkdir(parents=True,exist_ok=True)
    source=directory/'0207483c.c'
    source.write_bytes((SOURCE/'0207483c.c').read_bytes())
    source.with_name('item_display.h').write_text((SOURCE/'item_display.h').read_text().replace('native_main_0207483c(s32)','native_main_0207483c(unsigned short)'))
    rejected,unused=compare(source,directory/'compile')
    if len(rejected)!=1 or not rejected[0].get('compileFailed'):
        raise ValueError('Conflicting16-bit public caller prototype escaped real compiler')
    write_json(LANE/'prototype-control.json',dict(passed=True,actualCompilerRejected=True,sourceCredit=0))
    info,unused,unused=linker.measured_module('main')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',
        moduleSha256=info['sha256'],allPassed=True,matches=[dict(row,behaviorQualified=True)],
        functionMatches=1,sourceBytes=148,acceptedSourceCredit=0,vectors=len(traces),
        canonicalMatchedFunctions=1,canonicalMatchedBytes=148,cases=len(traces),nativeCalleeBodiesExecuted=1,externalStorageCredit=0,
        nativeSymbols={name:binding['address'] for name,binding in row['nativeSymbolEntries'].items()},
        nativeSymbolBindings=row['nativeSymbolEntries'],
        actualNativeAndSourceCallerReturns=2*len(traces),actualOriginalProviderReturnsPerSide=len(traces),
        negativeControls=negative,negativeEvidence=negative,producer='goal_resume_source1_item_display_proof.py',
        producerSha256=sha256(ROOT/'goal_resume_source1_item_display_proof.py'),
        bindingLayoutControls=dict(path=(LANE/'binding-controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'binding-controls.json')),
        generatedTrace=dict(path=(LANE/'traces.json.gz').relative_to(ROOT).as_posix(),
            sha256=sha256(LANE/'traces.json.gz'),uncompressedSha256=hashlib.sha256(raw).hexdigest()),
        originalProvider=dict(address=hex(PROVIDER),bytes=24,table=hex(table),sha256=hashlib.sha256(image[PROVIDER-0x02000000:PROVIDER-0x02000000+24]).hexdigest(),sourceCredit=0),
        limits=['Whole original148-byte caller and genuine freshly compiled/MW-linked148-byte ordinary C agree byte for byte; no accepted credit before shared gates.',
            'Nine supplied item words and four incoming condition states; actual original24-byte provider executes on both sides, including signed16 truncation and signed-byte lookup into a supplied original-BSS table snapshot.',
            'Two renderer services are bounded supplied six-word interfaces with real stack coordinate reads and independent observations; no complete UI, scene or hardware execution claim.',
            'Full registers/flags/ordered CPU writes and8MiB RAM agree; indices outside0..8 and unsupported owner/UI state are not qualified.',
            'Provider BSS snapshot and preceding guards are synthetic fixture state, never authored source/data credit; negative truncated IDs are bounded stress observations rather than a valid-game-ID claim. Original provider has no new source credit.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=1,bytes=148,vectors=len(traces),actualReturns=2*len(traces),actualProviderReturnsPerSide=len(traces),negativeControls=len(negative),sourceCredit=0),flush=True)


if __name__=='__main__':
    main()
