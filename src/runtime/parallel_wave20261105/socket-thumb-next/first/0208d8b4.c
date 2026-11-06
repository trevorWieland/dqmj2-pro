#include "context.h"
void native_main_0208d8b4(SocketView *socket)
{
    u8 state;
    native_fn_020069f8();
    state=socket->state8;
    if(state==3 || state==4){
        native_fn_0208cc18(socket,25);
        socket->state8=7;
    }else if(state!=0)native_fn_0208cc0c(socket,26);
}
