#include "context.h"
void native_ov000_021efec4(u8 value,s32 selector)
{
    EntryView*target=native_fn_02049ad0(19);
    EntryView*source=native_fn_02049ad0(selector);
    target->link=source->link;
    value+=2;
    native_fn_ov000_021ef688(18,2,127,22,value,7,2,1,1);
    native_fn_ov000_021ef1cc(1);
    native_fn_ov000_021ef2a8(176,(u8)(value<<3));
}
