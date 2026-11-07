#include "context.h"
u32 native_ov006_021e6c44(void) {
    s32 index;
    u32 fileSize;
    u32 asset;
    u32 loaded;
    const Spec3 *spec;
    BuildRecord12 *record;
    native_fn_0205fd80(0);
    {s32 clearIndex=0;do{native_data_ov006_02218df8[0][clearIndex]=32;clearIndex++;}while(clearIndex<4);}
    native_fn_02048f1c(2,0);native_fn_02048f2c(0,0);native_fn_02046150(0,0,1);
    native_fn_02045654(0);native_fn_02045654(1);native_fn_02045654(2);native_fn_02045654(3);
    native_fn_02008c58(0,native_fn_02045514(1),32);
    native_fn_02008c58(0,native_fn_02045514(2),32);
    native_fn_02008c58(0,native_fn_02045514(0),32);
    fileSize=native_fn_0202a8e0(native_data_ov006_02207e88);
    asset=native_fn_0203cc2c(native_data_ov006_02207e88,1);
    native_fn_020481b8(asset,0,fileSize);
    native_fn_020481b8((u32)native_data_ov006_02207dbe,0,2);
    native_fn_0202a498(1,asset);native_fn_ov006_022076b4(0);
    asset=native_fn_0203cc2c(native_data_ov006_02207e9c,1);
    native_data_ov006_02218d90.word70=0x3000;
    native_fn_0204540c(2,asset,0,0x3000);native_fn_0202a498(1,asset);
    native_fn_0205ff80(native_data_ov006_0220d334);
    spec=native_data_ov006_02207e4f;record=native_data_ov006_02218fc8;
    index=0;do {
        if(spec->font==0){loaded=native_fn_02065730(record,spec->tag,spec->font,spec->mode,native_data_ov006_02218df8[spec->font][spec->mode]);native_data_ov006_02218df8[spec->font][spec->mode]+=loaded;}
        index++;spec++;record++;
    }while(index<11);
    native_fn_0205ff9c();native_fn_ov006_021e7370(-1);
    native_fn_0204b9d0(1,native_data_ov006_02218df8);
    return native_fn_02048308();
}
