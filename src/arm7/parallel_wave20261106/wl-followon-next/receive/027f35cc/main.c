#include "context000.h"

#include "context001.h"

#include "context002.h"

void native_host_arm7_main_027f35cc(LPAUTH_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    LPAUTH_BODY pAuth;
    LPAUTH_FRAME pTxFrm;
    u32 bodyLen, cam_adrs;
    u32 bTxAuth;
    u16 seqNum, txtLen, stsCode;
    bodyLen = pFrm->FirmHeader.Length;
    pAuth = &pFrm->Body;
    ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000008 ) {
        LPTXQ pTxq = ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl.Txq;
        u16 map = *(vu16 *)((0x04808000) + 0x0B0) ;
        if ((((map & (0x0001 << 0) ) == 0) || (pTxq[0].Busy == 0)) && (((map & (0x0001 << 2) ) == 0) || (pTxq[1].Busy == 0)) && (((map & (0x0001 << 3) ) == 0) || (pTxq[2].Busy == 0)) && ((*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 0) ) == 0)) {
            *(vu16 *)((0x04808000) + 0x032) = 0x0000;
            *(vu16 *)((0x04808000) + 0x032) = 0x8000;
            ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->RxCtrl.IcvOkCntFlag = 0;
        }
    }
    if (native_host_arm7_arm_027f2000(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x0B * 0x0010)) )) {
        return;
    }
    bTxAuth = 0 ;
    txtLen = 0;
    seqNum = pAuth->SeqNum + 1;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if (cam_adrs == 0) {
        stsCode = 19 ;
        bTxAuth = 1 ;
    } else {
        if (pWork->Mode == 1 ) {
            if (native_host_arm7_arm_027ebfec(cam_adrs) > 0x20 ) {
                native_host_arm7_arm_027ebc50(cam_adrs, 0x20 );
                native_host_arm7_arm_027edbf0(pFrm->Dot11Header.SA, 1 );
            }
            if ((pFrm->MacHeader.Rx.Status & (0x0001 << 10) ) && (native_host_arm7_arm_027ec06c(cam_adrs) != 0)) {
                pAuth->AlgoType = 1 ;
                stsCode = 15 ;
                seqNum = 4;
                bTxAuth = 1 ;
                native_host_arm7_arm_027ebe78(cam_adrs, 0);
                goto tx_auth;
            }
        }
        switch (pAuth->AlgoType) {
        case 0 :
            if ((pWork->Mode == 1 ) && (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.AuthAlgo == 1 )) {
                stsCode = 13 ;
                bTxAuth = 1 ;
                break;
            }
            if (pWork->Mode == 1 ) {
                if (pAuth->SeqNum == 1) {
                    ;
                    stsCode = 0 ;
                    bTxAuth = 1 ;
                } else {
                    stsCode = 14 ;
                    seqNum = 2;
                    bTxAuth = 1 ;
                }
            }
            else if ((pWork->Mode != 1 ) && (pAuth->SeqNum == 2)) {
                ;
                if ((pMLME->pReq.Auth->algorithm == 0 ) && native_host_arm7_arm_027ea480(pMLME->pReq.Auth->peerMacAdrs, pFrm->Dot11Header.SA)) {
                    if (pMLME->State == (0x01 | 0x30) ) {
                        native_host_arm7_arm_027eabec();
                        if (pAuth->StatusCode == 0x00 ) {
                            native_host_arm7_arm_037f9238(0x30 );
                            pMLME->pCfm.Auth->resultCode = 0x00 ;
                            pMLME->pCfm.Auth->statusCode = 0x00 ;
                        } else {
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                        }
                        pMLME->State = (0x05 | 0x30) ;
                        native_host_arm7_arm_037f8598(2 , 2 );
                    }
                } else {
                }
            }
            break;
        case 1 :
            if (pWork->Mode == 1 ) {
                native_host_arm7_arm_027ebc50(cam_adrs, 0x20 );
                if (pAuth->SeqNum == 1) {
                    ;
                    pTxFrm = native_host_arm7_arm_027f1e08(pFrm->Dot11Header.SA, 128 , 1 );
                    if ((u32)pTxFrm != (0) ) {
                        pTxFrm->Body.AlgoType = pAuth->AlgoType;
                        pTxFrm->Body.SeqNum = seqNum;
                        pTxFrm->Body.StatusCode = 0;
                        SetChallengeText(cam_adrs, pTxFrm);
                        native_host_arm7_arm_027f1088((LPTXFRM)pTxFrm);
                    }
                }
                else if (pAuth->SeqNum == 3) {
                    ;
                    if ((native_host_arm7_arm_027ebfec(cam_adrs) != 0x20 ) || (native_host_arm7_arm_027ec06c(cam_adrs) == 0)) {
                        stsCode = 1 ;
                        bTxAuth = 1 ;
                        break;
                    }
                    if (CheckChallengeText(pFrm) == 0 ) {
                        stsCode = 15 ;
                        bTxAuth = 1 ;
                        native_host_arm7_arm_027ebe78(cam_adrs, 0);
                        break;
                    }
                    native_host_arm7_arm_027ebe78(cam_adrs, 0);
                    stsCode = 0 ;
                    bTxAuth = 1 ;
                }
                else {
                    native_host_arm7_arm_027ebe78(cam_adrs, 0);
                    stsCode = 14 ;
                    seqNum = 2;
                    bTxAuth = 1 ;
                }
                break;
            }
            else {
                if ((pMLME->pReq.Auth->algorithm != 1 ) || (native_host_arm7_arm_027ea480(pMLME->pReq.Auth->peerMacAdrs, pFrm->Dot11Header.SA) == 0)) {
                    break;
                }
                if (pAuth->SeqNum == 2) {
                    ;
                    if (pMLME->State == (0x01 | 0x30) ) {
                        if (pAuth->StatusCode != 0 ) {
                            native_host_arm7_arm_027eabec();
                            pMLME->State = (0x05 | 0x30) ;
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                            native_host_arm7_arm_037f8598(2 , 2 );
                            native_host_arm7_arm_037f9238(0x20 );
                        } else {
                            pMLME->State = (0x03 | 0x30) ;
                            pTxFrm = native_host_arm7_arm_027f1e08(pFrm->Dot11Header.SA, native_host_arm7_arm_027ead5c(&pFrm->Body.ChallengeText.Length), 1 );
                            if ((u32)pTxFrm != (0) ) {
                                pTxFrm->Dot11Header.FrameCtrl.Bit.WEP = 1;
                                MI_CpuCopy16((void *)(u32)&pFrm->Body, (void *) (u32)&pTxFrm->Body, pFrm->FirmHeader.Length + 1) ;
                                pTxFrm->Body.AlgoType = pAuth->AlgoType;
                                pTxFrm->Body.SeqNum = 3;
                                pTxFrm->Body.StatusCode = 0;
                                native_host_arm7_arm_027f1088((LPTXFRM)pTxFrm);
                            }
                        }
                    }
                }
                else if (pAuth->SeqNum == 4) {
                    ;
                    if (pMLME->State == (0x03 | 0x30) ) {
                        native_host_arm7_arm_027eabec();
                        if (pAuth->StatusCode == 0x00 ) {
                            native_host_arm7_arm_037f9238(0x30 );
                            pMLME->pCfm.Auth->resultCode = 0x00 ;
                            pMLME->pCfm.Auth->statusCode = 0x00 ;
                        } else {
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                        }
                        pMLME->State = (0x05 | 0x30) ;
                        native_host_arm7_arm_037f8598(2 , 2 );
                    }
                }
                else {
                }
            }
            break;
        default:
            ;
            if (pWork->Mode == 1 ) {
                stsCode = 13 ;
                bTxAuth = 1 ;
            }
            break;
        }
    }
tx_auth:
    if (bTxAuth) {
        pTxFrm = native_host_arm7_arm_027f1e08(pFrm->Dot11Header.SA, txtLen, (stsCode != 0 ));
        if ((u32)pTxFrm != (0) ) {
            pTxFrm->Body.AlgoType = pAuth->AlgoType;
            pTxFrm->Body.SeqNum = seqNum;
            pTxFrm->Body.StatusCode = stsCode;
            native_host_arm7_arm_027f1088((LPTXFRM)pTxFrm);
        }
    }
}

#include "context003.h"
