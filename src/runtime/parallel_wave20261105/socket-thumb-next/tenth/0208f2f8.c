#include "context.h"
int native_main_0208f2f8(SocketView *socket,void *buffer,int bufferLength,u16 *remotePort,u32 *remoteIp){
u32 enable;
RecvView *receive;
u8 *cpsBuffer;
s32 cpsLength,copyLength,consumeLength;
u16 localPort,peerPort;
u32 peerIp;
int result=0;
enable=native_fn_02007ff4();
cpsBuffer=native_fn_0208f3bc(socket,&cpsLength,&localPort,&peerPort,&peerIp);
if(cpsBuffer){if(cpsLength==0){result=-6;}else{copyLength=bufferLength>cpsLength?cpsLength:bufferLength;consumeLength=tcp(socket)?copyLength:cpsLength;native_fn_02008e0c(cpsBuffer,buffer,(u32)copyLength);receive=socket->recv64;if(!receive->noConsumeFE){receive->consumedF8+=consumeLength;}result=(int)consumeLength;}}
else{if(cpsLength==0){result=0;}else{result=-28;}socket->state70&=~6;}
if(result>=0){if(remotePort&&remoteIp){*remotePort=peerPort;*remoteIp=peerIp;}if(socket->local74==0){socket->local74=localPort;}}
(void)native_fn_02008008(enable);
return result;
}
