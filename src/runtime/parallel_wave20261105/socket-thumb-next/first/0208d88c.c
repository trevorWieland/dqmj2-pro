#include "context.h"
s32 native_main_0208d88c(void)
{
    SocketView *socket=native_data_020e33e4.thread4->socketA4;
    if(socket){
        if(socket->mode9)return native_fn_0209280c(socket);
        return native_fn_0208d820(socket);
    }
    return 1;
}
