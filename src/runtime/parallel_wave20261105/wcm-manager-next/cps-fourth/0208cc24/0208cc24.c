#include "context.h"
void native_main_0208cc24(u8*iphdr,u8*tcphdr,u32 len,u16 urgent) {
    CPSSoc*soc=&R.reset;
    native_fn_02008d78(soc,0,sizeof(CPSSoc));
    R.reset.local_port=CPS_GETUSHORT2(tcphdr+2);
    R.reset.remote_port=CPS_GETUSHORT2(tcphdr);
    R.reset.remote_ip=CPS_GETULONG2(iphdr+12);
    if(tcphdr[13]&0x10) {
        soc->seqno=CPS_GETULONG2(tcphdr+8);
        native_fn_0208cbc4(soc,4,urgent);
    }
    else {
        soc->seqno=0;
        soc->ackno=CPS_GETULONG2(tcphdr+4)+len;
        if(tcphdr[13]&3)soc->ackno++;
        native_fn_0208cbc4(soc,0x14,urgent);
    }
}
