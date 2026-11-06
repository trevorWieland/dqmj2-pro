#include "context.h"
u8 *native_main_02092854(u32 *count,SocketView *socket)
{
    ConnectionView *context=socket->ssl;
    if(context->record && !context->record_hold){
        if(native_fn_02091f54(context->record+context->record_offset,context->record_length-context->record_offset,socket)){
            native_data_021cfd38(context->record);context->record=0;*count=0;return 0;
        }
        native_fn_02091fbc(context,context->record);
        if(!context->record_hold)context->record=0;
    }
    while(!context->record){
        if(native_fn_02092174(socket)==9){*count=0;return 0;}
    }
    *count=context->record_length-context->record_offset;
    return context->record+context->record_offset;
}
