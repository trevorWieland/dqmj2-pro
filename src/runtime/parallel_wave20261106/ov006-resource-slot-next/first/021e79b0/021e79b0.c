#include "context.h"
u32 native_ov006_021e79b0(u32 mode,u32 flag,u32 value) {
    u32 mask=flag?3:2;
    native_fn_020414c8(63);native_fn_0204157c(0);native_fn_02041538(mode,mask,value);
    native_data_ov006_02218d90.state28=0;native_data_ov006_02218d90.state4c=0;
    return (u32)&native_data_ov006_02218d90;
}
