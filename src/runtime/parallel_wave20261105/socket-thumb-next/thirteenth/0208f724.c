#include "context.h"
int native_main_0208f724(int value,const void *buffer,int length,u16 remotePort,u32 peer,int flags){
SocketView *socket=(SocketView *)value;
SendView *send;
int flagBlock,result;
if(native_fn_02090294(socket)){return -28;}
if(!created(socket)){return -39;}
if(tcp(socket) && (!state(socket,4)||state(socket,8))){return -56;}
send=socket->send68;
if((flags&4)||socket->block72==0){if(!native_fn_020071a8(send->mutexE0)){return -6;}flagBlock=0;}
else{native_fn_0200708c(send->mutexE0);flagBlock=1;}
result=native_fn_0208f7e4(socket,buffer,length,remotePort,peer,flagBlock);
native_fn_02007110(send->mutexE0);
return result;
}
