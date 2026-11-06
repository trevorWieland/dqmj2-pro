#include "context.h"
void native_main_0208ce58(u8*iphdr,u8*tcphdr,u32 len) {
    CPSSoc*soc=native_fn_0208cb1c(iphdr,tcphdr);
    if(!soc||soc->state!=2) {
        native_fn_0208cc24(iphdr,tcphdr,len,0);
        return;
    }
    native_fn_020069f8();
    soc->ackno=CPS_GETULONG2(tcphdr+4)+1;
    soc->remote_ackno=CPS_GETULONG2(tcphdr+8);
    soc->remote_win=CPS_GETUSHORT2(tcphdr+14);
    native_fn_0208cb5c(tcphdr,soc);
    native_fn_0208cc0c(soc,0);
    soc->state=4;
    if(soc->block_type==1) {
        soc->block_type=0;
        native_fn_0200698c(soc->thread);
    }
}
