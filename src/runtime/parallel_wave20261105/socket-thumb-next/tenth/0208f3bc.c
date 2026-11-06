#include "context.h"
u8 *native_main_0208f3bc(SocketView *socket,s32 *bufferLength,u16 *localPort,u16 *remotePort,u32 *remoteIp){
RecvView *receive;
CpsView *cps;
s32 consumed,length;
receive=socket->recv64;
cps=receive->specificC4;
consumed=receive->consumedF8;
length=(s32)cps->length44-consumed;
if(length>=0){*localPort=cps->localA;*remotePort=cps->remote18;*remoteIp=cps->peer1C;*bufferLength=length;if(length==0 && cps->state8!=4){return 0;}}
else{*bufferLength=-1;return 0;}
return cps->buffer40+consumed;
}
