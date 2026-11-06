#include "context.h"
void native_host_arm7_wram_03804bc4(u32 command,u32 value)
{
 u32 data=((command<<8)&0x7f00)|(value&255);
 while(native_host_arm7_arm_037fe410(8,data,0)!=0){}
}
