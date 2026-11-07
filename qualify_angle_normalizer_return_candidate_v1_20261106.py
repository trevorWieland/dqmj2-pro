from project import ROOT,read_json,write_json,sha256
import match_runtime as C


def main():
    original=ROOT/'src/runtime/runtime06/native_main_02028158.c'
    old_hash='3ff701e865592f0c009c4968a1ee22839c6295dc7d30211c1f166c752542671f'
    assert sha256(original)==old_hash
    row=next(r for r in read_json(ROOT/'evidence/matches/main-runtime06.json')['matches']if int(r['address'],0)==0x02028158)
    assert row['sourceSha256']==old_hash and row['bytes']==52 and row['exactAfterDeclaredRelocation']
    text=original.read_text(encoding='utf-8')
    assert text.count('void native_main_02028158(s32 arg0)')==1 and text.count('return;')==1
    text=text.replace('void native_main_02028158(s32 arg0)','s32 native_main_02028158(s32 arg0)').replace('return;','return var_r0;')
    text=text.rstrip();assert text.endswith('}')
    text=text[:-1]+'    return var_r0;\n}\n'
    work=ROOT/'work/angle-normalizer-return-candidate-20261106';work.mkdir(exist_ok=True)
    source=work/'native_main_02028158.c';source.write_text(text,encoding='utf-8')
    C.WORK=work/'compile'
    records,compiled=C.compare(source,'main','2','off')
    assert len(records)==1 and len(compiled)==1
    candidate=records[0]
    assert candidate['compilerFlags']==row['compilerFlags'] and candidate['compilerSha256']==row['compilerSha256']
    assert candidate['bytes']==candidate['compiledBytes']==candidate['matchingBytes']==52 and candidate['exactAfterDeclaredRelocation']
    assert candidate['relocations']==row['relocations']==[]
    assert candidate['outputSha256']==candidate['targetSha256']==row['targetSha256']
    assert sha256(original)==old_hash
    report=dict(passed=True,sourceCredit=0,migrationPublished=False,originalSourceUnchanged=True,originalSource=original.relative_to(ROOT).as_posix(),originalSourceSha256=old_hash,candidate=candidate,actualReturnContract='signed32 normalized angle on both paths',compilerFlagsUnchanged=True,nativeBytesUnchanged=True,bytes=52,generatorSha256=sha256(__file__),limits=['Private compiler candidate only; accepted definition and registry remain unchanged','Join with measured native/caller ABI proof before any explicit interface migration','This does not establish whole native Windows execution'])
    write_json(ROOT/'evidence/verification/angle-normalizer-return-candidate-v1-20261106.json',report)
    print(dict(passed=True,exactBytes=52,sourceCredit=0,migrationPublished=False))


if __name__=='__main__':main()
