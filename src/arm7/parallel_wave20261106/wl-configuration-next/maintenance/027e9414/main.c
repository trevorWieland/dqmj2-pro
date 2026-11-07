#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e9414(u32 diversity, u32 useAntenna)
{
    if ((diversity > 1 ) || (useAntenna > 1 )) {
        return 0x05 ;
    }
    switch (diversity) {
    case 0 :
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.UseAntenna = useAntenna;
        break;
    case 1 :
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Mode != 1 ) {
            return 0x0B ;
        }
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.UseAntenna = 0 ;
        break;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Diversity = diversity;
    *(vu16 *)(0x04808000 + 0x290) = (u16)(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Config.UseAntenna ^ ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34)))->Config.MainAntenna) ;
    return 0;
}
