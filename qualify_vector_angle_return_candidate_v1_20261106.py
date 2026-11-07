from project import ROOT,read_json,write_json,sha256
import match_runtime as C


def main():
    source_name='src/runtime/runtime06/native_main_0202818c.c'
    old=ROOT/source_name;old_hash='97e70d014755234fb3a9a895a1163a9561c6e639ff933841d75e9dcbce99763e'
    assert sha256(old)==old_hash
    row=next(r for r in read_json(ROOT/'evidence/matches/main-runtime06.json')['matches']if int(r['address'],0)==0x0202818c)
    assert row['sourceSha256']==old_hash and row['bytes']==44 and row['exactAfterDeclaredRelocation']
    declarations={'src/math/20261031_atan2/division.c':'cd8cf51d95b362e9cd56295272495ef96064c855d3d954e695e5dbb0723e69a4','src/math/20261031_atan2/native_main_020028d8.c':'9d2507ae43cde98791a955f037ab670e6edbcf917a7505b4c3776f5d251c63f6'}
    assert all(sha256(ROOT/name)==digest for name,digest in declarations.items())
    text=old.read_text(encoding='utf-8')
    for original,replacement in [('extern u32 native_fn_0200235c();','extern u32 native_fn_0200235c(u32 numerator, s32 denominator);'),('extern u32 native_fn_020028d8();','extern u32 native_fn_020028d8(s32 y, s32 x);'),('void native_main_0202818c(void *arg0, void *arg1)','u32 native_main_0202818c(void *arg0, void *arg1)'),('    native_fn_0200235c(','    return native_fn_0200235c(')]:
        assert text.count(original)==1;text=text.replace(original,replacement)
    for offset in [0,8]:
        original='M2C_FIELD(arg1, s32 *, '+str(offset)+') - M2C_FIELD(arg0, s32 *, '+str(offset)+')'
        replacement='(s32)((u32)M2C_FIELD(arg1, s32 *, '+str(offset)+') - (u32)M2C_FIELD(arg0, s32 *, '+str(offset)+'))'
        assert text.count(original)==1;text=text.replace(original,replacement)
    work=ROOT/'work/vector-angle-return-candidate-20261106';work.mkdir(exist_ok=True)
    source=work/'native_main_0202818c.c';source.write_text(text,encoding='utf-8');C.WORK=work/'compile'
    records,compiled=C.compare(source,'main','2','off');assert len(records)==len(compiled)==1
    candidate=records[0]
    assert candidate['compilerFlags']==row['compilerFlags']and candidate['compilerSha256']==row['compilerSha256']
    assert candidate['bytes']==candidate['compiledBytes']==candidate['matchingBytes']==44 and candidate['exactAfterDeclaredRelocation']
    assert candidate['relocations']==row['relocations']and candidate['outputSha256']==candidate['targetSha256']==row['targetSha256']
    assert sha256(old)==old_hash
    write_json(ROOT/'evidence/verification/vector-angle-return-candidate-v1-20261106.json',dict(passed=True,sourceCredit=0,migrationPublished=False,originalSourceUnchanged=True,originalSource=source_name,originalSourceSha256=old_hash,candidate=candidate,actualReturnContract='forwarded raw32bit result; signed interpretation belongs to callers',strictPrototypesPinnedFromAcceptedDefinitions=declarations,coordinateSubtractionExplicitModulo32=True,compilerFlagsAndRelocationsUnchanged=True,nativeBytesUnchanged=True,generatorSha256=sha256(__file__),limits=['Private compiler candidate only; no accepted registry or source edit','Native caller/forwarding evidence and genuine link qualification remain required before an interface migration','Unsigned-to-signed interpretation retains the measured target two-complement convention; no full native Windows claim']))
    print(dict(passed=True,exactBytes=44,sourceCredit=0,migrationPublished=False))


if __name__=='__main__':main()
