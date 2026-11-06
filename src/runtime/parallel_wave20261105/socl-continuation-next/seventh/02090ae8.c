#include "context.h"
void native_main_02090ae8(ConnectionPrefix *context)
{
    s32 index;
    u32 enabled=native_fn_02007ff4();
    for(index=0;index<4;index++){
        SessionView *entry=&native_data_021d1748[index];
        if(entry->valid && !native_fn_0201b248(entry->session,context->session,32)){
            entry->valid=0;
            break;
        }
    }
    native_fn_02008008(enabled);
}
