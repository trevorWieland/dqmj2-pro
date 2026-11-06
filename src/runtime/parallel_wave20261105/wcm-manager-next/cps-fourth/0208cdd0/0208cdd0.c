#include "context.h"
void native_main_0208cdd0(u8*iphdr,u8*tcphdr,u32 len) {
    CPSSoc*soc;
    if(!native_fn_0208c97c(CPS_GETULONG2(iphdr+12),CPS_GETULONG2(iphdr+16)))return;
    if(native_fn_0208cd80(iphdr,tcphdr,len))return;
    soc=native_fn_0208ca18(iphdr,tcphdr);
    if(soc)native_fn_0208ccec(iphdr,tcphdr,soc);
    else {
        native_fn_020069f8();
        soc=native_fn_0208ca18(iphdr,tcphdr);
        if(soc)native_fn_0208ccec(iphdr,tcphdr,soc);
    }
}
