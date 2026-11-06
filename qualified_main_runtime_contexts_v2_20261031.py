from project import ROOT,sha256,write_json,configuration
from qualified_call_contexts_20261031 import apply

CONTRACTS=[
 ('0200235c','u32','u32, s32','src/math/20261031_atan2/division.c','Raw divider forwarding, two explicit words; positive modeled device contract'),
 ('020023c4','u32','void','src/math/20261031_atan2/division.c','Raw divider result reader, no input parameters'),
 ('020028d8','u32','s32, s32','src/math/20261031_atan2/native_main_020028d8.c','Raw32-bit angle result with explicit signed16 narrowing; bounded native coordinates'),
 ('02022a54','void','void *, s32','src/runtime/20261031_decimal_rounding/native_main_02022a54.c','Explicit buffer/count and no semantic return value'),
 ('020343fc','u32','u8 *, u32, const u8 *','src/runtime/20261031_record_init/native_main_020343fc.c','Ordered full-word and byte initializer, bounded aligned byte buffers'),
 ('02036994','u32','void **, u32','src/runtime/20261031_range_map/native_main_02036994.c','Raw returned address from an allocated inclusive-range chain'),
 ('0203cb8c','u32','u32, u32, u32','src/runtime/20261031_resource_load/native_main_0203cb8c.c','Three raw path/heap/selector words; lower protocols remain supplied'),
]


def catalogue():
    return [{'processor':'arm9','program':'','module':'main','mode':'arm','address':'0x'+address,'alias':'func_'+address,'returnType':returns,'parameterTypes':parameters,'source':source,'sourceSha256':sha256(ROOT/source),'qualification':scope,'contextPrototype':f'extern {returns} func_{address}({parameters});','sourceCredit':0,'callerNativeValidationRequired':True} for address,returns,parameters,source,scope in CONTRACTS]


if __name__=='__main__':
    write_json(ROOT/'evidence/verification/qualified-main-runtime-contexts-v2-20261031.json',{'romSha256':configuration()['romSha256'],'sourceCredit':0,'contracts':catalogue(),'scope':'New host ARM9 drafts only; every caller remains a hypothesis until separate native/ABI/link gates','historicalPrototypesClaimed':False})
