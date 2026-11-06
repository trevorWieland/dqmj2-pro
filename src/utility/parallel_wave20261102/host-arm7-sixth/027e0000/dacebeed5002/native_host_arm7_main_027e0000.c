#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e0000(WlInit *wlInit, WmInit *wmInit)
{
    native_host_arm7_data_027f7884.dmaNo = wmInit->dmaNo;
    native_host_arm7_data_027f7884.arenaId = wlInit->heapFunc.os.id;
    native_host_arm7_data_027f7884.heapHandle = wlInit->heapFunc.os.heapHandle;
    native_host_arm7_data_027f7884.wm7buf = ((void *)0) ;
    native_host_arm7_data_027f7884.status = ((void *)0) ;
    native_host_arm7_arm_037fc6ac(&(native_host_arm7_data_027f7884.toWLmsgQ), native_host_arm7_data_027f7884.toWLmsg, 2 );
    native_host_arm7_arm_037fc6ac(&(native_host_arm7_data_027f7884.fromWLmsgQ), native_host_arm7_data_027f7884.fromWLmsg, 4 );
    native_host_arm7_arm_037fc6ac(&(native_host_arm7_data_027f7884.confirmQ), native_host_arm7_data_027f7884.confirm, 4 );
    native_host_arm7_arm_037fc6ac(&(native_host_arm7_data_027f7884.requestQ), native_host_arm7_data_027f7884.request, 32 );
    wlInit->sendMsgQueuep = &(native_host_arm7_data_027f7884.toWLmsgQ);
    wlInit->recvMsgQueuep = &(native_host_arm7_data_027f7884.fromWLmsgQ);
    native_host_arm7_data_027f7884.indPrio_high = wmInit->indPrio_high;
    native_host_arm7_data_027f7884.wlPrio_high = wmInit->wlPrio_high;
    native_host_arm7_data_027f7884.reqPrio_high = wmInit->reqPrio_high;
    native_host_arm7_data_027f7884.indPrio_low = wmInit->indPrio_low;
    native_host_arm7_data_027f7884.wlPrio_low = wmInit->wlPrio_low;
    native_host_arm7_data_027f7884.reqPrio_low = wmInit->reqPrio_low;
    native_host_arm7_arm_037fc870(&(native_host_arm7_data_027f7884.fifoExclusive));
    native_host_arm7_arm_037fc054(
        &native_host_arm7_data_0380b3c0,
        native_host_arm7_data_027e0898,
        ((void *)0) ,
        (void *)(native_host_arm7_data_027f7884.indicateStack + (1024 / sizeof(u32))),
        1024 ,
        wmInit->indPrio_low
    );
    native_host_arm7_arm_037fc36c(&native_host_arm7_data_0380b3c0);
    native_host_arm7_arm_037fc054(
        &native_host_arm7_data_0380b31c,
        native_host_arm7_data_027e1cc0,
        ((void *)0) ,
        (void *)(native_host_arm7_data_027f7884.requestStack + (4096 / sizeof(u32))),
        4096 ,
        wmInit->reqPrio_low
    );
    native_host_arm7_arm_037fc36c(&native_host_arm7_data_0380b31c);
    {
        s32 i;
        for (i = 0; i < 32 ; i++) {
            native_host_arm7_data_027f7884.rssiHistory[i] = 0;
        }
        native_host_arm7_data_027f7884.rssiIndex = 0;
    }
    if (!native_host_arm7_arm_037fd798()) {
        native_host_arm7_arm_037fd74c();
    }
    native_host_arm7_arm_037fe2b4();
    native_host_arm7_arm_037fe39c(PXI_FIFO_TAG_WM, native_host_arm7_arm_027e0244);
    wlInit->dmaChannel = 2 ;
    wlInit->priority = wmInit->wlPrio_low;
    (void)native_host_arm7_arm_027e89ec(wlInit);
}
#include "dependency002.h"
