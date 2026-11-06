#include "context.h"
int native_main_0208f404(SocketView *socket,void *buffer,int bufferLength,u16 *remotePort,u32 *remoteIp){
ReadCommand *command;
s32 result;
command=native_fn_0208ebd8(native_fn_0208f430,socket,1);
command->buffer10=buffer;command->length14=bufferLength;command->remote18=remotePort;command->peer1C=remoteIp;
result=native_fn_0208eca4(socket,command);
return result;
}
