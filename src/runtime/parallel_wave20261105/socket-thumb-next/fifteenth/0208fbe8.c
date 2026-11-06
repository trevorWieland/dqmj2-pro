#include "context.h"
int native_main_0208fbe8(int value){
SocketView *socket=(SocketView *)value;
SendView *send;
CommandView *command;
s32 result;
if(native_fn_02090294(socket)){return -28;}
if(!created(socket)){return -39;}
if(!state(socket,4)||state(socket,8)){return -56;}
socket->state70|=8;send=socket->send68;
if(send&&send->executor10C){command=native_fn_0208ebd8(native_fn_0208fc70,send->executor10C,socket->block72);if(command==0){return -33;}result=native_fn_0208ecb0(send->executor10C,command);}else{result=0;}
return result;
}
