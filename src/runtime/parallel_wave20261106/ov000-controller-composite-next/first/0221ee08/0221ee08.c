#include "context.h"
u32 native_ov000_0221ee08(s32 selector0,s32 selector1,u32 field2,u32 field3,u8 field4,s8 field5)
{
    u32 flags=native_fn_ov000_0221e85c(field2);
    EntryView*entry=native_fn_02049ad0(selector0);
    ResourceView*resource=entry->link->resource;
    Point16 point;
    u16 buffer[32];
    buffer[1]=0;
    point.x=16;
    point.y=0;
    if(flags&1){
        buffer[0]=native_fn_02087554(0);
        native_fn_0204a808(selector0,&point,1,buffer,0);
    }
    point.x+=8;
    if(flags&2){
        buffer[0]=native_fn_02087554(1);
        native_fn_0204a808(selector0,&point,1,buffer,0);
    }
    native_fn_02046af4(native_data_021c9698,native_fn_0205dc70(8,0,field2),field4,24,buffer,255);
    native_fn_02049f4c(entry);
    native_fn_02087a48(resource,0,32,0,field5,buffer);
    native_fn_02086b14(resource,0);
    entry=native_fn_02049ad0(selector1);
    resource=entry->link->resource;
    native_fn_020877bc(field3,buffer,4,3);
    native_fn_02049f4c(entry);
    native_fn_02087a48(resource,0,48,0,field5,buffer);
    return native_fn_02086b14(resource,0);
}
