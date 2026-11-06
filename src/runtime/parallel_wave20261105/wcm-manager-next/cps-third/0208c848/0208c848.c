#include "context.h"
void native_main_0208c848(u8*iphdr,u8*icmpdata,u32 len) {
    u32 ip_reply_to=native_fn_0208bc18(CPS_GETULONG2(iphdr+12));
    if(ip_reply_to==0)return;
    if(native_fn_0208bf10(ip_reply_to)==NULL) {
        native_fn_0208bf98(ip_reply_to);
        return;
    }
    icmpdata[0]=0;
    CPS_USHORT2_HOST(icmpdata+2)=0;
    CPS_SETUSHORT2(icmpdata+2,native_fn_0208bb98(icmpdata,len));
    native_fn_0208c2b4(icmpdata,len,NULL,0,CPS_GETULONG2(iphdr+12),1);
}
