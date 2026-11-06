#include "context.h"
void native_main_02093774(Sha1View *context,u8 *output)
{
    s32 index;
    u32 padding;
    native_fn_02093128(output,&context->high,8);
    index=(context->low>>3)&63;
    padding=index<56?56-index:120-index;
    native_fn_020936f4(context,native_data_020dea18,padding);
    native_fn_020936f4(context,output,8);
    native_fn_02093128(output,context->state,20);
}
