#include "context.h"
void native_main_020930ac(Md5View *context,u8 *output)
{
    s32 index;
    u32 padding;
    native_fn_02092c98(output,&context->low,8);
    index=(context->low>>3)&63;
    padding=index<56?56-index:120-index;
    native_fn_0209302c(context,native_data_020de8d8,padding);
    native_fn_0209302c(context,output,8);
    native_fn_02092c98(output,context->state,16);
}
