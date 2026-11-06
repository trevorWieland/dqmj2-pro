#include "context.h"
int native_main_0208eff0(int handle,u16 remotePort,u32 remoteIP)
{
    SocketView *socket=(SocketView *)handle;
    int result;
    if(native_fn_02090294(socket) || state(socket,8))return -28;
    if(!created(socket))return -39;
    if(tcp(socket)){
        if(state(socket,4))return block(socket)?-30:0;
        if(state(socket,2)){
            if(state(socket,0x40))return socket->result6C;
            return native_data_020de7d0;
        }
        socket->remote76=remotePort;
        socket->peer78=remoteIP;
        result=native_fn_0208f0a0(socket);
        return block(socket)?result:-26;
    }
    socket->remote76=remotePort;
    socket->peer78=remoteIP;
    return 0;
}
