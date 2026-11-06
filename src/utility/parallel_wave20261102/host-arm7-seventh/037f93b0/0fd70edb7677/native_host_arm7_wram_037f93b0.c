#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_wram_037f93b0(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 15) ;
    ;
    ;
    if ((pWork->STA == 0x40 ) && (pWork->BeaconLostTh != 0) && (pWork->CurrListenInterval == pWork->ListenInterval)) {
        if (++pWork->BeaconLostCnt > pWork->BeaconLostTh) {
            ;
            ;
            pWork->BeaconLostCnt = 0;
            native_host_arm7_arm_037f8598(1 , 13 );
            ;
            ;
        }
    }
    pWork->PowerState = 1;
    ;
}
