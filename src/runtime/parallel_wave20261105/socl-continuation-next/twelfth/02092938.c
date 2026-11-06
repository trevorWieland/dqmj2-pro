#include "context.h"
void native_main_02092938(SocketView *socket)
{
    ConnectionView *context=socket->ssl;
    u32 amount;
    u8 *input;
    s32 complete;
    if(!context->record){
        if(socket->available<5)return;
        input=native_fn_0208d9a0(&amount,socket);
        amount=(input[3]<<8)+input[4]+5;
        if(amount>0x4805){context->state=9;return;}
        context->record=native_data_021cfd0c(amount);
        if(!context->record){context->state=9;return;}
        context->record_length=amount;context->record_offset=0;context->record_hold=0;
    }else if(!socket->available)return;
    input=native_fn_0208d9a0(&amount,socket);
    if(amount>=context->record_length-context->record_offset){amount=context->record_length-context->record_offset;complete=1;}
    else complete=0;
    native_fn_02008e0c(input,context->record+context->record_offset,amount);
    native_fn_0208da30(amount,socket);
    if(complete){
        native_fn_02091fbc(context,context->record);
        if(!context->record_hold)context->record=0;
    }else context->record_offset+=amount;
}
