#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e93ac(u32 mainAntenna)
{
    if (mainAntenna > 1 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MainAntenna = mainAntenna;
    *(vu16 *)(0x04808000 + 0x290) = (u16)(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Config.UseAntenna ^ ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Config.MainAntenna) ;
    return 0;
}
