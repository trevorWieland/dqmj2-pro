#include "context.h"
u32 native_ov006_021e76f0(s32 selector,u32 value) {
    EntryRecord *entry;
    ResourceView *resource;
    s16 x;
    entry=(EntryRecord*)native_fn_02049ad0((s8)selector);
    if(entry && entry->prefix.link && (resource=(ResourceView*)entry->prefix.link->resource)) {
        native_fn_0204a0b0(resource,value);
        x=entry->prefix.field5==127?0:8;
        native_fn_02085270(resource->payloadPrefix,x,0);
        return 1;
    }
    return 0;
}
