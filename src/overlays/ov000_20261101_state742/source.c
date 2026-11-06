#include "context.h"
void native_ov000_02219ba4(void) {
    NativeVector target;
    s32 difference_x,difference_z;
    target=native_data_ov000_02245e54.field4c;
    native_fn_ov000_02219ce4(&target);
    if(native_data_ov000_02245e54.field20!=0) {
        difference_x=target.x-native_data_ov000_02245e54.field40.x;
        difference_z=target.z-native_data_ov000_02245e54.field40.z;
    } else if(native_data_ov000_02245e54.field28!=0) {
        difference_x=(target.x-native_data_ov000_02245e54.field40.x)>>3;
        difference_z=(target.z-native_data_ov000_02245e54.field40.z)>>3;
    } else {
        difference_x=(target.x-native_data_ov000_02245e54.field40.x)>>4;
        difference_z=(target.z-native_data_ov000_02245e54.field40.z)>>4;
    }
    native_data_ov000_02245e54.field40.x+=difference_x;
    native_data_ov000_02245e54.field40.z+=difference_z;
}
