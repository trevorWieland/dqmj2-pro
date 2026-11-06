#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f9300(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    native_utility_child_arm7_arm_027e97ec();
    native_utility_child_arm7_arm_027e9640();
    native_utility_child_arm7_arm_037f93b8(0x20 );
    pWork->bUpdateGameInfo = 0 ;
    pWork->bSynchro = 0;
    *(vu16 *)((0x04808000) + 0x012) = 0;
    *(vu16 *)((0x04808000) + 0x004) = 0;
    *(vu16 *)((0x04808000) + 0x0EA) = 0;
    *(vu16 *)((0x04808000) + 0x0E8) = 0;
    *(vu16 *)((0x04808000) + 0x008) = 0;
    *(vu16 *)((0x04808000) + 0x00A) = 0;
    switch (pWork->Mode) {
    case 1 :
        native_utility_child_arm7_arm_027f15bc();
        break;
    }
    *(vu16 *)((0x04808000) + 0x0AC) = 0xFFFF ;
    *(vu16 *)((0x04808000) + 0x0B4) = 0xFFFF;
    native_utility_child_arm7_arm_027f17f8();
    native_utility_child_arm7_arm_027e8e88();
}
#include "dependency002.h"
