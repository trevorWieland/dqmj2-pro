#include "context.h"
s32 native_main_020901e4(SocketView *socket)
{
    RecvView *receive=socket->recv64;
    s32 size=0;
    if(receive){
        if(udp(socket)){
            UdpView *out=receive->out104;
            size=out?out->size4:0;
        }else if(tcp(socket))size=(s32)socket->received44-(s32)receive->consumedF8;
    }
    return size;
}
