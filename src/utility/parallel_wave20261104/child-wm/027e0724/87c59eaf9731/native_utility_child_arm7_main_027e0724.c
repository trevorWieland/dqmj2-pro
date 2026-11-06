#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0724(WlInit *wlInit, WmInit *wmInit)
{
    native_utility_child_arm7_data_027f84f0.dmaNo = wmInit->dmaNo;
    native_utility_child_arm7_data_027f84f0.arenaId = wlInit->heapFunc.os.id;
    native_utility_child_arm7_data_027f84f0.heapHandle = wlInit->heapFunc.os.heapHandle;
    native_utility_child_arm7_data_027f84f0.wm7buf = ((void *)0) ;
    native_utility_child_arm7_data_027f84f0.status = ((void *)0) ;
    native_utility_child_arm7_arm_037fcd60(&(native_utility_child_arm7_data_027f84f0.toWLmsgQ), native_utility_child_arm7_data_027f84f0.toWLmsg, 2 );
    native_utility_child_arm7_arm_037fcd60(&(native_utility_child_arm7_data_027f84f0.fromWLmsgQ), native_utility_child_arm7_data_027f84f0.fromWLmsg, 4 );
    native_utility_child_arm7_arm_037fcd60(&(native_utility_child_arm7_data_027f84f0.confirmQ), native_utility_child_arm7_data_027f84f0.confirm, 4 );
    native_utility_child_arm7_arm_037fcd60(&(native_utility_child_arm7_data_027f84f0.requestQ), native_utility_child_arm7_data_027f84f0.request, 32 );
    wlInit->sendMsgQueuep = &(native_utility_child_arm7_data_027f84f0.toWLmsgQ);
    wlInit->recvMsgQueuep = &(native_utility_child_arm7_data_027f84f0.fromWLmsgQ);
    native_utility_child_arm7_data_027f84f0.indPrio_high = wmInit->indPrio_high;
    native_utility_child_arm7_data_027f84f0.wlPrio_high = wmInit->wlPrio_high;
    native_utility_child_arm7_data_027f84f0.reqPrio_high = wmInit->reqPrio_high;
    native_utility_child_arm7_data_027f84f0.indPrio_low = wmInit->indPrio_low;
    native_utility_child_arm7_data_027f84f0.wlPrio_low = wmInit->wlPrio_low;
    native_utility_child_arm7_data_027f84f0.reqPrio_low = wmInit->reqPrio_low;
    native_utility_child_arm7_arm_037fcf10(&(native_utility_child_arm7_data_027f84f0.fifoExclusive));
    native_utility_child_arm7_arm_037fc5ec(
        &native_utility_child_arm7_data_0380926c,
        native_utility_child_arm7_arm_027e1fb8,
        ((void *)0) ,
        (void *)(native_utility_child_arm7_data_027f84f0.indicateStack + (1024 / sizeof(u32))),
        1024 ,
        wmInit->indPrio_low
    );
    native_utility_child_arm7_arm_037fc3ac(&native_utility_child_arm7_data_0380926c);
    native_utility_child_arm7_arm_037fc5ec(
        &native_utility_child_arm7_data_038091c8,
        native_utility_child_arm7_arm_027e2058,
        ((void *)0) ,
        (void *)(native_utility_child_arm7_data_027f84f0.requestStack + (4096 / sizeof(u32))),
        4096 ,
        wmInit->reqPrio_low
    );
    native_utility_child_arm7_arm_037fc3ac(&native_utility_child_arm7_data_038091c8);
    {
        s32 i;
        for (i = 0; i < 32 ; i++) {
            native_utility_child_arm7_data_027f84f0.rssiHistory[i] = 0;
        }
        native_utility_child_arm7_data_027f84f0.rssiIndex = 0;
    }
    if (!native_utility_child_arm7_arm_037fe390()) {
        native_utility_child_arm7_arm_037fe3a0();
    }
    native_utility_child_arm7_arm_037fcf64();
    native_utility_child_arm7_arm_037fe5d4(PXI_FIFO_TAG_WM, native_utility_child_arm7_arm_027e0630);
    wlInit->dmaChannel = 2 ;
    wlInit->priority = wmInit->wlPrio_low;
    (void)native_utility_child_arm7_arm_027e8b78(wlInit);
}
#include "dependency002.h"
