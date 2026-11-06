#include "context.h"
u32 native_ov000_022198ec(void) {
    u32 value;
    NativeFlagObject *object;
    value=native_data_ov000_02245f2c.field00;
    if(value!=127) {
        value=native_data_ov000_02245f2c.field1c;
        if(value!=0) {
            value=native_fn_0205f98c((s32)value,0);
            object=(NativeFlagObject*)value;
            if(native_data_ov000_02245e54.opaque00[1]!=0)object->field7c|=2;
            else object->field7c&=~2U;
        }
    }
    return value;
}
