#include "context.h"
u32 native_ov000_021f2d24(s32 selector,u32 field4,u32 field5,u8 p0,u8 p1,u8 width,u8 height,s8 tag,u32 enabled)
{
    EntryView *entry=native_fn_02049ad0(selector);
    if(entry->link)return 0;
    if(!native_fn_02049be4(entry,1,field4,field5,p0,p1,width,height,native_data_ov000_02236dbc.words[1],tag,enabled))return 0;
    entry->link->resource->flags|=2;
    if(enabled)native_data_ov000_02236dbc.words[1]+=width*height;
    return 1;
}
