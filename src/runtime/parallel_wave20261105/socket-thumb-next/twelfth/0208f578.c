#include "context.h"
int native_main_0208f578(SocketView *socket,void *buffer,int bufferLength,u16 *remotePort,u32 *remoteIp,s32 flagBlock){
RecvView *receive=socket->recv64;
UdpView *data=receive->out104;
u32 enable;
int result;
enable=native_fn_02007ff4();
while((data=receive->out104)==0){if(!(flagBlock&1)){result=-6;break;}native_fn_020068d4(receive->waiting10C);if(native_fn_02090294(socket)||!created(socket)){result=-56;break;}}
if(data){if(bufferLength>data->size4){bufferLength=data->size4;}native_fn_02008e0c((u8 *)&data[1],buffer,(u32)bufferLength);if(remotePort){*remotePort=data->remote6;}if(remoteIp){*remoteIp=data->peer8;}result=data->size4;if(!receive->noConsumeFE){receive->out104=data->next0;if(data->next0==0){receive->in100=0;}native_data_020de7cc->release1C(data);receive->size108-=result;}}
(void)native_fn_02008008(enable);
return result;
}
