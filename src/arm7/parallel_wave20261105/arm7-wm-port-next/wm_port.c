#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e692c(u16 pollBitmap)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlMaMpCfm *wlResult;
    const u16 resume = 0;
    const u16 retryLimit = 0;
    u32 txop;
    u16 tmptt;
    u16 currTsf;
    u32 destBitmap;
    u32 dataLength;
    u16 wmHeader;
    u32 currPollBitmap;
    u32 childBitmap;
    u32 mpReadyBitmap;
    {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        childBitmap = status->child_bitmap;
        mpReadyBitmap = status->mp_readyBitmap;
        (void)native_host_arm7_arm_037fdd14(e);
    }
    wmHeader = 0;
    if (status->mp_newFrameFlag == 1 ) {
        pollBitmap = 0xffffU;
        status->mp_newFrameFlag = 0 ;
    }
    if (status->mp_pingFlag == 0 ) {
        u16 recvSize = status->mp_recvSize;
        int nextRecvBufSize;
        if (WmspMakePortPacket(pollBitmap, childBitmap, mpReadyBitmap, &wmHeader, &destBitmap, &dataLength) == WM_ERRCODE_FAILED) {
            ((void)0) ;
            status->mp_count = 0;
            status->mp_limitCount = 0;
            return;
        }
        txop = (u32)(recvSize + 2 );
        if (status->mp_current_minPollBmpMode == 1 ) {
            currPollBitmap = destBitmap;
        } else {
            currPollBitmap = pollBitmap;
        }
        currPollBitmap &= childBitmap;
        nextRecvBufSize = WMSP_GetMPOneReceiveBufferSizeParent(recvSize, native_host_arm7_arm_03803830(currPollBitmap));
        if (status->mp_recvBufSize < nextRecvBufSize) {
            ((void)0)
                ;
            (void)native_host_arm7_main_027e74f8(0 , (u16)currPollBitmap);
            status->mp_count = 0;
            status->mp_limitCount = 0;
            return;
        }
        if (status->mp_count == 1 || status->mp_limitCount == 1) {
            tmptt = native_host_arm7_main_027e7c20(dataLength, txop, currPollBitmap, status->mp_parentVCount);
            wmHeader |= 0x8000 ;
        } else {
            tmptt = 0;
        }
    } else {
        ((void) 0) ;
        status->mp_pingFlag = 0 ;
        currPollBitmap = childBitmap;
        txop = 0x80d6;
        tmptt = 0;
        dataLength = 0;
        wmHeader &= ~0x8000 ;
        {
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            status->mp_count++;
            status->mp_limitCount++;
            (void)native_host_arm7_arm_037fdd14(e);
        }
    }
    ((void)0) ;
    currTsf = *(u16 *)((0x04808000) + 0x0F8) ;
    wlResult = native_host_arm7_arm_027e2314((u16 *)wlBuf, resume, retryLimit, (u16)txop, (u16)currPollBitmap, tmptt, currTsf, (u16)dataLength, wmHeader, (u16 *)status->mp_sendBuf);
    status->mp_prevPollBitmap = (u16)currPollBitmap;
    status->mp_prevWmHeader = wmHeader;
    status->mp_prevTxop = (u16)txop;
    status->mp_prevDataLength = (u16)dataLength;
    if (wlResult->resultCode != 0x00 ) {
        ((void)0) ;
    }
}

#include "context002.h"

#include "context003.h"
