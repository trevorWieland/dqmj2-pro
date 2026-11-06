from project import ROOT,configuration,read_json,write_json,native_dependencies,sha256
native_dependencies(configuration())
from link_arm7 import accepted,build_module
from elftools.elf.elffile import ELFFile


def main():
    report_path=ROOT/'evidence/matches/arm7-lane-thread-init240-20261031.json'
    report=read_json(report_path);row=report['matches'][0];functions,symbols=accepted()
    previous=[f for f in functions if f['module']==row['module'] and int(f.get('address','0'),0)==int(row['address'],0)]
    assert len(previous)<=1
    if previous:assert previous[0]['sourceSha256']==row['sourceSha256'] and previous[0]['objectSha256']==row['objectSha256']
    else:functions.append({**report,**row})
    for name,value in report['nativeSymbols'].items():
        if name in symbols:assert int(symbols[name],0)==int(value,0)
        symbols[name]=value
    module=next(m for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules'] if m['name']=='arm7-wram')
    directory=ROOT/'work/arm7-thread-init240-module-probe-20261031'
    result,units=build_module(module,functions,symbols,configuration(),output_root=directory)
    assert result['exactBytes'] and result['symbolCheckPassed']
    with (directory/'arm7-wram/linked.elf').open('rb') as stream:
        elf=ELFFile(stream);table={s.name:s for s in elf.get_section_by_name('.symtab').iter_symbols()};checks=[]
        for name in ['SDK_SYS_STACKSIZE','SDK_IRQ_STACKSIZE']:
            symbol=table[name];assert symbol['st_value']==0x400 and symbol['st_size']==0
            checks.append({'name':name,'value':symbol['st_value'],'size':symbol['st_size'],'sectionIndex':symbol['st_shndx'],'numericOnly':True,'memoryPermissionGranted':False})
    output={'sourceCredit':0,'registrySha256':sha256(ROOT/'recovery.json'),'candidateReportSha256':sha256(report_path),'report':result,'candidateAlreadyRegistered':bool(previous),'candidateInitializedBytes':240,'constants':checks,'sharedLinkerPolicyChanged':False,'acceptedRegistryChanged':False,'moduleOutputSha256':result['outputSha256'],'limitations':['Whole-module bytes include all current registered source and explicit original gaps; this does not prove source-only completion','Two qualified numeric linker symbols do not define memory objects, permissions or initialized-data credit']}
    write_json(ROOT/'evidence/verification/arm7-thread-init240-whole-module-probe-20261031.json',output)
    print({'wholeWramExact':True,'qualifiedIntegerSymbols':2,'candidateBytes':240,'sourceCredit':0})


if __name__=='__main__':main()
