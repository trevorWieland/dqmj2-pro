#include "context.h"
u32 native_main_0208cd80(u8*iphdr,u8*tcphdr,u32 len) {
    CPSSoc*soc=native_fn_0208cb1c(iphdr,tcphdr);
    if(soc) {
        if(soc->state==1)native_fn_0208ccec(iphdr,tcphdr,soc);
        else if(soc->state==3||soc->state==4) {
            soc->seqno--;
            native_fn_0208ccec(iphdr,tcphdr,soc);
        }
        else native_fn_0208cc24(iphdr,tcphdr,len,0);
        return 1;
    }
    return 0;
}
