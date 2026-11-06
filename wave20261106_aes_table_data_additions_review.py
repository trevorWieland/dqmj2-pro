import subprocess
from project import ROOT,read_json,write_json,sha256,configuration
import recovery_registry as registry
import source_selection
import build_modules
from ledger_state import collect_matches
from wave20261106_aes_table_data_paths import EVIDENCE,WORK,SOURCE
from wave20261106_aes_table_data_build import ELFFile
from wave20261106_aes_table_data_additions import selected_data,identity,membership,validate,qualify


def reject(cases,label,call):
    try:call()
    except(ValueError,AssertionError,KeyError)as error:cases.append(dict(case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong AES data addition accepted:'+label)


def main():
    folder=WORK/'addition-review';folder.mkdir(parents=True,exist_ok=True);claim=read_json(EVIDENCE/'data-claim.json');revision=claim['sourceRevision'];reg=folder/'recovery-private.json';pref=folder/'preferences-private.json';reg.write_bytes(subprocess.check_output(['git','show',revision+':recovery.json'],cwd=ROOT));pref.write_bytes(subprocess.check_output(['git','show',revision+':source-preferences.json'],cwd=ROOT));old_registry=registry.REGISTRY;old_preferences=source_selection.preferences;old_work=build_modules.WORK;report='evidence/matches/aes-table-data-20261106.json';descriptor=(EVIDENCE/'canonical-packet.json').relative_to(ROOT).as_posix()
    try:
        registry.REGISTRY=reg;source_selection.preferences=lambda namespace:old_preferences(namespace,path=pref);before=selected_data();functions,bad=collect_matches(configuration()['romSha256'])
        if bad:raise ValueError('Closed167 existing private function projection failed:'+str(bad)[:400])
        registry.register(ROOT/report,['wave20261106_aes_table_data_packet.py',descriptor]);after=selected_data();after_functions,bad=collect_matches(configuration()['romSha256'])
        if bad or after_functions!=functions:raise ValueError('Private AES data registration changed earlier source functions')
        expected=claim['claimedStorage'];layout,admitted,assets=membership(before,after,expected,functions);key=sorted(admitted)[0];row=after[key];cases=[]
        reject(cases,'missing-whole-table',lambda:membership(before,{k:v for k,v in after.items()if k!=key},expected,functions))
        reject(cases,'wrong-whole-extent',lambda:membership(before,after,[dict(r,bytes=r['bytes']+4)if identity(r)==key else r for r in expected],functions))
        changed=dict(after);changed[key]=dict(row,module='ov000');reject(cases,'wrong-overlay-namespace',lambda:membership(before,changed,expected,functions))
        old_key=next(iter(before));changed=dict(after);changed[old_key]=dict(before[old_key],sourceSha256='0'*64);reject(cases,'earlier-data-source-mutated',lambda:membership(before,changed,expected,functions))
        changed=dict(after);changed[old_key]=dict(before[old_key],realLink={'forged':True});reject(cases,'earlier-data-proof-mutated',lambda:membership(before,changed,expected,functions))
        changed_functions=dict(functions);changed_functions['private-overlap-control']=dict(row,kind='thumb',mode='thumb',size=1024);reject(cases,'earlier-function-overlap',lambda:membership(before,after,expected,changed_functions))
        overlap_key=(*key[:4],key[4]-4);overlap=dict(row,address=hex(key[4]-4),bytes=8,size=8);changed_before=dict(before);changed_before[overlap_key]=overlap;changed_after=dict(after);changed_after[overlap_key]=overlap;reject(cases,'earlier-data-overlap',lambda:membership(changed_before,changed_after,expected,functions))
        image=(ROOT/assets[key]['binary']).read_bytes()
        for label,field,value in [('false-exact','exactBytes',False),('wrong-data-compiler','compilerFlags',['-O0']),('missing-real-header','sourceDependencies',[]),('missing-semantic-generator-input','dataSourceDependencies',row['dataSourceDependencies'][:1]),('wrong-semantic-source','semanticSource','work/w6at/wrong.json'),('wrong-overlay-label','nativeAlias','data_ov000_022088b8'),('wrong-placement-section','targetSection','.data'),('false-BSS-credit','allocatedZeroFillBytes',1),('extra-interior-view-credit','interiorViewExtraBytes',4)]:
            changed=dict(row);changed[field]=value;reject(cases,label,lambda changed=changed:validate(changed,assets[key],admitted[key],layout,image))
        print(dict(privateBeforeData=len(before),privateAfterData=len(after),unchangedFunctions=len(functions),negativeControls=len(cases),freshLinksStarting=10),flush=True);proof=qualify(before,after,expected,functions,folder/'fresh-links')
        build_modules.WORK=folder/'module-projection';build_modules.WORK.mkdir(parents=True,exist_ok=True);units_path=build_modules.collect_units(None,[ROOT/report]);units=read_json(units_path);stage=dict(sourceUnits=[]);build_modules.prepare_units(units_path,stage)
        if len(units['units'])!=10 or len(stage['sourceUnits'])!=10 or sum(r['compiledBytes']for r in stage['sourceUnits'])!=10240:raise ValueError('Private AES standard staging inflated/dropped whole arrays')
        report_rows=read_json(ROOT/report)['dataMatches'];view_proofs=[]
        for unit in stage['sourceUnits']:
            source_row=next(r for r in report_rows if int(r['address'],0)==int(unit['start'],0))
            if unit['kind']!='data'or unit['section']!='.rodata'or unit['sourceSection']!='.rodata'or unit['symbols']!={source_row['nativeAlias']:source_row['nativeSymbol']}or not unit['prelinkUnrelocatedByteCheckPassed']:raise ValueError('Private AES standard rodata/alias staging differs')
            with open(unit['stagedObject'],'rb')as stream:
                elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
                for view in source_row['existingConfiguredInteriorElementViews']:
                    found=[s for s in symbols if s.name==view['nativeAlias']]
                    if len(found)!=1 or(found[0]['st_info']['type'],found[0]['st_size'],found[0]['st_value'])!=('STT_OBJECT',0,view['byteOffset']):raise ValueError('Existing AES ambiguous interior element export was fabricated/moved/credited')
                    config=(build_modules.WORK/'config-arm9/overlays/ov006/symbols.txt').read_text().splitlines()
                    if view['originalOverlay6ConfiguredRecord']not in config:raise ValueError('Existing AES original ambiguous qualifier was removed/renamed')
                    view_proofs.append(dict(alias=view['nativeAlias'],type='STT_OBJECT',size=0,offset=view['byteOffset'],originalAmbiguousRecordPreserved=True))
        original_main=ROOT/'config/arm9/relocs.txt';staged_main=build_modules.WORK/'config-arm9/relocs.txt'
        if sha256(original_main)!=sha256(staged_main)or len(view_proofs)!=3:raise ValueError('Private AES staging changed plural main relocations or dropped ambiguous views')
        projected=dict(wholeUnits=10,wholeInitializedBytes=10240,sourceAndTargetSection='.rodata',threeGenuineInteriorSTT_OBJECTSizeZeroExports=view_proofs,ambiguousQualifiersPreserved=True,allMainPluralRelocationsUnchanged=True,unitSpec=units_path.relative_to(ROOT).as_posix(),unitSpecSha256=sha256(units_path),noSharedModuleLinkRun=True)
    finally:registry.REGISTRY=old_registry;source_selection.preferences=old_preferences;build_modules.WORK=old_work
    value=dict(passed=True,qualification=proof,negativeControls=cases,privateBaselineRevision=revision,selectedDataBefore=len(before),selectedDataAfter=len(after),unchangedSelectedFunctions=len(functions),privateRegistry=dict(path=reg.relative_to(ROOT).as_posix(),sha256=sha256(reg)),privateStandardModuleProjection=projected,allProcessLocalOverridesRestored=True,noSharedWritesOrWholeModuleBuild=True,qualifierSha256=sha256(ROOT/'wave20261106_aes_table_data_additions.py'),reviewerSha256=sha256(__file__),sourceCreditPendingSharedAcceptance=True);write_json(EVIDENCE/'addition-compatibility-review.json',value);print(dict(passed=True,tables=10,bytes=10240,negativeControls=len(cases),freshGenuineLinks=10,stagedSizeZeroInteriorAliases=3),flush=True)


if __name__=='__main__':main()
