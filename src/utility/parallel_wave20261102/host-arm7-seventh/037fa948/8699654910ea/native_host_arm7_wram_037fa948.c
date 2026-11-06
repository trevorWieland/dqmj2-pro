#include "dependency000.h"
#include "dependency001.h"
#include "dependency002.h"

void native_host_arm7_wram_037fa948(void)
{
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->RxCtrl;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan;
    LPRXFRM_MAC pMFrm;
    LPRXFRM pFrm;
    u32 bnry, curr, length, status, i, bRelease, next_bnry;
    for (i = 0;; i++) {
        bnry = *(vu16 *)((0x04808000) + 0x05A) ;
        curr = pRxCtrl->wlCurr;
        if (bnry == curr) {
            break;
        }
        if (bnry >= (0x1000 + 0x1B0 - 36) / 2) {
            native_host_arm7_arm_027ea1b8();
        }
        pMFrm = (LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(bnry) * 2)) ;
        next_bnry = *(u16 *)native_host_arm7_arm_037fa6c8(&pMFrm->MacHeader.Rx.NextBnry);
        if (pMFrm->MacHeader.Rx.Status == 0xFFFF) {
            *(vu16 *)((0x04808000) + 0x05A) = next_bnry;
            continue;
        }
        length = *(u16 *)native_host_arm7_arm_037fa6c8(&pMFrm->MacHeader.Rx.MPDU);
        pFrm = native_host_arm7_arm_037fae50(pMFrm, length);
        *(vu16 *)((0x04808000) + 0x05A) = next_bnry;
        if ((u32)pFrm == (0) ) {
            if ((pMFrm->MacHeader.Rx.Status & (0x000F) ) == (0x000C << 0) ) {
                native_host_arm7_arm_027eb078(0x0010 );
            } else {
                native_host_arm7_arm_027eb078(0x0008 );
            }
            continue;
        }
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000008 ) {
            if (pFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) {
                pRxCtrl->IcvOkCntFlag = 0;
            }
        }
        status = pFrm->MacHeader.Rx.Status;
        bRelease = 1 ;
        if (status & (0x0001 << 9) ) {
            if ((pFrm->Dot11Header.FrameCtrl.Bit.MoreFrag == 1) || (pFrm->Dot11Header.SeqCtrl.Bit.FragNum != 0)) {
                bRelease = 0 ;
                native_host_arm7_arm_037f8988(&pHeapMan->TmpBuf, &pHeapMan->Defrag, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                native_host_arm7_arm_037f8598(2 , 9 );
            }
        } else {
            switch (status & (0x000F) ) {
            case (0x0008 << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & (0x0003 | 0x000C )) == 0x02 * 0x0004 ) {
                    bRelease = 0 ;
                    native_host_arm7_arm_037f8988(&pHeapMan->TmpBuf, &pHeapMan->RxData, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                    native_host_arm7_arm_037f8598(2 , 6 );
                }
                break;
            case (0x0001 << 0) :
                if (pFrm->Dot11Header.FrameCtrl.Data == ((0x00 * 0x0004) | (0x08 * 0x0010)) ) {
                    ;
                    ;
                    native_host_arm7_arm_027f284c((LPBEACON_FRAME)pFrm);
                    ;
                    ;
                }
                break;
            case (0x0000 << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & (0x0003 | 0x000C )) == 0x00 * 0x0004 ) {
                    bRelease = 0 ;
                    native_host_arm7_arm_037f8988(&pHeapMan->TmpBuf, &pHeapMan->RxManCtrl, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                    native_host_arm7_arm_037f8598(1 , 7 );
                }
                break;
            case (0x0005 << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & 0xE7FF) == ((0x01 * 0x0004) | (0x0A * 0x0010)) ) {
                    bRelease = 0 ;
                    native_host_arm7_arm_037f8988(&pHeapMan->TmpBuf, &pHeapMan->RxManCtrl, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                    native_host_arm7_arm_037f8598(1 , 7 );
                }
                break;
            case (0x000E << 0) :
            case (0x000F << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & 0xE7BF) == (((0x02 * 0x0004) | (0x01 * 0x0010)) | 0x0100) ) {
                    native_host_arm7_arm_027f25cc(pFrm);
                }
                break;
            case (0x000C << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & 0xE7FF) == (((0x02 * 0x0004) | (0x02 * 0x0010)) | 0x0200) ) {
                    ;
                    ;
                    ;
                    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.PowerState == ((0x0001 << 0) >> 1)) {
                        *(vu16 *)((0x04808000) + 0x03C) = (0x0001 << 0) ;
                    }
                    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.multiPoll.rxMp++;
                    bRelease = native_host_arm7_arm_027f2450(pFrm);
                    ;
                    ;
                    ;
                }
                break;
            case (0x000D << 0) :
                if ((pFrm->Dot11Header.FrameCtrl.Data & 0xE7FF) == (((0x02 * 0x0004) | (0x01 * 0x0010)) | 0x0200) ) {
                    ;
                    ;
                    ;
                    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.multiPoll.rxMpAck++;
                    bRelease = native_host_arm7_arm_027f2778(pFrm);
                    ;
                    ;
                }
                break;
            default:
                break;
            }
        }
        if (bRelease) {
            native_host_arm7_arm_037f8908(&pHeapMan->TmpBuf, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
        }
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000001 ) {
            u16 *pClr = (u16 *)pMFrm;
            u32 j;
            for (j = 0; j < 7; j++) {
                if ((u32)pClr >= ((0x04800000 + 0x4000) + 0x1F60 )) {
                    pClr = (u16 *)((u32)pClr - (u32)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.Ofst.RxBuf.Size);
                }
                *pClr++ = 0xFFFF;
            }
        }
    }
}
#include "dependency003.h"
