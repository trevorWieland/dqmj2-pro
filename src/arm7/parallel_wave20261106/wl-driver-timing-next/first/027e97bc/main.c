#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027e97bc(void)
{
    u16 macAdrs[3];
    u16 ench;
    ;
    native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->macAdrs[0]) , 6, (u8 *)macAdrs);
    native_host_arm7_arm_027f4e1c((u32)(&((LPFLASH_TABLE)0x002a)->enableChannel) , 2, (u8 *)&ench);
    native_host_arm7_arm_027e8e68(macAdrs);
    native_host_arm7_arm_027e8ec8(7 );
    native_host_arm7_arm_027e8efc(ench & 0x7FFE);
    native_host_arm7_arm_027e8f3c(2 );
    native_host_arm7_arm_027e8fbc(0 );
    native_host_arm7_arm_027e8ff0(0 );
    native_host_arm7_arm_027e9090(0 );
    native_host_arm7_arm_027e90b4((u16 *)native_host_arm7_data_027f730c);
    native_host_arm7_arm_027e96ec(500 );
    native_host_arm7_arm_027e9114(0 );
    native_host_arm7_arm_027e914c(0 );
    native_host_arm7_arm_027e9184(16 );
    native_host_arm7_arm_027e91bc(0xFFFF , 0 );
    native_host_arm7_arm_027e926c((u16 *)native_host_arm7_data_027f72ac);
    native_host_arm7_arm_027e929c(1 );
    native_host_arm7_arm_027e9344(0 );
    native_host_arm7_arm_027e9b98((LPRATE_SET)&native_host_arm7_data_027f72a8);
    native_host_arm7_arm_027e9368(0 , 0x1F );
    native_host_arm7_main_027e9e3c(5 );
    native_host_arm7_arm_027e9414(0 , 0 );
    native_host_arm7_arm_027e93ac(0 );
    native_host_arm7_arm_027e94e8(0 );
    native_host_arm7_arm_027e9528(0 );
    native_host_arm7_arm_027ead78(*(vu16 *)(0x04808000 + 0x044) + (*(vu16 *)(0x04808000 + 0x044) << 8), *(vu16 *)(0x04808000 + 0x044) );
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.RxDtims = 1 ;
}

#include "context003.h"
