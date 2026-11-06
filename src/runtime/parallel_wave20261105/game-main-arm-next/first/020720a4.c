#include "context.h"
void native_main_020720a4(s32 index,s32 duplicate,u32 first,u32 second)
{
    ContextPrefix *context=native_fn_02061944();
    s32 offset=index*12;
    LayoutRecord *rows=context->rows;
    if(native_fn_020625bc()!=0)native_fn_0207211c(2,first,second);
    else native_fn_0207211c(1,first,second);
    native_fn_02065818((LayoutRecord *)((u8 *)rows+offset),first,second);
    if(duplicate!=0)native_fn_02065818(rows,first,second);
}
