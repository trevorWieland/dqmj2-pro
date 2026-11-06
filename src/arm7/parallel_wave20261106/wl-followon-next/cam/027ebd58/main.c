#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ebd58(u16 camAdrs, u16 pmtMode)
{
    LPCAM_MAN pCamMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan;
    ;
    pCamMan->PowerMgtMode = (pCamMan->PowerMgtMode & ~(1 << camAdrs)) | (pmtMode << camAdrs);
    if (pCamMan->PowerMgtMode & ~pCamMan->NotClass3) {
        *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 3) ;
    } else {
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 3) ;
    }
}
