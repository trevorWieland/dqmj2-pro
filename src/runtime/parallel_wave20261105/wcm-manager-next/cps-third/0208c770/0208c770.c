#include "context.h"
void native_main_0208c770(u8*buf,u32 len) {
    int to_me,from_me;
    u32 ipfrom,my_ip;
    u16 opcode;
    if(len<28||!native_fn_0208bcc4(buf+8,native_data_021d01e0)||G.myip==0)return;
    if(CPS_USHORT2_HOST(buf)!=0x100||CPS_USHORT2_HOST(buf+2)!=8||CPS_USHORT2_HOST(buf+4)!=0x406)return;
    opcode=CPS_GETUSHORT2(buf+6);
    if(opcode!=1&&opcode!=2)return;
    ipfrom=CPS_GETULONG2(buf+14);
    my_ip=G.myip;
    from_me=(ipfrom==my_ip);
    to_me=(CPS_GETULONG2(buf+24)==my_ip);
    if(!from_me)native_fn_0208c080(buf+8,ipfrom,to_me);
    if(opcode==1&&to_me)native_fn_0208c6f8(buf);
    else if(opcode==2&&to_me&&from_me)G.status1=1;
}
