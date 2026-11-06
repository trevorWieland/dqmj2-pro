#include "context.h"
void *native_main_0208d9a0(u32 *output,SocketView *socket)
{
    u32 size;
    if(socket->word44==0 && socket->state8==4){
        u32 level=native_fn_02007ff4();
        while(socket->word44==0 && socket->state8==4){socket->kind4=2;native_fn_020068d4(0);}
        native_fn_02008008(level);
    }else native_fn_020069f8();
    size=socket->word44;
    *output=size;
    if(size)return socket->buffer40;
    return 0;
}
