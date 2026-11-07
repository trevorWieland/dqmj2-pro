#include "context.h"
void native_ov000_02207acc(SelectionView*selection,s32 value)
{
    if(native_data_ov000_022382c8.words[70]){
        EntryView*entry=native_fn_02049ad0((s8)(selection->first-selection->base+value));
        if(entry->link){
            Pair16 pair;
            pair.field0=entry->link->resource->field28*8;
            pair.field2=entry->link->resource->field29*8;
            native_fn_0204b53c(native_data_ov000_022382c8.words[70],&pair);
            native_fn_ov000_02207b7c(entry->link->resource->field94);
        }
        native_fn_0205f9e4(native_data_ov000_022382c8.words[70]);
    }
    native_data_02101ae8.fieldC84=1;
}
