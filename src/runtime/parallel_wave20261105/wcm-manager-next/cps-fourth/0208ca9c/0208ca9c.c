#include "context.h"
u32 native_main_0208ca9c(u8*iphdr,u8*tcphdr,CPSSoc*soc) {
    return soc->state!=10&&soc->state!=11&&soc->local_port==CPS_GETUSHORT2(tcphdr+2)&&soc->remote_port==CPS_GETUSHORT2(tcphdr)&&soc->remote_ip==CPS_GETULONG2(iphdr+12);
}
