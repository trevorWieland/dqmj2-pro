#include "context.h"
void native_main_0208c1e0(u8*hdr,u32 hdr_len,u8*body,u32 body_len,u32 ip_to,u32 offset){
 CPS_SETUSHORT2(hdr-18,hdr_len+20+body_len);
 CPS_SETUSHORT2(hdr-14,offset);
 CPS_USHORT2_HOST(hdr-10)=0;
 CPS_SETUSHORT2(hdr-10,native_fn_0208bb98(hdr-20,20));
 if(ip_to!=0x7f000001&&ip_to!=CPSMyIp)native_fn_0208c140(hdr-20,hdr_len+20,body,body_len,ip_to,0x0800);
 if(ip_to==0x7f000001||ip_to==CPSMyIp||native_fn_0208bc58(ip_to)){
  u32 intr;
  native_fn_02008e0c(native_data_020de7b4,hdr-28,8);
  intr=native_fn_02007ff4();
  native_fn_0208bd24(native_data_021d01e0,native_data_021d01e0,hdr-28,hdr_len+28,body,body_len);
  native_fn_02008008(intr);
 }
}
