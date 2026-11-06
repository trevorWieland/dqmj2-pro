#include "context.h"
int native_main_0203d494(u32 mode)
{
    int result=1;
    if(mode!=native_data_020f6048.field4) {
        if(native_fn_0203d3ec(mode))native_data_020f6048.field4=mode;
        else result=0;
    }
    return result;
}
