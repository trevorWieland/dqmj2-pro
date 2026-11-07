#include "resource_display.h"
void native_main_020724f4(s32 index,u32 selection)
{
    const u16 *resource=native_data_021c9698;
    void *target=(*native_fn_02061dcc(index))->render;
    Point point={0,0};
    native_fn_02049ffc(target);
    u32 value=native_data_021c4f78[selection];
    if(value!=0)native_fn_0204abd4(index,resource,&point,1,value,1);
}
