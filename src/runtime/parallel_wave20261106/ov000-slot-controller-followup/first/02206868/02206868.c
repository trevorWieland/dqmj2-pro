#include "context.h"
void native_ov000_02206868(s32 selector,u32 field4,u32 field5,u8 p0,u8 p1,u8 width,u8 height,s8 tag,u32 enabled,u32*counter)
{
    EntryView*entry=native_fn_02049ad0(selector);
    native_fn_02049be4(entry,1,field4,field5,p0,p1,width,height,*counter,tag,enabled);
    entry->link->resource->flags|=2;
    if(enabled)*counter+=width*height;
}
