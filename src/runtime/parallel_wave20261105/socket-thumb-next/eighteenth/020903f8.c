#include "context.h"
int native_main_020903f8(int value,const void *buffer,int length,int flags,const void *to){AddressView *address;u16 port;u32 ip;if(to){address=(AddressView *)to;port=SWAP16(address->port2);ip=SWAP32(address->address4);}else{port=0;ip=0;}return native_fn_0208f724(value,buffer,length,port,ip,flags);}
