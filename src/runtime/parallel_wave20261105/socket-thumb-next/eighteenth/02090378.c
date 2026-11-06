#include "context.h"
int native_main_02090378(int value,void *buffer,int length,int flags,void *from){u16 port;u32 ip;int result;result=native_fn_0208f14c((SocketView *)value,buffer,length,&port,&ip,flags);if(result>=0 && from){AddressView *address=(AddressView *)from;address->port2=SWAP16(port);address->address4=SWAP32(ip);}return result;}
