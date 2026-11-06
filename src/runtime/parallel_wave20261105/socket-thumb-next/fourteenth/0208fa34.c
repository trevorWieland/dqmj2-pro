#include "context.h"
int native_main_0208fa34(void *arg){
WriteCommand *command=(WriteCommand *)arg;
SocketView *socket=command->socket4;
SendView *send=socket->send68;
u8 *sendBuffer;
int sendLength,offset,copied=0,result;
if(!tcp(socket)||state(socket,4)){
if(command->peer28){native_fn_0208d780(command->local24,command->remote26,command->peer28);}
offset=tcp(socket)?54:42;sendBuffer=socket->cps0.sendBuffer4C+offset;
if(tcp(socket)){sendLength=native_fn_0208fb2c((int)socket->cps0.sendSize48-offset);}else{sendLength=(int)socket->cps0.sendSize48-offset;}
for(;;){result=native_fn_0208fb94(sendBuffer,sendLength,command);if(result<=0){break;}result=(int)native_fn_0208dd38(sendBuffer,(u32)result);if(result<=0){if(tcp(socket)){socket->state70&=~14;socket->state70|=128;native_fn_0208d910();}copied=-76;break;}copied+=result;}}
else{copied=-76;}
send->out102=command->after20;native_fn_02006924(send->waiting104);return copied;
}
