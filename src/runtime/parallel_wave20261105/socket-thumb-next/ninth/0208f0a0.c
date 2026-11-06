#include "context.h"
int native_main_0208f0a0(SocketView *socket)
{
    BindCommand *command;
    s32 result;
    command=native_fn_0208ebd8(native_fn_0208f0e8,socket,socket->block72);
    if(!command)return -33;
    command->local10=socket->local74;
    command->remote12=socket->remote76;
    command->peer14=socket->peer78;
    socket->state70|=2;
    result=native_fn_0208eca4(socket,command);
    return result;
}
