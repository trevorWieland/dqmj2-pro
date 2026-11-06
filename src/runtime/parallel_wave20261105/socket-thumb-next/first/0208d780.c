#include "context.h"
void native_main_0208d780(u32 local,u32 remote,u32 address)
{
    SocketView *socket=native_data_020e33e4.thread4->socketA4;
    if(socket){
        if(address==0x7f000001)address=native_data_021cfcf8.address50;
        socket->remote1A=remote;
        socket->remote18=socket->remote1A;
        socket->address20=address;
        socket->address1C=address;
        if(local==0)socket->portA=native_fn_0208d6b4();
        else socket->portA=local;
    }
}
