import hashlib
import re
import struct
import subprocess
import sys
from pathlib import Path
from project import ROOT,configuration,verify_inputs,read_json,write_json,sha256
sys.path.insert(0,str(ROOT/'deps/native'))
from elftools.elf.elffile import ELFFile

WORK=ROOT/'work/w5weak/source-scope-v1'
LANE=ROOT/'evidence/lanes/parallel-wave20261105/weak-source-export-scope'
BUILD=ROOT/'build/link-work'
DSD_SHA='5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932'
TARGETS=[('original-asm','native_main_02000800','SDK_WEAK_SYMBOL asm void _start(void)'),('branch-following','native_main_02008430','SDK_WEAK_SYMBOL void OS_Terminate(void)')]


def inspect(path,name,companion=None,companion_base=None):
    with Path(path).open('rb') as stream:
        elf=ELFFile(stream);table=elf.get_section_by_name('.symtab');symbols=list(table.iter_symbols())
        matches=[(i,s) for i,s in enumerate(symbols) if s.name==name and isinstance(s['st_shndx'],int)]
        assert len(matches)==1,(str(path),name)
        index,symbol=matches[0];section=elf.get_section(symbol['st_shndx']);offset=(symbol['st_value']&~1)-section['sh_addr']
        body=section.data()[offset:offset+symbol['st_size']]
        body_source='ELF section'
        if len(body)!=symbol['st_size']:
            assert companion is not None and companion_base is not None
            initialized=Path(companion).read_bytes();position=(symbol['st_value']&~1)-companion_base
            body=initialized[position:position+symbol['st_size']]
            body_source='MW out-of-line initialized binary; ELF carries symbols'
        assert len(body)==symbol['st_size']
        relocs=[]
        for relsection in elf.iter_sections():
            if relsection['sh_type'] not in ['SHT_REL','SHT_RELA'] or relsection['sh_info']!=symbol['st_shndx']:continue
            for rel in relsection.iter_relocations():
                where=rel['r_offset']
                if not offset<=where<offset+len(body):continue
                relocs.append(dict(offset=where-offset,type=rel['r_info_type'],symbol=symbols[rel['r_info_sym']].name,
                    addend=rel.entry.get('r_addend'),encodedWord=section.data()[where:where+4].hex()))
        raw=table.data()[index*16+12]
        return dict(path=str(Path(path).relative_to(ROOT)),sha256=sha256(path),name=name,rawStInfo=hex(raw),binding=raw>>4,
            type=raw&15,address=hex(symbol['st_value']),bytes=symbol['st_size'],bodySha256=hashlib.sha256(body).hexdigest(),bodySource=body_source,
            relocations=sorted(relocs,key=lambda r:r['offset'])),body


def reloc_shape(row):
    return [(r['offset'],r['type'],r['addend'],r['encodedWord']) for r in row['relocations']]


def replace_scope(text,names):
    counts={name:0 for name in names};result=[]
    for line in text.splitlines(keepends=True):
        name=line.split(' ',1)[0]
        if name in names:
            assert ' weak' not in line and ' local' not in line
            counts[name]+=1;line=line.rstrip('\r\n')+' weak\n'
        result.append(line)
    assert all(count==1 for count in counts.values()),counts
    return ''.join(result)


def check_case(label,base_config,base_symbols,names,expected_success,expected_errors):
    folder=WORK/label;folder.mkdir(parents=True,exist_ok=True)
    symbols=folder/'symbols.txt';symbols.write_text(replace_scope(base_symbols,names))
    original=(BUILD/'config-arm9/symbols.txt').as_posix()
    assert base_config.count(original)==1
    config=folder/'config.yaml';config.write_text(base_config.replace(original,symbols.as_posix()))
    command=[str(ROOT/'tools/dsd.exe'),'check','symbols','--config-path',str(config),'--elf-path',str(BUILD/'linked.elf'),'--fail']
    result=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=180)
    output=result.stdout+result.stderr
    success=result.returncode==0
    assert success==expected_success,(label,result.returncode,output[-3000:])
    errors=re.findall(r"Symbol '([^']+)'[^\n]*expected to be[^\n]*",output)
    assert set(errors)==set(expected_errors),(label,errors,expected_errors,output[-3000:])
    (folder/'check.txt').write_text(output)
    print(label,'passed' if success else 'rejected',errors,flush=True)
    return dict(label=label,argv=command,cwd=str(folder.relative_to(ROOT)),exitCode=result.returncode,
        strictCheckPassed=success,expectedMismatches=expected_errors,reportedMismatches=errors,
        generatedConfigSha256=sha256(config),generatedSymbolsSha256=sha256(symbols),outputSha256=sha256(folder/'check.txt'))


