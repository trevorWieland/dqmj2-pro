#include "context000.h"

#include "context001.h"

#include "context002.h"

LPASSRES_FRAME native_host_arm7_main_027f1888(u16 camAdrs, u16 statusCode, LPSSID_ELEMENT pSSID)
{
    WlMaDataReq *pReq;
    LPASSRES_FRAME pFrm;
    u32 ofst, i, aid;
    u8 *p;
    ;
    pReq = (WlMaDataReq *)native_host_arm7_arm_037f886c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(ASSRES_FRAME) + 4)) + 34);
    if ((u32)pReq == (0) ) {
        native_host_arm7_arm_027eb078(0x0002 );
        return (LPASSRES_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPASSRES_FRAME)&pReq->frame;
    if (statusCode == 0 ) {
        aid = native_host_arm7_arm_027ebebc(camAdrs);
        if (aid == 0) {
            statusCode = 19 ;
        }
    } else {
        aid = 0;
    }
    native_host_arm7_arm_027f1fb4((LPTXFRM)pFrm, native_host_arm7_arm_027ec04c(camAdrs));
    pFrm->Body.CapaInfo.Data = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.CapaInfo;
    pFrm->Body.StatusCode = statusCode;
    pFrm->Body.AID = aid;
    if (aid) {
        pFrm->Body.AID |= 0xC000;
    }
    ofst = native_host_arm7_arm_027f20dc(&pFrm->Body.Buf[0]);
    pFrm->FirmHeader.Length = ofst + 2 + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x01 * 0x0010)) ;
    p = (u8 *)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU);
    if (pSSID != 0 ) {
        u32 len = native_host_arm7_arm_027ead5c(&pSSID->Length);
        native_host_arm7_arm_027ead30(p++, native_host_arm7_arm_027ead5c(&pSSID->ID));
        native_host_arm7_arm_027ead30(p++, len);
        for (i = 0; i < len; i++, p++) {
            native_host_arm7_arm_027ead30(p, native_host_arm7_arm_027ead5c(&pSSID->SSID[i]));
        }
    } else {
        native_host_arm7_arm_027ead30(p++, 0 );
        native_host_arm7_arm_027ead30(p, 0);
    }
    return pFrm;
}

#include "context003.h"
