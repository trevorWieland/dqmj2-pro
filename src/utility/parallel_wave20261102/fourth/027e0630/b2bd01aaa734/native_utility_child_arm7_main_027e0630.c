#include "dependency000.h"

void native_utility_child_arm7_main_027e0630(PXIFifoTag tag, u32 data, BOOL err)
{
    BOOL result;
    if (err) {
        return;
    }
    ((void)0) ;
    result = native_utility_child_arm7_arm_037fcccc(&(native_utility_child_arm7_data_027f84f0.requestQ), (OSMessage)data, 0 );
    if (!result) {
        if (native_utility_child_arm7_data_027f84f0.wm7buf != ((void *)0) ) {
            WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = *((u16 *)data);
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->wlCmdID = 0;
            cb->wlResult = 0;
            native_utility_child_arm7_arm_038057c8((void *)cb);
        }
    }
}
