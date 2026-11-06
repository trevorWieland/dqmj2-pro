#include "context.h"
void native_main_0208d154(u32 first,u32 second)
{
    SocketView *socket=native_fn_0208cb1c(first,second);
    if(socket){
        native_fn_020069f8();
        socket->state8=0;
        if(socket->kind4==1 || socket->kind4==2){
            socket->kind4=0;
            native_fn_0200698c(socket->owner0);
        }
    }
}
