#include "context.h"
u32 native_ov006_021e6ef4(void) {
    s32 index;
    u32 asset;
    u32 loaded;
    u32 layout[2];
    const Spec3 *spec;
    BuildRecord12 *record;
    const Spec3 *secondarySpec;
    BuildRecord12 *secondaryRecord;
    native_fn_020489f0(1);native_fn_0205fd80(1);
    {s32 clearIndex=0;do{*(u32*)((u8*)&native_data_ov006_02218df8+(u32)clearIndex*sizeof(u32)+sizeof(native_data_ov006_02218df8.rows[0]))=32;clearIndex++;}while(clearIndex<4);}
    native_data_ov006_02218d90.word7c=0;
    native_fn_02048f1c(3,1);native_fn_02048f2c(2,1);native_fn_02048f3c(0,1);
    native_fn_02046150(1,0,1);native_fn_02046150(2,2,1);
    native_fn_02045680(0);native_fn_02045680(1);native_fn_02045680(2);native_fn_02045680(3);
    native_fn_0204607c(0);native_fn_0204607c(1);native_fn_0204607c(2);native_fn_0204607c(3);
    native_fn_02008c58(0,native_fn_02045560(3),32);
    native_fn_02008c58(0,native_fn_02045560(2),32);
    native_fn_02008c58(0,native_fn_02045560(0),32);
    asset=native_fn_0203cc2c(native_data_ov006_0220d378,1);native_fn_ov006_021e6e2c(asset);native_fn_ov006_022076b4(1);
    native_fn_0204518c(layout,asset,1);native_fn_02045490(1,layout[0],0,layout[1]);
    native_data_ov006_02218d90.word7c=layout[1];native_fn_0202a498(1,asset);
    native_fn_0205ff80(native_data_ov006_0220d38c);
    spec=native_data_ov006_02207e1c;record=native_data_ov006_02219094;
    index=0;do {
        native_fn_02008d78(record,0,12);
        if(spec->tag==127)goto sentinel_record;
        loaded=native_fn_0205ffcc(record,spec->tag,spec->font,spec->mode,native_data_ov006_02218df8.rows[spec->font][spec->mode]);
        native_data_ov006_02218df8.rows[spec->font][spec->mode]+=loaded;
        goto record_ready;
sentinel_record:
        record->tag8=spec->tag;record->font10=spec->font;record->mode11=spec->mode;
record_ready:
        index++;spec++;record++;
    }while(index<17);
    secondarySpec=native_data_ov006_02207e70;secondaryRecord=native_data_ov006_0221904c;
    index=11;do {
        if(secondarySpec->font==1){loaded=native_fn_02065730(secondaryRecord,secondarySpec->tag,secondarySpec->font,secondarySpec->mode,native_data_ov006_02218df8.rows[secondarySpec->font][secondarySpec->mode]);native_data_ov006_02218df8.rows[secondarySpec->font][secondarySpec->mode]+=loaded;}
        index++;secondarySpec++;secondaryRecord++;
    }while(index<17);
    native_fn_0205ff9c();native_fn_ov006_021e7210((u32)native_data_ov006_0220d3a0,4);
    return native_fn_02048308();
}
