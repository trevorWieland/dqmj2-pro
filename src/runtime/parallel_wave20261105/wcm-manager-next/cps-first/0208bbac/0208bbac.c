#include "context.h"
u32 native_main_0208bbac(u8*tcpudp_hdr,u32 len,u8*ip_hdr,u16 proto){u32 sum;sum=native_fn_0208bb08(tcpudp_hdr,len,proto);sum=native_fn_0208bb08(ip_hdr+12,8,sum);sum+=len;if(sum&0x10000)sum=(u16)(sum+1);return sum!=0xffff;}
