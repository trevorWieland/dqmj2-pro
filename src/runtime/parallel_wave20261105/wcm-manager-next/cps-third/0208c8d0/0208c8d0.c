#include "context.h"
void native_main_0208c8d0(u8*iphdr,u8*icmpdata,u32 len) {
    u32 enable;
    ThreadPrefix*t;
    CPSSoc*soc;
    enable=native_fn_02007ff4();
    for(t=native_data_020e33e4.head;t;t=t->next) {
        soc=t->cps;
        if(soc&&soc->thread&&soc->state==11&&(u16)(u32)soc->thread==CPS_USHORT2_HOST(icmpdata+4)&&soc->local_port==CPS_USHORT2_HOST(icmpdata+6)&&soc->rcvbufp==0&&soc->remote_ip==CPS_GETULONG2(iphdr+12)) {
            len-=8;
            if(len>soc->rcvbuf.size)soc->rcvbufp=soc->rcvbuf.size;
            else soc->rcvbufp=len;
            native_fn_02008e0c(icmpdata+8,soc->rcvbuf.data,soc->rcvbufp);
            if(soc->block_type==3) {
                soc->block_type=0;
                native_fn_0200698c(soc->thread);
            }
            break;
        }
    }
    native_fn_02008008(enable);
}
