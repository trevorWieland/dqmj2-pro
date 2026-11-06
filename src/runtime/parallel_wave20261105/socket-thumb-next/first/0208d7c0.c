#include "context.h"
void native_main_0208d7c0(void)
{
    ThreadView *thread=native_data_020e33e4.thread4;
    SocketView *socket=thread->socketA4;
    if(socket){
        socket->owner0=thread;
        socket->state8=0;
        socket->word44=0;
        socket->word60=0;
        socket->word38=0;
    }
}
