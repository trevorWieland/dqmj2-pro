#include "context000.h"

#include "context001.h"

static LPRXFRM TakeoutRxFrame(LPRXFRM_MAC pMFrm, u32 length) __attribute__((never_inline))
{
    LPRXPACKET pPacket;
    LPRXFRM pFrm;
    ;
    pPacket = (LPRXPACKET)AllocateHeapBuf(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, length + sizeof(WlCmdHeader) + sizeof(MAC_HEADER) + sizeof(FIRM_HEADER) + sizeof(WlCmdCfm));
    if ((u32)pPacket == (0) ) {
        ;
        ;
        return (LPRXFRM)(0) ;
    }
    pFrm = (LPRXFRM)&pPacket->frame;
    ;
    DMA_Read((void *)&pFrm->MacHeader, (void *)pMFrm, length + sizeof(MAC_HEADER));
    pFrm->FirmHeader.Length = length - 24;
    StoreHigh(&pFrm->MacHeader.Rx.Service_Rate, LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI));
    ;
    return pFrm;
}
