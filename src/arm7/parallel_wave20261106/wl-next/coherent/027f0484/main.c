#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027f0484(LPTXFRM pFrm, u32 flag)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    WlCounter *pCounter = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter;
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TxPri[1 ];
    LPAUTH_FRAME pAuth;
    LPASSRES_FRAME pAssRes;
    LPDISASS_FRAME pDisAss;
    LPDEAUTH_FRAME pDeAuth;
    u32 bRelease = 1 ;
    u32 i, type, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounter->tx.success++;
        if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
            pCounter->tx.multicast++;
        } else {
            pCounter->tx.unicast++;
        }
        if (native_host_arm7_arm_027ec02c(cam_adrs)) {
            if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
                native_host_arm7_arm_027ebdb4(cam_adrs);
            }
        }
    } else {
        pCounter->tx.failed++;
    }
    if (pFrm->Dot11Header.FrameCtrl.Bit.WEP) {
        pCounter->tx.wep++;
    }
    pCounter->tx.retry += LoadLow(&pFrm->MacHeader.Tx.rsv_RetryCount);
    type = pFrm->Dot11Header.FrameCtrl.Data & (0x00F0 | 0x000C );
    switch (type) {
    case ((0x00 * 0x0004) | (0x0B * 0x0010)) :
        if (cam_adrs == 0) {
            break;
        }
        if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
            pAuth = (LPAUTH_FRAME)pFrm;
            if ((pAuth->Body.AlgoType == 0 ) && (pAuth->Body.SeqNum == 2) && (pAuth->Body.StatusCode == 0 )) {
                native_host_arm7_arm_027ebc50(cam_adrs, 0x30 );
                native_host_arm7_arm_027edb74(pAuth->Dot11Header.DA, pAuth->Body.AlgoType);
            } else if ((pAuth->Body.AlgoType == 1 ) && (pAuth->Body.SeqNum == 4) && (pAuth->Body.StatusCode == 0 )) {
                native_host_arm7_arm_027ebc50(cam_adrs, 0x30 );
                native_host_arm7_arm_027edb74(pAuth->Dot11Header.DA, pAuth->Body.AlgoType);
            }
        }
        else {
        }
        break;
    case ((0x00 * 0x0004) | (0x01 * 0x0010)) :
    case ((0x00 * 0x0004) | (0x03 * 0x0010)) :
        if (cam_adrs == 0) {
            break;
        }
        pAssRes = (LPASSRES_FRAME)pFrm;
        if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
            if ((pAssRes->Body.StatusCode == 0 ) && (native_host_arm7_arm_027ebfec(cam_adrs) == 0x30 )) {
                native_host_arm7_arm_027ebc50(cam_adrs, 0x40 );
                if (type == ((0x00 * 0x0004) | (0x01 * 0x0010)) ) {
                    native_host_arm7_arm_027edc6c(pAssRes->Dot11Header.DA, pAssRes->Body.AID, (LPSSID_ELEMENT)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU));
                } else {
                    native_host_arm7_arm_027edd64(pAssRes->Dot11Header.DA, pAssRes->Body.AID, (LPSSID_ELEMENT)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU));
                }
            }
        }
        else {
            native_host_arm7_arm_027ebf6c(cam_adrs);
            pDeAuth = native_host_arm7_arm_027f1ec8(pAssRes->Dot11Header.DA, 1 , 0 );
            if ((u32)pDeAuth != (0) ) {
                pDeAuth->FirmHeader.FrameId = 0x0002 ;
                if (flag) {
                    TxManCtrlFrame((LPTXFRM)pDeAuth);
                } else {
                    native_host_arm7_arm_027f10a0((LPTXFRM)pDeAuth);
                }
            }
        }
        break;
    case ((0x00 * 0x0004) | (0x0A * 0x0010)) :
        if (pWork->Mode == 1 ) {
            if (cam_adrs != 0) {
                if (native_host_arm7_arm_027ebfec(cam_adrs) > 0x30 ) {
                    native_host_arm7_arm_027ebc50(cam_adrs, 0x30 );
                }
            } else if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                for (i = 1; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum; i++) {
                    if (native_host_arm7_arm_027ebfec(i) > 0x30 ) {
                        native_host_arm7_arm_027ebc50(i, 0x30 );
                    }
                }
            }
        } else {
            if (pWork->STA > 0x30 ) {
                native_host_arm7_arm_037f9238(0x30 );
                native_host_arm7_arm_027ea048();
            }
        }
        if ((pMLME->State == (0x01 | 0x70) ) && (pFrm == pMLME->Work.DisAss.pTxFrm)) {
            pDisAss = (LPDISASS_FRAME)pFrm;
            if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
                pMLME->pCfm.DisAss->resultCode = 0x00 ;
            } else {
                pMLME->pCfm.DisAss->resultCode = 0x0C ;
            }
            pMLME->State = 0x00 ;
            native_host_arm7_arm_027edb20();
        }
        break;
    case ((0x00 * 0x0004) | (0x0C * 0x0010)) :
        if (pWork->Mode == 1 ) {
            if (cam_adrs != 0) {
                if (native_host_arm7_arm_027ebfec(cam_adrs) > 0x20 ) {
                    native_host_arm7_arm_027ebc50(cam_adrs, 0x20 );
                }
            } else if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                for (i = 1; i < ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.MaxStaNum; i++) {
                    if (native_host_arm7_arm_027ebfec(i) > 0x20 ) {
                        native_host_arm7_arm_027ebc50(i, 0x20 );
                    }
                }
            }
        } else {
            if (pWork->STA > 0x20 ) {
                native_host_arm7_arm_037f9238(0x20 );
                native_host_arm7_arm_027ea048();
            }
        }
        if ((pMLME->State == (0x01 | 0x40) ) && (pFrm == pMLME->Work.DeAuth.pTxFrm)) {
            pDeAuth = (LPDEAUTH_FRAME)pFrm;
            if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
                pMLME->pCfm.DeAuth->resultCode = 0x00 ;
            } else {
                pMLME->pCfm.DeAuth->resultCode = 0x0C ;
            }
            pMLME->State = 0x00 ;
            native_host_arm7_arm_027edb20();
        }
        if (pFrm->FirmHeader.FrameId == 0x0001 ) {
            ;
            if (cam_adrs != 0) {
                ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.NotSetTIM &= ~(1 << cam_adrs);
                native_host_arm7_arm_027ec438(cam_adrs);
            }
            native_host_arm7_arm_027edbf0(pFrm->Dot11Header.Adrs1, 1 );
        } else if (pFrm->FirmHeader.FrameId == 0x0002 ) {
            ;
            pDeAuth = (LPDEAUTH_FRAME)pFrm;
            native_host_arm7_arm_027edbf0(pFrm->Dot11Header.Adrs1, pDeAuth->Body.ReasonCode);
        }
        break;
    default:
        break;
    }
    if (bRelease) {
        native_host_arm7_arm_027ebbe0(pFrm);
        native_host_arm7_arm_037f8908(pBufMan, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Txq[1 ].Busy = 0 ;
    if (flag && ((*(LPHEAPBUF_MAN)pBufMan).Count) ) {
        native_host_arm7_arm_027eff00(1 );
    }
}

#include "context003.h"
