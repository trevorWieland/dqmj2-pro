#include "context000.h"

#include "context001.h"

u16 native_host_arm7_main_027e9f60(u32 length, u8 *pGameInfo)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    u8 *p;
    u32 i;
    if (length > 128 ) {
        return 0x04 ;
    }
    if (length != 0) {
        if (pWork->GameInfoAlign & 1) {
            p = (u8 *)pWork->GameInfoAdrs;
            native_host_arm7_arm_027ead30(p, 0xFF);
            p++;
            for (i = 0; i < length; i++) {
                native_host_arm7_arm_027ead30(p, native_host_arm7_arm_027ead5c(pGameInfo));
                p++;
                pGameInfo++;
            }
        } else {
            MI_CpuCopy16((void *)(u32)pGameInfo, (void *) (u32)pWork->GameInfoAdrs, length + 1) ;
        }
    }
    pWork->GameInfoLength = length;
    pWork->bUpdateGameInfo = 1 ;
    return 0;
}

#include "context002.h"
