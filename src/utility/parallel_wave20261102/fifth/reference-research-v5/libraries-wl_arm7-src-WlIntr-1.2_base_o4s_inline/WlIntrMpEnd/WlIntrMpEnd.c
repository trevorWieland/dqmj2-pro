#include "context000.h"

#include "context001.h"

static void WlIntrMpEnd(u32 bMacBugPatch)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TxCtrl;
    u32 cnt;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 12) ;
    ;
    if (pTxCtrl->Mp.Busy == 0 ) {
        ;
        return;
    }
    ;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->WlOperation & 0x00000010 ) {
        if (bMacBugPatch) {
            u16 pri = *(vu16 *)((0x04808000) + 0x0B6) ;
            u16 state = *(vu16 *)(0x04808000 + 0x214) ;
            if ((state == 3 ) || (state == 5 )) {
                if (pri == 0) {
                    u16 tm, map;
                    ;
                    map = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2;
                    cnt = 0;
                    while (map != 0) {
                        cnt += (map & 1);
                        map >>= 1;
                    }
                    tm = cnt * (10 + *(u16 *)&pTxCtrl->Mp.pMacFrm->Body[0]) + 96 + (pTxCtrl->Mp.pMacFrm->MacHeader.Tx.MPDU) * 4 + 96;
                    SetupUsTimeOut(tm, MacBugTxMp);
                    ;
                    ;
                    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.MpEndErrCount++;
                    return;
                }
            }
        }
    }
    ;
    ;
    ;
    AddTask(0 , 16 );
    ;
}

#include "context002.h"
