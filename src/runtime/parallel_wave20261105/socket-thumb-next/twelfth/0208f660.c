#include "context.h"
int native_main_0208f660(u8 *data,u32 length,CpsView *cps){
SocketView *socket=(SocketView *)cps;
RecvView *receive=socket->recv64;
UdpView *packet;
u32 enable=native_fn_02007ff4();
if(receive->max10A>=receive->size108+length){packet=native_data_020de7cc->allocate18(sizeof(UdpView)+length);if(packet){receive->size108+=length;packet->next0=0;packet->size4=(u16)length;packet->remote6=cps->remote18;packet->peer8=cps->peer1C;native_fn_02008e0c(data,(void *)&packet[1],length);if(receive->in100){receive->in100->next0=packet;}receive->in100=packet;if(receive->out104==0){receive->out104=packet;}}
else{native_data_021d15a4[0]++;}}else{native_data_021d15a4[1]++;}
if(socket->local74==0){socket->local74=cps->localA;}
cps->remote18=cps->bound1A;cps->peer1C=cps->bound20;
native_fn_02006924(receive->waiting10C);
(void)native_fn_02008008(enable);
return 1;
}
