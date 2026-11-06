#include "context.h"
void native_main_0209302c(Md5View *context,const u8 *input,u32 length)
{
    u32 index=(context->low>>3)&63;
    u32 offset,remaining;
    context->low+=length<<3;
    if(context->low<(length<<3))context->high++;
    context->high+=length>>29;
    remaining=64-index;
    if(length>=remaining){
        native_fn_02008e0c(input,context->buffer+index,remaining);
        index=0;
        native_fn_02092cb8(context,context->buffer);
        for(offset=remaining;offset+63<length;offset+=64)native_fn_02092cb8(context,input+offset);
    }else offset=0;
    native_fn_02008e0c(input+offset,context->buffer+index,length-offset);
}
