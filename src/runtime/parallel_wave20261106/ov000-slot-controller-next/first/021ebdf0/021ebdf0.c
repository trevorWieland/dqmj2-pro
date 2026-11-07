#include "context.h"
StateView * native_ov000_021ebdf0(s32 selector,u32 field4,u32 field5,u8 p0,u8 p1,u8 width,u8 height,s8 tag,u32 enabled)
{
    EntryView *entry=native_fn_02049ad0(selector);
    native_fn_02049be4(entry,1,field4,field5,p0,p1,width,height,native_data_ov000_02236a98.words[2],tag,enabled);
    entry->link->resource->flags|=2;
    native_data_ov000_02236a98.words[2]+=width*height;
    return &native_data_ov000_02236a98;
}
