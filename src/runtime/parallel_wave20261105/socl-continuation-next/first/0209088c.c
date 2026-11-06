#include "context.h"
s32 native_main_0209088c(s32 handle,SslConnection *connection)
{
    SocketPrefix *socket=(SocketPrefix *)handle;
    if(native_fn_02090294(socket))return -28;
    if(!socket_tcp(socket))return -28;
    if(!socket_created(socket))return -39;
    if(socket_connecting(socket))return -28;
    return native_fn_020908f0(socket,connection);
}
