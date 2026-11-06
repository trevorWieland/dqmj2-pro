#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f93b8(u32 state)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    if (pWork->STA == state) {
        return;
    }
    if (pWork->STA == 0x40 ) {
        native_utility_child_arm7_arm_027e9640();
    }
    switch (state) {
    case 0x00 :
        native_utility_child_arm7_arm_027ea564();
        break;
    case 0x10 :
        native_utility_child_arm7_arm_027ea5d8((0x0000 << 15) );
        native_utility_child_arm7_arm_037f9300();
        native_utility_child_arm7_arm_027ea4d0();
        break;
    case 0x40 :
        if (pWork->Mode == 2 ) {
            native_utility_child_arm7_arm_027ea3e4();
        }
        native_utility_child_arm7_arm_027e9810(100 , native_utility_child_arm7_arm_027e976c);
        break;
    }
    pWork->STA = state;
}
#include "dependency002.h"
