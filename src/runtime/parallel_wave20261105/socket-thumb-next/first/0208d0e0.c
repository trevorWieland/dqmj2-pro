#include "context.h"
void native_main_0208d0e0(u32 first,u32 second,u32 third)
{
    SocketView *socket=native_fn_0208cb1c(first,second);
    if(socket){
        switch(socket->state8){
        case 7:
            ++socket->sequence24;
            native_fn_0208cc0c(socket,0);
            socket->state8=9;
            break;
        case 8:
            ++socket->sequence24;
            native_fn_0208cc0c(socket,0);
            socket->state8=0;
            if(socket->kind4==2){socket->kind4=0;native_fn_0200698c(socket->owner0);}
            break;
        case 4:
            ++socket->sequence24;
            native_fn_0208cc18(socket,0);
            socket->state8=6;
            break;
        default:
            native_fn_0208cc24(first,second,third,0);
            break;
        }
    }
}
