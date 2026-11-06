#include "context.h"

u32 native_main_020c9c58(NativeInput* arg0,u32 arg1,u32 arg2) {
    u32 var_r4;
    u8* temp_r4;
    u8* temp_r5;

    temp_r5 = (u8*)native_fn_02062a10(arg1);
    temp_r4 = (u8*)native_fn_02062a10(arg1);
    native_fn_020c9984(1U,(u32)arg0->field0010,0xcU,1,5U,0x19U,8U,1,0);
    native_fn_020c9984(0xdU,(u32)arg0->field0010,1U,2,6U,0x17U,2U,0,1);
    native_fn_020c9a3c(0xdU,9U,1U,6U,0x10U);
    native_fn_02072f48((u32)((NativeRecord*)temp_r4)->field0018);
    native_fn_020c9984(0xeU,(u32)arg0->field0010,7U,2,8U,0x17U,2U,0,1);
    native_fn_020c9a3c(0xeU,9U,1U,0x15U,0x10U);
    if(((native_fn_02062aa0() == 1) && (((NativeRecord*)temp_r5)->field0014 == ((NativeRecord*)native_fn_02062a50(0U))->field0014)) || (native_fn_020629e0() == 1)) {
        var_r4 = 3;
    } else {
        var_r4 = 1;
    }
    native_fn_020c9984(0xfU,(u32)arg0->field0010,7U,2,0xaU,0x17U,2U,0,1);
    native_fn_020c9a3c(0xfU,9U,1U,7U,0x10U);
    native_fn_020c9c10(2U,var_r4);
    return native_fn_020c9a84(arg0,3U,3U,0xdU,5U,7U,arg2);
}