def main():
    assert not (LANE/'receipt.json').exists(),'Proof receipt is immutable after publication'
    config=configuration();original=verify_inputs(config)
    assert sha256(ROOT/'tools/dsd.exe')==DSD_SHA
    units=read_json(BUILD/'source-units.json')['units'];by_name={r.get('function'):r for r in units}
    protected=[BUILD/'linked.elf',BUILD/'arm9.lcf',BUILD/'config.yaml',BUILD/'source-units.json',ROOT/'config/arm9/symbols.txt']
    protected+=list((BUILD/'config-arm9').rglob('*'))+list((BUILD/'build').glob('*.bin'))
    protected=[p for p in protected if p.is_file()]
    before={str(p.relative_to(ROOT)):sha256(p) for p in protected}
    base_config=(BUILD/'config.yaml').read_text();base_symbols=(BUILD/'config-arm9/symbols.txt').read_text()
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();evidence=[];pins=[]
    for packet,name,published_decl in TARGETS:
        lane=ROOT/f'evidence/lanes/parallel-wave20261104/main-sdk-prefix/{packet}'
        inputs=read_json(lane/'inputs.json');item=next(r for r in inputs['entries'] if Path(r['source']).stem==name)
        match=next(r for r in read_json(lane/'match.json')['matches'] if r['name']==name)
        unit=by_name[name];source=ROOT/item['source'];reference=ROOT/item['provenance']['referenceSource']
        assert sha256(source)==item['sourceSha256']==unit['sourceSha256']
        assert sha256(reference)==item['provenance']['referenceSourceSha256']
        normalized=lambda s:re.sub(r'\s+',' ',s)
        assert published_decl in normalized(reference.read_text())
        assert re.search(r'__declspec\(weak\)\s+(?:asm\s+)?void\s+'+name+r'\s*\(',source.read_text())
        for pin in item['sourceDependencies']:assert sha256(ROOT/pin['path'])==pin['sha256']
        compiler,raw=inspect(ROOT/unit['object'],name)
        assert compiler['sha256']==unit['sha256']==match['objectSha256']
        isolated_split,isolated_raw=inspect(Path(match['realLink']['linkerAttempt']['cwd'])/'caller.o',name)
        isolated_binary=Path(match['realLink']['linkerAttempt']['cwd'])/'caller.bin'
        assert sha256(isolated_binary)==match['realLink']['linkedCallerSha256']
        isolated_final,isolated_code=inspect(ROOT/match['realLink']['linkedElf'],name,isolated_binary,int(item['address'],0))
        staged,staged_raw=inspect(BUILD/(name+'.o'),name)
        final,code=inspect(BUILD/'linked.elf',name,BUILD/'build/arm9.bin',0x02000000)
        assert all(row['binding']==14 and row['type']==2 and row['bytes']==item['bytes'] for row in [compiler,isolated_split,isolated_final,staged,final])
        assert raw==isolated_raw==staged_raw
        assert reloc_shape(compiler)==reloc_shape(isolated_split)==reloc_shape(staged)
        aliases={int(k):v for k,v in unit['relocationAliases'].items()}
        assert all(b['symbol']==aliases.get(a['offset'],a['symbol']) for a,b in zip(compiler['relocations'],staged['relocations']))
        address=int(item['address'],0);native=image[address-0x02000000:address-0x02000000+item['bytes']]
        assert code==isolated_code==native and final['bodySha256']==item['targetSha256']
        line=next(line for line in base_symbols.splitlines() if line.startswith(name+' '));assert ' weak' not in line
        evidence.append(dict(name=name,address=item['address'],bytes=item['bytes'],publishedSource=str(reference.relative_to(ROOT)),
            publishedSourceSha256=sha256(reference),publishedWeakDeclaration=published_decl,source=str(source.relative_to(ROOT)),
            sourceSha256=sha256(source),originalCompiler=compiler,isolatedSplit=isolated_split,isolatedLinked=isolated_final,
            sharedSplit=staged,sharedLinked=final,generatedRecordBefore=line,generatedRecordAfter=line+' weak',
            fullNativeBytesUnchanged=True,originalRelocationTypesAddendsAndEncodedWordsUnchanged=True))
        pins += [source,reference,ROOT/unit['object'],lane/'inputs.json']
        pins += [ROOT/p['path'] for p in item['sourceDependencies']]
    aliases={}
    for name in ['Entry','func_02008430']:
        row,unused=inspect(BUILD/'linked.elf',name);assert row['binding']==1;aliases[name]=row
    strong='native_main_02000a78';row,unused=inspect(BUILD/'linked.elf',strong,BUILD/'build/arm9.bin',0x02000000);assert row['binding']==1
    names={r['name'] for r in evidence}
    cases=[check_case('baseline',base_config,base_symbols,set(),False,sorted(names)),
        check_case('preserved-two-weak-exports',base_config,base_symbols,names,True,[]),
        check_case('missing-start-weak',base_config,base_symbols,names-{'native_main_02000800'},False,['native_main_02000800']),
        check_case('missing-terminate-weak',base_config,base_symbols,names-{'native_main_02008430'},False,['native_main_02008430']),
        check_case('wrong-strong-export-marked-weak',base_config,base_symbols,names|{strong},False,[strong])]
    after={str(p.relative_to(ROOT)):sha256(p) for p in protected};assert before==after
    assert verify_inputs(config)==original
    primary=['tools/ds-decomp-source/cli/src/config/symbol.rs','tools/ds-decomp-source/cli/src/cmd/check/symbols.rs','tools/ds-decomp-source/lib/src/config/symbol.rs']
    assert 'const STB_MWARM_WEAK: u8 = 14;' in (ROOT/primary[0]).read_text()
    assert 'matching_symbol.scope.is_weak() && !target_symbol.scope.is_weak()' in (ROOT/primary[1]).read_text()
    assert 'scope.unwrap_or(SymbolScope::Global)' in (ROOT/primary[2]).read_text()
    report=dict(schemaVersion=1,allPassed=True,createdFromReadOnlySharedArtifacts=True,sourceOrCodeByteCredit=0,
        rootCause='Weak binding14 is retained in every compiler/split/linked stage. Generated config renaming preserves implicitGlobal scope instead of the proven SDK weak source-export scope.',
        diagnosticDirection='The unchanged dsd checker emits expected-weak/nonweak when the matching ELF symbol is weak but generated target config is notweak.',
        originalStrongAliasesAreNotTheImmediateMismatch=True,strongAliasesRetainOriginalScopes=aliases,
        onlyGeneratedCanonicalSourceExportRecordsChange=True,sourceHeadersObjectsInstructionsRelocationsLcfAndOriginalConfigUntouched=True,
        recommendedConsumerFile='build_modules.py',recommendedConsumerFunction='prepare_units',
        recommendedInsertion='After verifying the selected compiler symbol and before writing each renamed canonical config record, retain scopeweak for exactly these two proven SDK exports. Derive from their actual binding14 plus pinned source/public weak-declaration witness; do not alter aliases, other strong exports or checker semantics.',
        records=evidence,cases=cases,originalInputs=original,originalInputsShaPreserved=True,sharedArtifactsShaPreserved=True,
        protectedSharedArtifacts=before,primaryConsumerSources=[dict(path=p,sha256=sha256(ROOT/p)) for p in primary],
        sourcePins=[dict(path=str(p.relative_to(ROOT)),sha256=sha256(p)) for p in sorted(set(pins))],
        dsdSha256=DSD_SHA,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        limitation='Private metadata proof only. Coordinator owns shared consumer integration and subsequent full shared gates.')
    write_json(LANE/'receipt.json',report)
    write_json(LANE/'proven-weak-exports.json',dict(schemaVersion=1,scope='generated-canonical-source-export-records-only',
        exports=[{k:r[k] for k in ['name','address','bytes','source','sourceSha256','publishedSource','publishedSourceSha256','publishedWeakDeclaration']} for r in evidence],
        requiredCompilerBinding=14,definedFunctionOnly=True,originalAliasesAndStrongScopesUnchanged=True,sourceByteCredit=0))
    print(dict(receipt=str((LANE/'receipt.json').relative_to(ROOT)),sha256=sha256(LANE/'receipt.json'),strictPositive=True,negativeControls=3),flush=True)


if __name__=='__main__':main()
