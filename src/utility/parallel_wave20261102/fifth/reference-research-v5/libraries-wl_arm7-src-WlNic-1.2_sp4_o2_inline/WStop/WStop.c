#include "context000.h"

#include "context001.h"

void WStop(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    ClearPeriodicTimeOut();
    ClearTimeOut();
    WSetStaState(0x20 );
    pWork->bUpdateGameInfo = 0 ;
    pWork->bSynchro = 0;
    *(vu16 *)((0x04808000) + 0x012) = 0;
    *(vu16 *)((0x04808000) + 0x004) = 0;
    *(vu16 *)((0x04808000) + 0x0EA) = 0;
    *(vu16 *)((0x04808000) + 0x0E8) = 0;
    *(vu16 *)((0x04808000) + 0x008) = 0;
    *(vu16 *)((0x04808000) + 0x00A) = 0;
    switch (pWork->Mode) {
    case 1 :
        StopBeaconFrame();
        break;
    }
    *(vu16 *)((0x04808000) + 0x0AC) = 0xFFFF ;
    *(vu16 *)((0x04808000) + 0x0B4) = 0xFFFF;
    DeleteAllTxFrames();
    ReleaseAllWlHeapBuf();
}

#include "context002.h"
