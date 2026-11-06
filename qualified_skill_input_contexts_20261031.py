import re
from project import ROOT,sha256,write_json
SOURCE='src/mechanics_save/record_update.c'
SOURCE_SHA='fa7fef97fe89b83cc446fc45bef3d1a22a98aff1c1adb5a1eee7b98349ec800f'
MAIN_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
SPAN_SHA='1d645c440545a90b05400d617e2c4e29e822c25a30118d45acb0ec0d769305df'
CASE_DIGEST='f9dfaac43ea4d3ec8ea309426372283337fc240209d1ecea27de87f4439dcd6b'
TYPE='typedef struct { unsigned char skill; unsigned char allocated; } NativeSavedSkillInput2_20261031;'


def catalogue():
    assert sha256(ROOT/SOURCE)==SOURCE_SHA
    arm=(ROOT/'extract/arm9/arm9.bin').read_bytes()
    import hashlib
    assert hashlib.sha256(arm).hexdigest()==MAIN_SHA and hashlib.sha256(arm[0x62E44:0x62ECC]).hexdigest()==SPAN_SHA
    return [dict(module='main',processor='arm9',mode='arm',address='0x02062e44',bytes=136,alias='func_02062e44',
        source=SOURCE,sourceSha256=SOURCE_SHA,nativeSpanSha256=SPAN_SHA,returnType='int',
        parameterTypes='unsigned int, int, const NativeSavedSkillInput2_20261031 *',sourceTypeDeclaration=TYPE,
        contextPrototype='extern int func_02062e44(unsigned int, int, const NativeSavedSkillInput2_20261031 *);',
        inputObject=dict(argument=2,bytes=2,alignment=1,fields=[dict(offset=0,type='u8',name='skill'),dict(offset=1,type='u8',name='allocated')],
            whenRead='record resolution succeeds and input!=NULL',nativeSlotCheck=False,supportedSourceSlots=[0,1,2,3,4]),
        proof=dict(report='evidence/verification/save-core-skill-input-kernel-20261031.json',nativeCaseDigest=CASE_DIGEST,
            contexts=7970,actualReturns=15940,providedLowerKinds=3,usedAsGeneratedInput=False),
        callerNativeValidationRequired=True,sourceCredit=0)]


def apply(context,module,rows=None,processor='arm9',program=None):
    if processor!='arm9' or program not in (None,'') or not (module in ('main','itcm','dtcm') or re.fullmatch(r'ov\d{3}',module)):
        raise ValueError('Skill-input contract belongs to the primary ARM9 program')
    expected=catalogue()[0]
    if 'NativeSavedSkillInput2_20261031' in context and TYPE not in context:
        raise ValueError('Skill-input type declaration collision')
    changed=[]
    for row in [expected] if rows is None else rows:
        assert all(row.get(key)==value for key,value in expected.items()),'QualifiedSkillInputContractMismatch'
        pattern=r'^extern\s+[^;\n]*\b'+re.escape(row['alias'])+r'\s*\([^;\n]*\);'
        context,count=re.subn(pattern,row['contextPrototype'],context,flags=re.M)
        if count:
            if TYPE not in context:context=TYPE+'\n'+context
            changed.append(dict(alias=row['alias'],prototype=row['contextPrototype'],inputObjectBytes=2,
                sourceTypeDeclaration=TYPE,sourceSha256=SOURCE_SHA,nativeSpanSha256=SPAN_SHA,proofCaseDigest=CASE_DIGEST))
    return context,changed


def main():
    report=dict(schemaVersion=1,contracts=catalogue(),sourceCredit=0,generatorSha256=sha256(ROOT/'qualified_skill_input_contexts_20261031.py'),
        limitations=['Only new primary-ARM9 caller hypotheses; no accepted source/context changes',
            'The minimum two-byte input extent is conditional on record resolution and nonnull input;no general aggregate/global extent is inferred',
            'Lower UID/kind/observer boundaries are supplied in the qualifying proof;actual lower semantics and caller reachability remain separate',
            'Every caller still requires independent source/native ABI,field-width,bounds,genuine-link and returning-effect validation'])
    write_json(ROOT/'evidence/verification/qualified-skill-input-contexts-20261031.json',report)
    print(dict(contracts=len(report['contracts']),sourceCredit=0))


if __name__=='__main__':main()
