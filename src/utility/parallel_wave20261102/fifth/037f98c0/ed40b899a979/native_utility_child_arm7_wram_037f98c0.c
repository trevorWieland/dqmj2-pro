#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_wram_037f98c0(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 13) ;
    *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 3) | (0x0001 << 2) | (0x0001 << 0) ;
    if (pWork->bFirstTbtt == 1) {
        pWork->bFirstTbtt = 2;
    } else if (pWork->bFirstTbtt == 2) {
        pWork->bFirstTbtt = 0;
    } else if ((pWork->Mode == 2 ) && (pWork->STA != 0x40 )) {
        *(vu16 *)((0x04808000) + 0x048) = 0;
    }
}
