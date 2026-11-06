#include "context.h"
u32 native_main_02072de8(ObjectPrefix *object,s32 option)
{
    Point point;
    point.x=native_data_021c5a13[object->index].value*8;
    point.y=native_data_021c5a14[object->index].value*8;
    native_fn_0204b53c((u8 *)object+0x50,&point);
    native_fn_0204b5b0((u8 *)object+0x50,64);
    native_fn_0204b380((u8 *)object+8,0);
    if(option!=0)native_fn_0204b61c((u8 *)object+0x50,0);
    else native_fn_0204b61c((u8 *)object+0x50,1);
    return native_fn_0205f9e4((u8 *)object+0x50);
}
