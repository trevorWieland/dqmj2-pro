#include "context.h"
void native_main_0208fdc8(SocketView *socket){
u32 enable;
if(socket){socket->state70=0;
if(tcp(socket)){native_fn_0208fe74(socket->send68);native_fn_0208fe74(socket->recv64);}
else if(udp(socket)){UdpView *data=socket->recv64->out104;UdpView *next;while(data){next=data->next0;native_data_020de7cc->release1C(data);data=next;}socket->recv64->size108=0;socket->recv64->in100=0;socket->recv64->out104=0;native_fn_02006924(socket->recv64->waiting10C);native_fn_0208fe74(socket->recv64);}
else if(socket->mode73==2){native_fn_0208fe74(socket->send68);}
enable=native_fn_02007ff4();native_fn_02090248(socket);native_fn_02090284(socket);native_data_020de7cc->release1C(socket);(void)native_fn_02008008(enable);}
}
