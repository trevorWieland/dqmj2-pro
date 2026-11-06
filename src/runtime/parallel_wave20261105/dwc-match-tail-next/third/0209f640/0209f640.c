#include "context.h"
void native_main_0209f640 (void)
{
    int count = -1;
    int i;
    for (i = 0; i < DWC_MAX_CONNECTIONS; i++) {
        if (native_fn_020a3d70()->validAidBitmap & (1u << i))
            count++;
    }
    if (count == -1) native_fn_020a3d70()->gt2NumValidConn = 0;
    else native_fn_020a3d70()->gt2NumValidConn = (u8)count;
}
