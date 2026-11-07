#include "context.h"
u32 native_ov006_021e7608(s32 selector) {
    EntryRecord *entry;
    if (native_fn_ov006_021e75ec(selector)) {
        entry=(EntryRecord*)native_fn_02049ad0((s8)selector);
        if(entry && entry->prefix.link) {
            if(entry->prefix.link->resource)native_fn_0205ff4c(entry->prefix.link);
            entry->prefix.link=0;
        }
        entry->prefix.field4=-1;
        entry->prefix.field5=-1;
        entry->prefix.field6=-1;
        entry->prefix.gap7=0;
        entry->extra8=0;
        return 1;
    }
    return 0;
}
