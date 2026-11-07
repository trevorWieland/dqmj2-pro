#include "context.h"
void native_main_0207211c(u32 index,u32 first,u32 second)
{
    ContextPrefix *context=native_fn_02061944();
    u32 offset=index*12;
    DetailPrefix *detail=native_data_021c4f60.detail;
    LayoutRecord *rows=context->rows;
    switch(index){
    case 1:case 2:
        native_fn_02065818((LayoutRecord *)((u8 *)rows+offset),first,second);
        break;
    case 3:case 4:case 5:case 6:case 7:case 8:case 9:
        native_fn_020720a4(index,detail->flags&(1U<<(index-3)),first,second);
        break;
    }
}
