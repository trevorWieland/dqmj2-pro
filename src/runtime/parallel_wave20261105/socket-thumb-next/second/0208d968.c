#include "context.h"
void *native_main_0208d968(u32 *output,SocketView *socket)
{
    u32 level=native_fn_02007ff4();
    u32 size=socket->word44;
    while(size==0){socket->kind4=3;native_fn_020068d4(0);size=socket->word44;}
    native_fn_02008008(level);
    *output=size;
    return socket->buffer40;
}
