#include "context.h"
void native_host_arm7_wram_03804b80(u32 command,u32 value,s32 error)
{
 u32 data=0x03000000|(((command&255)|128)<<8)|(value&255);
 while(native_host_arm7_arm_037fe410(8,data,error)<0){}
}
