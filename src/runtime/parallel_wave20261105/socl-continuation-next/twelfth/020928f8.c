#include "context.h"
void native_main_020928f8(u32 count,SocketView *socket)
{
    ConnectionView *context=socket->ssl;
    if(count>=context->record_length-context->record_offset){
        if(context->record)native_data_021cfd38(context->record);
        context->record=0;
    }else context->record_offset+=count;
}
