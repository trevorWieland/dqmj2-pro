#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e9d88(void)
{
    u32 bp;
    *(vu16 *)(0x04808000 + 0x036) = 0 ;
    WWait(8);
    *(vu16 *)(0x04808000 + 0x168) = 0;
    switch (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Rf.Id) {
    case 2 :
        bp = BBP_Read(0x01);
        native_host_arm7_arm_027ea5fc(0x01, bp & 0x7F);
        native_host_arm7_arm_027ea5fc(0x01, bp);
        WWait(40);
        native_host_arm7_arm_027ea7cc();
        break;
    case 3 :
        native_host_arm7_arm_027ea7cc();
        break;
    default:
        ;
        break;
    }
}

#include "context002.h"
