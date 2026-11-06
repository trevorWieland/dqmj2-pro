#include "context.h"
void native_main_0208da30(u32 count,SocketView *socket)
{
    u32 level=native_fn_02007ff4();
    u32 size=socket->word44;
    s32 full=0;
    if(size==socket->capacity3C && count!=0)full=1;
    if(count>=size)socket->word44=0;
    else{
        u8 *buffer=socket->buffer40;
        socket->word44=size-count;
        native_fn_0201b1bc(buffer,buffer+count,size-count);
    }
    native_fn_02008008(level);
    if(socket->state8!=10 && socket->state8!=11 && (socket->word44==0 || full))native_fn_0208cc0c(socket,27);
}
