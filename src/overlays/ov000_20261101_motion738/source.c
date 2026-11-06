#include "context.h"
void native_ov000_022199b8(void) {
    NativeVector source,previous;
    NativeRow *row;
    f32 ratio,value;
    s32 scaled;
    row=(NativeRow*)native_fn_ov000_021df3bc((s32)native_fn_ov000_021df1f0());
    ratio=native_fn_02025578(8.0f,native_fn_02025a28(row->field0a));
    native_data_ov000_02245e54.field4c.x=row->field04;
    native_data_ov000_02245e54.field4c.z=row->field06;
    native_data_ov000_02245e54.field4c.x*=4096;
    native_data_ov000_02245e54.field4c.z*=4096;
    native_fn_02041f74((u32)native_fn_ov000_021e07ac(),&source);
    native_data_ov000_02245e54.field4c.x+=native_fn_020259b4(native_fn_02025ab8(native_fn_02025a28(source.x),ratio));
    native_data_ov000_02245e54.field4c.z+=native_fn_020259b4(native_fn_02025ab8(native_fn_02025a28(source.z),ratio));
    if(native_data_ov000_02245e54.field20==0)return;
    scaled=native_data_ov000_02245e54.field10*4096;
    if(native_data_ov000_02245e54.field10>0)value=native_fn_02024e0c(0.5f,native_fn_02025a28(scaled));
    else value=native_fn_02025ca4(native_fn_02025a28(scaled),0.5f);
    native_data_ov000_02245e54.field4c.x-=native_fn_020259b4(value);
    scaled=native_data_ov000_02245e54.field12*4096;
    if(native_data_ov000_02245e54.field12>0)value=native_fn_02024e0c(0.5f,native_fn_02025a28(scaled));
    else value=native_fn_02025ca4(native_fn_02025a28(scaled),0.5f);
    native_data_ov000_02245e54.field4c.z-=native_fn_020259b4(value);
    previous=native_data_ov000_02245ea0;
    native_fn_ov000_02219ce4(&native_data_ov000_02245ea0);
    native_data_ov000_02245e54.field10=(s16)native_fn_020259b4(native_fn_02025ca4(native_fn_02025a28(native_data_ov000_02245e54.field10),native_fn_02025578(native_fn_02025a28(native_data_ov000_02245e54.field4c.x-previous.x),4096.0f)));
    native_data_ov000_02245e54.field12=(s16)native_fn_020259b4(native_fn_02025ca4(native_fn_02025a28(native_data_ov000_02245e54.field12),native_fn_02025578(native_fn_02025a28(native_data_ov000_02245e54.field4c.z-previous.z),4096.0f)));
}
