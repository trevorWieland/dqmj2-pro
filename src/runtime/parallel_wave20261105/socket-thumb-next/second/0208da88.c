#include "context.h"
void native_main_0208da88(u32 count)
{
    SocketView *socket=native_data_020e33e4.thread4->socketA4;
    if(socket){
        if(socket->mode9)native_fn_020928f8(count,socket);
        else native_fn_0208da30(count,socket);
    }
}
