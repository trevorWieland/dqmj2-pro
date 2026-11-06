#include "context000.h"

#include "context001.h"

#include "context002.h"

LPPRBRES_FRAME native_host_arm7_main_027f1be8(u16 *pDA)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    WlMaDataReq *pReq;
    LPPRBRES_FRAME pFrm;
    u32 ofst;
    ;
    if (!native_host_arm7_arm_027f1680()) {
        ;
        return (0) ;
    }
    pReq = (WlMaDataReq *)native_host_arm7_arm_037f886c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(PRBRES_FRAME) + 4)) + pWork->GameInfoLength);
    if ((u32)pReq == (0) ) {
        native_host_arm7_arm_027eb078(0x0002 );
        return (LPPRBRES_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPPRBRES_FRAME)&pReq->frame;
    native_host_arm7_arm_027f1fb4((LPTXFRM)pFrm, pDA);
    pFrm->Body.BeaconInterval = pWork->BeaconPeriod;
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    ofst = native_host_arm7_arm_027f2068(&pFrm->Body.Buf[0]);
    ofst += native_host_arm7_arm_027f20dc(&pFrm->Body.Buf[ofst]);
    ofst += SetDSParamSet(&pFrm->Body.Buf[ofst]);
    ofst += SetGameInfoElement(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 8 + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x05 * 0x0010)) ;
    return pFrm;
}

#include "context003.h"
