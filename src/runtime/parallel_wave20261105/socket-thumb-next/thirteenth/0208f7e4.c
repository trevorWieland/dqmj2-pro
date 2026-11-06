#include "context.h"
int native_main_0208f7e4(SocketView *socket,const u8 *buffer,s32 length,u16 remotePort,u32 peer,s32 flagBlock){
SendView *send=socket->send68;
s32 sendLength,writeIn,writeLength,minimum,copied=0;
int result;
sendLength=(s32)send->executor10C->cps0.sendSize48;
if(udp(socket)){sendLength-=42;if(length>sendLength){return -35;}minimum=length;}
else{sendLength-=54;minimum=length>sendLength?sendLength:length;}
while(length>0){writeLength=native_fn_0208f898(socket,length,minimum,&writeIn,flagBlock);if(writeLength>0){result=native_fn_0208f91c(socket,buffer,writeLength,writeIn,remotePort,peer,flagBlock);if(result<=0){return -6;}buffer+=writeLength;length-=writeLength;copied+=writeLength;}
if(!(flagBlock&1)){if(writeLength<=0){return -6;}break;}}
return (int)copied;
}
