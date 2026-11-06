#include "context.h"
int native_main_0208f0e8(void *argument)
{
    BindCommand *command=(BindCommand *)argument;
    SocketView *socket=command->socket4;
    RecvView *receive;
    u32 result=0;
    receive=socket->recv64;
    native_fn_0200708c(receive->mutexE0);
    native_fn_0208d780(command->local10,command->remote12,command->peer14);
    receive->consumedF8=0;
    if(command->modeC==0 || command->modeC==4)result=native_fn_0208d88c();
    native_fn_02007110(receive->mutexE0);
    if(result){socket->state70|=0x40;return -76;}
    socket->state70|=4;
    return 0;
}
