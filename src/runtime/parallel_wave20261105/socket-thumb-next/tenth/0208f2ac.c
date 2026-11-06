#include "context.h"
int native_main_0208f2ac(SocketView *socket,void *buffer,int bufferLength,u16 *remotePort,u32 *remoteIp,s32 flagBlock){
int result;
if(socket->mode73==4){result=native_fn_0208f404(socket,buffer,bufferLength,remotePort,remoteIp);return result;}
result=native_fn_0208f2f8(socket,buffer,bufferLength,remotePort,remoteIp);
if(result==-6 && (flagBlock&1)){result=native_fn_0208f404(socket,buffer,bufferLength,remotePort,remoteIp);}
return result;
}
