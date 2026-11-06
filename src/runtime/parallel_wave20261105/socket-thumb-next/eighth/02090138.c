#include "context.h"
int native_main_02090138(int handle)
{
    SocketView *socket=(SocketView *)handle;
    int result=0;
    u32 level;
    if(native_fn_02090294(socket))result|=0x80;
    else{
        if(state(socket,0x40))result|=0x20;
        if(udp(socket) || state(socket,4)){
            level=native_fn_02007ff4();
            if(native_fn_020901e4(socket)>0)result|=1;
            if(native_fn_0208f900(socket)>0)result|=8;
            native_fn_02008008(level);
        }
        if(tcp(socket)){
            if(state(socket,4) && socket->cpsState8!=4 && !(result&1))socket->state70&=~6;
            if(!state(socket,2) && !state(socket,4))result|=0x40;
        }
    }
    return result;
}
