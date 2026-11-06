#include "context.h"
void native_main_0208c998(u8*iphdr,u8*icmpdata,u32 len) {
    if(native_fn_0208bb98(icmpdata,len)!=0xffff)return;
    if(!native_fn_0208c97c(CPS_GETULONG2(iphdr+12),CPS_GETULONG2(iphdr+16)))return;
    switch(icmpdata[0]) {
        case 0:native_fn_0208c8d0(iphdr,icmpdata,len);
        break;
        case 8:native_fn_0208c848(iphdr,icmpdata,len);
        break;
        default:return;
    }
}
