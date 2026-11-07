#include "item_display.h"
void native_main_0207483c(s32 index)
{
    Point point={0,0};
    s16 selected=(s16)native_data_021c5df8[index];
    u32 value=native_fn_02063144(selected);
    point.x=16;
    native_fn_0204a448(1,&point,1,selected,0,1);
    point.x=184;
    native_fn_0204a154(1,&point,1,value,4,0);
}
