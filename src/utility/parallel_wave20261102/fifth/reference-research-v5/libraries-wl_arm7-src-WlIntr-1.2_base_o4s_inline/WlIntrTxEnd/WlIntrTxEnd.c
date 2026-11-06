#include "context000.h"

#include "context001.h"

static void WlIntrTxEnd(void) __attribute__((never_inline))
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 txFrm;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 1) ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA == 0x12 ) {
        void IntrCarrierSuppresionSignal(void);
        IntrCarrierSuppresionSignal();
        return;
    }
    ;
    ;
    txFrm = *(vu16 *)((0x04808000) + 0x0B8) & (0x000F << 8) ;
    switch (txFrm) {
    case (0x0003 << 8) :
        if (pTxCtrl->Flag & 0x0002 ) {
            SetParentTbttTxq();
        }
        ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Counter.tx.beacon++;
        AddTask(0 , 8 );
        break;
    case (0x0008 << 8) :
        ;
        if (pTxCtrl->RetryLimit <= (u16)LoadLow(&pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount)) {
            *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 1) ;
            pTxCtrl->MpBlkCnt++;
            ;
        }
        pTxCtrl->pMpEndInd->mpKey.txCount++;
        break;
    case (0x000B << 8) :
        ;
        *(u16 *)((0x04800000 + 0x4000) + 0x1f70) = 0xFFFF;
        *(u16 *)((0x04800000 + 0x4000) + 0x1f72) = 0xFFFF;
        *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
        *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
        if (pTxCtrl->Mp.Busy) {
            if (pTxCtrl->Mp.pMacFrm->Dot11Header.SeqCtrl.Data == 0xFFFF) {
                u16 retry = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount;
                if (retry != 0) {
                    pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
                    ;
                    pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2 = pTxCtrl->SetKeyMap;
                }
            }
        }
        {
            u16 setmap, pollmap;
            WlMpKeyData *pKeyData;
            setmap = pTxCtrl->SetKeyMap;
            pollmap = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2;
            pKeyData = (WlMpKeyData *)pTxCtrl->pMpEndInd->mpKey.data;
            if ((pollmap > 1) && (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.Diversity != 0 )) {
                if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) || (0x0001 << 6) )) == 0) {
                    *(vu16 *)(0x04808000 + 0x290) ^= 1 ;
                }
            }
            if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000040 ) {
                while (pollmap > 1) {
                    pollmap >>= 1;
                    if (pollmap & 1) {
                        pKeyData->noResponse++;
                    }
                    setmap >>= 1;
                    if (setmap & 1) {
                        pKeyData = (WlMpKeyData *)((u32)pKeyData + pTxCtrl->pMpEndInd->mpKey.length);
                    }
                }
            }
        }
        break;
    default:
        break;
    }
    if ((txFrm != (0x0008 << 8) ) && ((*(vu16 *)((0x04808000) + 0x0B0) & (0x0001 << 1) ) == 0)) {
        if (pTxCtrl->Mp.Busy) {
            *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 1) ;
            *(vu16 *)((0x04808000) + 0x048) = 0;
            if ((*(vu16 *)((0x04808000) + 0x010) & (0x0001 << 12) ) == 0) {
                WlIntrMpEnd(2);
            } else {
                pTxCtrl->MpLastOk++;
            }
            pTxCtrl->MpRstCnt++;
        }
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 1) ;
        ;
    }
    AddTask(0 , 14 );
    ;
}

#include "context002.h"
