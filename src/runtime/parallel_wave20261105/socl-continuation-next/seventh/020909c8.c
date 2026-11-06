#include "context.h"
void native_main_020909c8(ConnectionPrefix *context,u32 ip,u16 port)
{
    s32 index;
    u32 enabled=native_fn_02007ff4();
    context->cached=0;
    for(index=0;index<4;index++){
        SessionView *entry=&native_data_021d1748[index];
        if(entry->valid && entry->ip==ip && entry->port==port){
            native_fn_02008e0c(entry->session,context->session,32);
            native_fn_02008e0c(entry->master,context->master,48);
            entry->when=(u32)(native_fn_02007a9c()>>16);
            context->cached=1;
            break;
        }
    }
    native_fn_02008008(enabled);
}
