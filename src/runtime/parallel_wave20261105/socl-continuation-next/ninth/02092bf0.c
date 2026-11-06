#include "context.h"
void native_main_02092bf0(u32 now)
{
    u32 enabled;
    ThreadView *thread;
    SocketView *socket;
    s32 i;
    enabled=native_fn_02007ff4();
    for(i=0;i<4;i++){
        if(native_data_021d1748[i].valid && (s32)(now-native_data_021d1748[i].when)>957)native_data_021d1748[i].valid=0;
    }
    native_fn_02008008(enabled);
    for(thread=native_data_020e33e4.first;thread;thread=thread->next){
        socket=thread->socket;
        if(socket && socket->thread && socket->secured && socket->type==4 && socket->ssl->state<8 && (s32)(now-socket->when)>239 && socket->state==2){
            socket->type=0;socket->state=0;
            native_fn_0200698c(socket->thread);
        }
    }
}
