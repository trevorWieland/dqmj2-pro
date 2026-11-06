#include "context.h"
void native_main_0208c488(u8*data,u32 len,CPSSoc*soc){
 u8*hdr=soc->sndbuf.data+34;
 CPS_SETULONG2(hdr-12,CPSMyIp);
 CPS_SETULONG2(hdr-8,soc->remote_ip);
 CPS_SETUSHORT2(hdr-4,17);
 CPS_SETUSHORT2(hdr+4,len+8);
 CPS_USHORT2_HOST(hdr-2)=CPS_USHORT2_HOST(hdr+4);
 CPS_SETUSHORT2(hdr+2,soc->remote_port);
 CPS_SETUSHORT2(hdr,soc->local_port);
 CPS_USHORT2_HOST(hdr+6)=0;
 CPS_SETUSHORT2(hdr+6,native_fn_0208bb84((u16)native_fn_0208bb08(data,len,native_fn_0208bb08(hdr-12,20,0))));
 native_fn_0208c2b4(hdr,8,data,len,soc->remote_ip,17);
}
