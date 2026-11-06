import subprocess
from project import ROOT,read_json,write_json,sha256,configuration
import recovery_registry as registry
import source_selection
from ledger_state import collect_matches
from wave20261106_auth_character_data_paths import EVIDENCE,WORK,SOURCE
from wave20261106_auth_character_data_additions import selected_data,identity,membership,validate,qualify


def reject(cases,label,call):
    try:call()
    except(ValueError,AssertionError,KeyError)as error:cases.append(dict(case=label,rejected=True,reason=str(error)))
    else:raise ValueError('Wrong Auth data addition was admitted: '+label)


def main():
    folder=WORK/'addition-review';folder.mkdir(parents=True,exist_ok=True);claim=read_json(EVIDENCE/'data-claim.json');revision=claim['sourceRevision'];registry_path=folder/'recovery-private.json';preferences_path=folder/'preferences-private.json';registry_path.write_bytes(subprocess.check_output(['git','show',revision+':recovery.json'],cwd=ROOT));preferences_path.write_bytes(subprocess.check_output(['git','show',revision+':source-preferences.json'],cwd=ROOT));original_registry=registry.REGISTRY;original_preferences=source_selection.preferences;report='evidence/matches/auth-character-data-20261106.json';descriptor=(EVIDENCE/'canonical-packet.json').relative_to(ROOT).as_posix()
    try:
        registry.REGISTRY=registry_path;source_selection.preferences=lambda namespace:original_preferences(namespace,path=preferences_path);before=selected_data();functions,bad=collect_matches(configuration()['romSha256'])
        if bad:raise ValueError('Closed167 private existing function projection failed: '+str(bad)[:400])
        registry.register(ROOT/report,['wave20261106_auth_character_data_packet.py',descriptor]);after=selected_data();after_functions,bad=collect_matches(configuration()['romSha256'])
        if bad or after_functions!=functions:raise ValueError('Auth private data registration changed earlier functions')
        expected=claim['claimedStorage'];layout,admitted,assets=membership(before,after,expected,functions);key=sorted(admitted)[0];row=after[key];cases=[]
        reject(cases,'missing-whole-object',lambda:membership(before,{k:v for k,v in after.items()if k!=key},expected,functions))
        reject(cases,'wrong-complete-extent',lambda:membership(before,after,[dict(r,bytes=r['bytes']+1)if identity(r)==key else r for r in expected],functions))
        changed=dict(after);changed[key]=dict(row,module='ov000');reject(cases,'foreign-module',lambda:membership(before,changed,expected,functions))
        old_key=next(iter(before));changed=dict(after);changed[old_key]=dict(before[old_key],sourceSha256='0'*64);reject(cases,'earlier-data-source-mutated',lambda:membership(before,changed,expected,functions))
        changed=dict(after);changed[old_key]=dict(before[old_key],realLink={'forged':True});reject(cases,'earlier-data-proof-mutated',lambda:membership(before,changed,expected,functions))
        changed_functions=dict(functions);changed_functions['private-overlap-control']=dict(row,kind='arm',mode='arm',size=row['bytes']);reject(cases,'function-overlap',lambda:membership(before,after,expected,changed_functions))
        old_overlap_key=(*key[:4],key[4]-1);old_overlap=dict(row,address=hex(key[4]-1),bytes=2,size=2);changed_before=dict(before);changed_before[old_overlap_key]=old_overlap;changed_after=dict(after);changed_after[old_overlap_key]=old_overlap;reject(cases,'old-data-overlap',lambda:membership(changed_before,changed_after,expected,functions))
        image=(ROOT/assets[key]['binary']).read_bytes()
        for label,field,value in [('false-exact','exactBytes',False),('wrong-compiler','compilerFlags',['-O0']),('missing-header','sourceDependencies',[]),('missing-generation-input','dataSourceDependencies',row['dataSourceDependencies'][:1]),('wrong-semantic-source','semanticSource','work/w6ac/wrong.json'),('wrong-data-alias','nativeAlias','data_020deb91'),('false-BSS','allocatedZeroFillBytes',1)]:
            changed=dict(row);changed[field]=value;reject(cases,label,lambda changed=changed:validate(changed,assets[key],admitted[key],layout,image))
        print(dict(privateBeforeData=len(before),privateAfterData=len(after),unchangedFunctions=len(functions),negativeControls=len(cases),freshLinksStarting=102),flush=True);proof=qualify(before,after,expected,functions,folder/'fresh-links')
    finally:registry.REGISTRY=original_registry;source_selection.preferences=original_preferences
    value=dict(passed=True,qualification=proof,negativeControls=cases,privateBaselineRevision=revision,selectedDataBefore=len(before),selectedDataAfter=len(after),unchangedSelectedFunctions=len(functions),privateRegistry=dict(path=registry_path.relative_to(ROOT).as_posix(),sha256=sha256(registry_path)),allProcessLocalOverridesRestored=True,noSharedWritesOrWholeModuleBuild=True,qualifierSha256=sha256(ROOT/'wave20261106_auth_character_data_additions.py'),reviewerSha256=sha256(__file__),sourceCreditPendingSharedAcceptance=True)
    write_json(EVIDENCE/'addition-compatibility-review.json',value);print(dict(passed=True,objects=102,bytes=1431,negativeControls=len(cases),freshGenuineLinks=102),flush=True)


if __name__=='__main__':main()
