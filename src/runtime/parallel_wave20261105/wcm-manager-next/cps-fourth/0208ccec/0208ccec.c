#include "context.h"
void native_main_0208ccec(u8*iphdr,u8*tcphdr,CPSSoc*soc) {
    soc->state=3;
    soc->when=tick();
    soc->local_ip_real=CPS_GETULONG2(iphdr+16);
    soc->remote_port=CPS_GETUSHORT2(tcphdr);
    soc->remote_ip=CPS_GETULONG2(iphdr+12);
    soc->ackno=CPS_GETULONG2(tcphdr+4)+1;
    native_fn_0208cb5c(tcphdr,soc);
    native_fn_0208cbc4(soc,0x12,0);
}
