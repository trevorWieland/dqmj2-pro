#include "context.h"
void native_main_0209158c(ConnectionView *context,u8 *input)
{
    s32 methods,sessions,challenge,offset;
    u16 method;
    if(!native_fn_02091580(input[0],input[1]))return;
    methods=(input[2]<<8)+input[3];
    method=native_fn_0209154c(input+8,methods/3,3);
    if(!method)return;
    context->method=method;
    sessions=(input[4]<<8)+input[5];challenge=(input[6]<<8)+input[7];
    context->cached=0;
    offset=8+methods+sessions;
    if(challenge>=32)native_fn_02008e0c(input+offset,context->randoms,32);
    else {
        native_fn_02008d78(context->randoms,0,32-challenge);
        native_fn_02008e0c(input+offset,context->randoms+32-challenge,challenge);
    }
    context->state=1;
}
