#include "context.h"
s32 native_main_0208d820(SocketView *socket)
{
    u32 seed=native_fn_0208d71c();
    u32 retry=0;
    do{
        u32 level;
        socket->word28=seed;
        socket->state8=2;
        socket->tick10=(u32)(native_fn_02007a9c()>>16);
        native_fn_0208cbc4(socket,2,24);
        level=native_fn_02007ff4();
        if(socket->state8==2 && native_data_021cfcf8.address50!=0){socket->kind4=1;native_fn_020068d4(0);}
        native_fn_02008008(level);
        if(socket->state8==4)return 0;
        if(native_data_021cfcf8.address50==0)break;
        ++retry;
    }while(retry<3);
    return 1;
}
