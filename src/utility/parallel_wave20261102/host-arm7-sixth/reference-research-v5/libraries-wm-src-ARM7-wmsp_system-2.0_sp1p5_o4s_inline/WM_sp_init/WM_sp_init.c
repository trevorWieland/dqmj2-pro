#include "context000.h"

#include "context001.h"

void WM_sp_init(WlInit *wlInit, WmInit *wmInit)
{
    wmspW.dmaNo = wmInit->dmaNo;
    wmspW.arenaId = wlInit->heapFunc.os.id;
    wmspW.heapHandle = wlInit->heapFunc.os.heapHandle;
    wmspW.wm7buf = ((void *)0) ;
    wmspW.status = ((void *)0) ;
    OS_InitMessageQueue(&(wmspW.toWLmsgQ), wmspW.toWLmsg, 2 );
    OS_InitMessageQueue(&(wmspW.fromWLmsgQ), wmspW.fromWLmsg, 4 );
    OS_InitMessageQueue(&(wmspW.confirmQ), wmspW.confirm, 4 );
    OS_InitMessageQueue(&(wmspW.requestQ), wmspW.request, 32 );
    wlInit->sendMsgQueuep = &(wmspW.toWLmsgQ);
    wlInit->recvMsgQueuep = &(wmspW.fromWLmsgQ);
    wmspW.indPrio_high = wmInit->indPrio_high;
    wmspW.wlPrio_high = wmInit->wlPrio_high;
    wmspW.reqPrio_high = wmInit->reqPrio_high;
    wmspW.indPrio_low = wmInit->indPrio_low;
    wmspW.wlPrio_low = wmInit->wlPrio_low;
    wmspW.reqPrio_low = wmInit->reqPrio_low;
    OS_InitMutex(&(wmspW.fifoExclusive));
    OS_CreateThread(
        &wmspIndicateThread,
        WMSP_IndicateThread,
        ((void *)0) ,
        (void *)(wmspW.indicateStack + (1024 / sizeof(u32))),
        1024 ,
        wmInit->indPrio_low
    );
    OS_WakeupThreadDirect(&wmspIndicateThread);
    OS_CreateThread(
        &wmspRequestThread,
        WMSP_RequestThread,
        ((void *)0) ,
        (void *)(wmspW.requestStack + (4096 / sizeof(u32))),
        4096 ,
        wmInit->reqPrio_low
    );
    OS_WakeupThreadDirect(&wmspRequestThread);
    {
        s32 i;
        for (i = 0; i < 32 ; i++) {
            wmspW.rssiHistory[i] = 0;
        }
        wmspW.rssiIndex = 0;
    }
    if (!OS_IsVAlarmAvailable()) {
        OS_InitVAlarm();
    }
    PXI_Init();
    PXI_SetFifoRecvCallback(PXI_FIFO_TAG_WM, WmspPxiCallback);
    wlInit->dmaChannel = 2 ;
    wlInit->priority = wmInit->wlPrio_low;
    (void)WL_InitDriver(wlInit);
}

#include "context002.h"
