#include "context.h"
void native_ov000_0220820c(u32 field0,u32 field1,u32 field2,u32 field3)
{
    EntryView*entry=native_fn_02049ad0(8);
    u8 value=field2&~0x80;
    PairSigned16 pair;
    native_fn_020602ec(entry->link,field0,field1,24,field3,1);
    pair.field0=120;
    pair.field2=field3;
    pair.field0+=native_fn_ov000_02206ab8(8,5,1,1,&pair,0);
    pair.field0+=native_fn_ov000_02206a20(8,native_data_ov000_0222f73c,&pair,0);
    if(value<100)native_fn_0204a154(8,&pair,(field2&0x80)?5:1,value,2,0);
}
