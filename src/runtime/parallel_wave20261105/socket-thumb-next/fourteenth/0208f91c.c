#include "context.h"
int native_main_0208f91c(SocketView *socket,const u8 *buffer,s32 length,s32 writeIn,u16 remotePort,u32 peer,s32 flagBlock){
SendView *send=socket->send68;
WriteCommand *command;
u8 *writeBuffer;
s32 writeSize;
int result;
u16 savedIn;
command=native_fn_0208ebd8(native_fn_0208fa34,send->executor10C,flagBlock);
if(command==0){return -33;}
if((flagBlock&1)&&!udp(socket)){command->blockD=3;}else{command->blockD=0;}
writeBuffer=send->bufferFC;writeSize=(s32)send->sizeF8;
if(writeIn+length<writeSize){command->first10=writeBuffer+writeIn;command->firstLength14=length;command->second18=0;command->secondLength1C=0;writeIn+=length;}
else{const u8 *buffer2;command->first10=writeBuffer+writeIn;command->firstLength14=writeSize-writeIn;command->second18=writeBuffer;command->secondLength1C=length-command->firstLength14;writeIn=command->secondLength1C;buffer2=buffer+command->firstLength14;native_fn_02008e0c(buffer2,command->second18,(u32)command->secondLength1C);}
native_fn_02008e0c(buffer,command->first10,(u32)command->firstLength14);
savedIn=send->in100;send->in100=command->after20=(u16)writeIn;
if(udp(socket)){if(socket->local74==0){socket->local74=native_fn_0208d6b4();socket->cps0.localA=socket->local74;}command->local24=socket->local74;
if(socket->peer78==0 || peer!=0){command->peer28=peer;command->remote26=remotePort;}else{command->peer28=socket->peer78;command->remote26=socket->remote76;}}
else{command->peer28=0;}
result=native_fn_0208ecb0(send->executor10C,command);
if(result!=0){send->in100=savedIn;length=0;}
return(int)length;
}
