#include "context.h"
void native_main_0208cef0(u8*iphdr,u8*tcphdr,u32 len) {
    u32 enabled,remote_ackno,bufok,remote_seqno;
    u8 flag;
    CPSSoc*soc;
    soc=native_fn_0208cb1c(iphdr,tcphdr);
    if(!soc) {
        native_fn_0208cc24(iphdr,tcphdr,len,0);
        return;
    }
    flag=tcphdr[13];
    remote_ackno=CPS_GETULONG2(tcphdr+8);
    if((s32)(remote_ackno-soc->remote_ackno)>0)soc->remote_ackno=remote_ackno;
    remote_seqno=CPS_GETULONG2(tcphdr+4);
    if(soc->state==4&&soc->ackno!=remote_seqno) {
        native_fn_0208cc0c(soc,0);
        return;
    }
    soc->remote_win=CPS_GETUSHORT2(tcphdr+14);
    switch(soc->state) {
        case 0:case 2:native_fn_0208cc24(iphdr,tcphdr,len,0);
        break;
        case 3:soc->state=4;
        if(soc->block_type==1) {
            soc->block_type=0;
            native_fn_0200698c(soc->thread);
        }
        if(len==0)break;
        case 4:soc->ackrcvd++;
        if(len>soc->rcvbuf.size-soc->rcvbufp) {
            len=soc->rcvbuf.size-soc->rcvbufp;
            bufok=0;
        }
        else bufok=1;
        if(len) {
            enabled=native_fn_02007ff4();
            native_fn_02008e0c(tcphdr+(tcphdr[12]&0xf0)/4,soc->rcvbuf.data+soc->rcvbufp,len);
            soc->rcvbufp+=len;
            soc->ackno+=len;
            native_fn_02008008(enabled);
            if(soc->block_type==2) {
                soc->block_type=0;
                native_fn_0200698c(soc->thread);
            }
        }
        if(bufok&&(flag&1)) {
            soc->state=6;
            soc->ackno++;
            native_fn_0208cc18(soc,0);
            if(len==0&&soc->block_type==2) {
                soc->block_type=0;
                native_fn_0200698c(soc->thread);
            }
        }
        else if(len)native_fn_0208cc0c(soc,0);
        break;
        case 7:case 8:if(flag&1) {
            soc->ackno+=len+1;
            native_fn_0208cc0c(soc,0);
            soc->state=0;
            if(soc->block_type==2) {
                soc->block_type=0;
                native_fn_0200698c(soc->thread);
            }
        }
        else {
            if(len) {
                soc->ackno+=len;
                native_fn_0208cc0c(soc,0);
            }
            soc->state=8;
        }
        break;
        case 6:case 9:soc->state=0;
        if(soc->block_type==2) {
            soc->block_type=0;
            native_fn_0200698c(soc->thread);
        }
        break;
        default:if(flag&1)soc->ackno++;
        native_fn_0208cc0c(soc,0);
        break;
    }
    native_fn_020069f8();
}
