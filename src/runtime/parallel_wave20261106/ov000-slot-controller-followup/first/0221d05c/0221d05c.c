#include "context.h"
void native_ov000_0221d05c(s32 selector,u32 enabled)
{
    EntryView*entry=native_fn_02049ad0(selector);
    int index=native_fn_0206db90(entry->field5);
    if(!entry->link||!entry->link->resource)return;
    if(enabled)entry->link->resource->flags|=2;
    else{
        ResourceView*resource=entry->link->resource;
        resource->flags&=~2;
        native_fn_02045dc4(1,native_data_ov000_02246227[index].value,resource->field92,resource->field93,resource->field94,resource->field95);
        resource=entry->link->resource;
        if(resource->field96)native_fn_02049ffc(resource);
    }
}
