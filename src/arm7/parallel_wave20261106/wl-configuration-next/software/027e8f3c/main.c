#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e8f3c(u16 mode)
{
    if (mode > 3 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Mode = mode;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Mode = mode;
    *(vu16 *)((0x04808000) + 0x006) = (u16)((*(vu16 *)((0x04808000) + 0x006) & (u16)~ (0x0007 << 0)) | ((u16) mode)) ;
    native_host_arm7_arm_027e9c58(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.PowerMgtMode);
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.ParamFlag |= (0x01UL << 3) ;
    return 0;
}

#include "context002.h"
