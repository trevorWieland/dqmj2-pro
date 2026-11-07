#include "context.h"
u32 native_ov006_021e749c(s32 selector,s32 dx,s32 dy,s32 width,s32 height) {
    EntryRecord *entry;
    ResourceView *resource;
    const Spec3 *spec;
    s32 reset;
    entry=(EntryRecord*)native_fn_02049ad0((s8)selector);
    if (entry) {
        if (entry->prefix.link && (resource=(ResourceView*)entry->prefix.link->resource)) {
            spec=&native_data_ov006_02207e1c[native_data_ov006_02219160[selector]];
            if(dx==0 && dy==0) {
                if(width<0 && height<0)reset=1;
                else goto explicit_extent;
            } else {
explicit_extent:
                reset=0;
            }
            if(width<0)width=resource->width;
            if(height<0)height=resource->height;
            if(spec->mode!=5)native_fn_02045dc4(spec->font,spec->mode,(u8)((u32)resource->x+(u32)dx),(u8)((u32)resource->y+(u32)dy),(u8)width,(u8)height);
            native_fn_02045dc4(spec->font,resource->layer,(u8)((u32)resource->x+(u32)dx),(u8)((u32)resource->y+(u32)dy),(u8)width,(u8)height);
            if(reset)native_fn_02049ffc(resource);
            else native_fn_0204a010(resource,(s32)((u32)dx<<3),(s32)((u32)dy<<3),(s32)((u32)width<<3),(s32)((u32)height<<3));
            native_fn_020850a0(resource);
        }
        return 1;
    }
    return 0;
}
