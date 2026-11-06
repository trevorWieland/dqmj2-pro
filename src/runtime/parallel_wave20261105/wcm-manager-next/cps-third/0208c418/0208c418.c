#include "context.h"
void native_main_0208c418(u8*pattern,u32 len,CPSSoc*soc) {
    u8*icmp=soc->sndbuf.data+34;
    u16 sequence;
    CPS_USHORT2_HOST(icmp)=8;
    CPS_USHORT2_HOST(icmp+4)=(u16)(u32)native_data_020e33e4.current;
    sequence=G.pingId;
    CPS_USHORT2_HOST(icmp+2)=0;
    soc->local_port=sequence;
    G.pingId=sequence+1;
    CPS_USHORT2_HOST(icmp+6)=sequence;
    CPS_SETUSHORT2(icmp+2,native_fn_0208bb84((u16)native_fn_0208bb08(pattern,len,native_fn_0208bb08(icmp,8,0))));
    native_fn_0208c2b4(icmp,8,pattern,len,soc->remote_ip,1);
}
