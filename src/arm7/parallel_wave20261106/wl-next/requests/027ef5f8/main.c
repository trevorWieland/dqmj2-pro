#include "context000.h"

#include "context001.h"

#include "context002.h"

u16 native_host_arm7_main_027ef5f8(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    WlMaDataReq *pReq = (WlMaDataReq *)pReqt;
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    LPTXFRM pFrm;
    u32 camAdrs;
    pFrm = (LPTXFRM)&pReq->frame;
    if (pReq->frame.length > 1508 ) {
        ;
        return 0x05 ;
    }
    switch (pConfig->Mode) {
    case 1 :
        camAdrs = native_host_arm7_arm_027eb90c(pFrm->Dot11Header.Adrs1);
        if ((camAdrs == 255 ) || (native_host_arm7_arm_027ebfec(camAdrs) != 0x40 )) {
            return 0x0A ;
        }
        break;
    default:
        camAdrs = pWork->APCamAdrs;
        break;
    }
    pFrm->FirmHeader.CamAdrs = camAdrs;
    pFrm->FirmHeader.FrameTime = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.IntervalCount;
    if (LoadLow(&pFrm->MacHeader.Tx.rsv_AppRate) == 0) {
        pFrm->MacHeader.Tx.Service_Rate = native_host_arm7_arm_027ec0ac(camAdrs);
    } else {
        pFrm->MacHeader.Tx.Service_Rate = pFrm->MacHeader.Tx.rsv_AppRate;
        pFrm->MacHeader.Tx.rsv_AppRate = 0;
    }
    if (pFrm->FirmHeader.Length == 0) {
        pFrm->Dot11Header.FrameCtrl.Data = (pWork->FrameCtrl | 0x0040 ) & ~0x4000 ;
        pFrm->MacHeader.Tx.MPDU = sizeof(pFrm->Dot11Header) + 4;
    } else {
        pFrm->Dot11Header.FrameCtrl.Data = pWork->FrameCtrl;
        if (pConfig->WepMode == 0 ) {
            pFrm->MacHeader.Tx.MPDU = sizeof(pFrm->Dot11Header) + pFrm->FirmHeader.Length + 4;
        } else {
            pFrm->MacHeader.Tx.MPDU = sizeof(pFrm->Dot11Header) + pFrm->FirmHeader.Length + 4 + 4 + 4;
        }
    }
    switch (pConfig->Mode) {
    case 1 :
        native_host_arm7_arm_027ea0ec(pFrm->Dot11Header.Adrs3, pFrm->Dot11Header.Adrs2);
        native_host_arm7_arm_027ea0ec(pFrm->Dot11Header.Adrs2, pWork->BSSID);
        if (camAdrs == 0) {
            native_host_arm7_arm_027ebaf4(&pHeapMan->RequestCmd, pReq);
            if ((((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.PowerMgtMode & ~((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotClass3) == 0) {
                native_host_arm7_arm_027eff00(2 );
            }
        } else {
            native_host_arm7_arm_027ebb50(pFrm);
            native_host_arm7_arm_037f8988(&pHeapMan->RequestCmd, &pHeapMan->TxPri[0 ], pReq);
            native_host_arm7_arm_027eff00(0 );
        }
        break;
    case 2 :
    case 3 :
        native_host_arm7_arm_027ea0ec(pFrm->Dot11Header.Adrs3, pFrm->Dot11Header.Adrs1);
        native_host_arm7_arm_027ea0ec(pFrm->Dot11Header.Adrs1, pWork->BSSID);
        native_host_arm7_arm_027ebb50(pFrm);
        native_host_arm7_arm_037f8988(&pHeapMan->RequestCmd, &pHeapMan->TxPri[0 ], pReq);
        {
            native_host_arm7_arm_027eff00(0 );
        }
        break;
    }
    return 0x81 ;
}
