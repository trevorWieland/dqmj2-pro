#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e0244(PXIFifoTag tag, u32 data, BOOL err)
{
    BOOL result;
    if (err) {
        return;
    }
    ((void)0) ;
    result = native_host_arm7_arm_037fc6d4(&(native_host_arm7_data_027f7884.requestQ), (OSMessage)data, 0 );
    if (!result) {
        if (native_host_arm7_data_027f7884.wm7buf != ((void *)0) ) {
            WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = *((u16 *)data);
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->wlCmdID = 0;
            cb->wlResult = 0;
            native_host_arm7_arm_038073a4((void *)cb);
        }
    }
}
