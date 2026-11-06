#include "context.h"
u32 native_main_02092778(SocketView *socket)
{
    s32 result;
    ConnectionView *context=socket->ssl;
    native_fn_02092470(socket);
    for(;;){
        result=native_fn_02092174(socket);
        if(result==9)return 1;
        if(result==4 || context->reuse)break;
    }
    if(context->reuse){
        native_fn_020918a4(context);
        if(native_fn_02092754(socket))return 1;
        native_fn_02092380(socket);
    }else{
        native_fn_02092584(socket);
        native_fn_02091864(context);
        if(context->cached)native_fn_02090a3c(context,socket->ip,socket->port);
        native_fn_020918a4(context);
        native_fn_02092380(socket);
        if(native_fn_02092754(socket))return 1;
    }
    context->state=8;
    return 0;
}
