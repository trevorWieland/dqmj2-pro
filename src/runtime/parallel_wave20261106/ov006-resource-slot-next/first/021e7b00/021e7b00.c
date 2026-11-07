#include "context.h"
u32 native_ov006_021e7b00(s32 selector) {
    EntryRecord *entry;
    ResourceView *resource;
    entry=(EntryRecord*)native_fn_02049ad0((s8)selector);
    if(entry && entry->prefix.link) {
        resource=(ResourceView*)entry->prefix.link->resource;
        native_fn_ov006_021e7ab0(native_data_ov006_02219160[selector],resource->x,resource->y,resource->width,resource->height);
        return 1;
    }
    return 0;
}
