#include "context.h"
void native_main_02090a3c(ConnectionPrefix *context,u32 ip,u16 port)
{
    s32 index;
    SessionView *candidate;
    u32 biggest;
    u32 enabled=native_fn_02007ff4();
    u32 now=(u32)(native_fn_02007a9c()>>16);
    candidate=native_data_021d1748;biggest=0;
    for(index=0;index<4;index++){
        SessionView *entry=&native_data_021d1748[index];
        if(entry->valid && ip && ip==entry->ip && port && port==entry->port){candidate=entry;break;}
        if(biggest!=(u32)-1){
            if(!entry->valid){biggest=(u32)-1;candidate=entry;}
            else if(now-entry->when>biggest){biggest=now-entry->when;candidate=entry;}
        }
    }
    native_fn_02008e0c(context->session,candidate->session,32);
    native_fn_02008e0c(context->master,candidate->master,48);
    candidate->when=now;candidate->valid=1;candidate->ip=ip;candidate->port=port;
    native_fn_02008008(enabled);
}
