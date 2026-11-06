#include "context.h"
void native_host_arm7_wram_038052fc(void)
{
 *(volatile u16*)0x04000304 &=~2;
 native_host_arm7_arm_0380528c(1);
 native_host_arm7_arm_03804f54(1);
}
