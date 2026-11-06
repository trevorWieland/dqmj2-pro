#include "context.h"
int native_main_0205f4bc(u32 index,u32 first,u32 second)
{
    Record8 *record=&native_data_021b8af0[index];
    int value=record->field4;
    if(value>=0) {
        native_fn_0203a050(record,first,second);
        return native_fn_0205ed58(0);
    }
    return native_fn_0205ed58(8);
}
