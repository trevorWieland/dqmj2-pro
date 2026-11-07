import copy
import match_runtime
from elftools.elf.elffile import ELFFile
from project import ROOT,read_json


def verify(row):
    if(row['address'],row['bytes'],row['processor'],row['module'],row['mode'])!=('0x27f60b4',1156,'arm7','arm7-main','arm'):raise ValueError('Exact RTC source-owned boundary differs')
    group='native_host_arm7_data_027f8e34';binding=row['nativeSymbolEntries'][group]
    if(binding['program'],binding['processor'],binding['module'],binding['kind'],binding['mode'],binding['address'],binding['region'])!=('','arm7','arm7-main','data','data','0x27f8e34','bss'):raise ValueError('Genuine original imported RTC data/BSS view differs')
    with(ROOT/row['object']).open('rb')as stream:
        elf=ELFFile(stream);sections=[dict(name=s.name,type=s['sh_type'],flags=s['sh_flags'],bytes=s['sh_size'])for s in elf.iter_sections()if s['sh_flags']&2]
        if any(s['bytes']and not s['flags']&4 for s in sections):raise ValueError('Source object unexpectedly defines allocated noncode storage')
        symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==group)
        if(symbol['st_shndx'],symbol['st_info']['bind'],symbol['st_info']['type'],symbol['st_size'],symbol['st_value'])!=('SHN_UNDEF','STB_GLOBAL','STT_NOTYPE',0,0):raise ValueError('Imported group is not a genuine source-generated undefined global')
    original=read_json(ROOT/'evidence/lanes/parallel-wave20261106/arm7-rtc-loop-next/claim.json')['importedGlobalView'];rels=[r for r in row['relocations']if r['type']==2];projection=[]
    for reference in original['actualOriginalDataConstraints']:
        selected=[r for r in rels if r['offset']==reference['offset']]
        if len(selected)!=1:raise ValueError('Exact original RTC literal relocation absent')
        rel=selected[0];address=int(binding['address'],0)+rel['explicitAddend']
        if rel['symbol']!=group or rel['format']!='SHT_RELA'or rel['originalEncodedWord']!='00000000'or address!=int(reference['nativeWord'],0):raise ValueError('Natural source group relocation changes genuine effective native reference')
        oldValue=4 if reference['primarySymbol']=='rtcWork'else 0
        if oldValue+reference['explicitAddend']!=rel['explicitAddend']:raise ValueError('Before-compile typed view does not preserve original section-relative storage offset')
        projection.append(dict(offset=rel['offset'],originalSourceSymbol=reference['primarySymbol'],originalSymbolBinding=reference['primaryBinding'],originalSymbolSectionValue=oldValue,originalExplicitAddend=reference['explicitAddend'],newSourceSymbol=group,newExplicitAddend=rel['explicitAddend'],effectiveOriginalNativeAddress=hex(address),sourceTransformationBeforeCompilation=True,compiledElfLocalRebinding=False))
    if len(rels)!=3:raise ValueError('Unqualified extra RTC data relocations')
    return dict(status='passed',sourceCredit=0,sourceAllocatedSections=sections,sourceDefinedStorage=0,initializedStorageCredit=0,importedGroup=dict(symbol=group,binding=binding,consumedPrefixBytes=478,sourceViewTypeBytes=952,nativeFullAllocationProven=False),originalToSourceGroupProjection=projection,postCompileSymbolOrRelocationModification=False)


def controls(row,compile_unit):
    from wave20261106_arm7_rtc_loop_source_first_build import SOURCE,WORK
    result=verify(row);rejected=[]
    for label,key,value in[('base-plus4','address','0x27f8e38'),('wrong-region','region','initialized'),('wrong-program','program','dwc/utility.bin/move/child.srl')]:
        altered=copy.deepcopy(row);altered['nativeSymbolEntries']['native_host_arm7_data_027f8e34'][key]=value
        try:verify(altered)
        except ValueError as error:rejected.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong imported RTC storage contract admitted')
    directory=WORK/'storage-negative';directory.mkdir(parents=True,exist_ok=True)
    for path in(SOURCE/'027f60b4').glob('*'):
        if path.suffix not in['.c','.h']:continue
        text=path.read_text(encoding='utf-8');old='extern RTCImportedView native_host_arm7_data_027f8e34;';new='RTCImportedView native_host_arm7_data_027f8e34;';(directory/path.name).write_text(text.replace(old,new),encoding='utf-8')
    attempt=compile_unit(directory/'main.c',directory/'bad.o',True)
    if attempt['exitCode']:raise ValueError('Coherent source-owned storage negative did not compile')
    altered=copy.deepcopy(row);altered['object']=(directory/'bad.o').relative_to(ROOT).as_posix()
    try:verify(altered)
    except ValueError as error:rejected.append(dict(case='new-source-defined-global-storage',rejected=True,reason=str(error),actualSourceCompile=attempt))
    else:raise ValueError('Unadmitted source-owned RTC BSS allocation accepted')
    return dict(positive=result,negativeControls=rejected)
