#include "context.h"
u32 native_main_0208bb08(u8*s,u32 len,u32 sum){
 if((u32)s&1){while(len>1){sum+=CPS_GETUSHORT1(s);s+=2;len-=2;}}
 else{sum=CPS_htons((u16)sum);while(len>1){sum+=CPS_USHORT2_HOST(s);s+=2;len-=2;}sum=CPS_htonl(sum);}
 if(len)sum+=(u32)*s<<8;
 sum=(sum&0xffff)+(sum>>16);
 return(u16)(sum+(sum>>16));
}
