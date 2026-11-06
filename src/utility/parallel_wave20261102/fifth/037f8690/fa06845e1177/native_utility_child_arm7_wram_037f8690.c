#include "dependency000.h"
#include "dependency001.h"
#include "dependency002.h"

void native_utility_child_arm7_wram_037f8690(void)
{
    OSMessage msg;
    native_utility_child_arm7_arm_037fcc2c(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pRecvMsgQueue, &msg, 1 );
    native_utility_child_arm7_arm_037f86d4(&msg);
    native_utility_child_arm7_arm_037f8558(3 , 12 );
}
#include "dependency003.h"
