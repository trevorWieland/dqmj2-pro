#include "context.h"
void native_ov000_02208854(SelectionView*selection,s32 value)
{
    if(native_data_ov000_022383e8.words[67]){
        EntryView*entry=native_fn_02049ad0((s8)(selection->first-selection->base+value));
        if(entry->link){
            Pair16 pair;
            pair.field0=entry->link->resource->field28*8;
            pair.field2=entry->link->resource->field29*8;
            native_fn_0204b53c(native_data_ov000_022383e8.words[67],&pair);
            native_fn_ov000_02208918(entry->link->resource->field94);
        }
        native_fn_0205f9e4(native_data_ov000_022383e8.words[67]);
    }
    if(native_data_ov000_022383e8.words[68])native_fn_0205f9e4(native_data_ov000_022383e8.words[68]);
    native_data_02101ae8.fieldC84=1;
}
