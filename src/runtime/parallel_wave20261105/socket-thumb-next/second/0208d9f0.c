#include "context.h"
void *native_main_0208d9f0(u32 *output)
{
    SocketView *socket=native_data_020e33e4.thread4->socketA4;
    if(socket){
        if(socket->state8==10 || socket->state8==11)return native_fn_0208d968(output,socket);
        if(socket->mode9)return native_fn_02092854(output,socket);
        return native_fn_0208d9a0(output,socket);
    }
    *output=0;
    return 0;
}
