#include "context.h"
u32 native_main_020a2c80 (BOOL valid)
{
    u32 bitmask = 0;
    int i;

    if (valid) {
        return (DWCi_GetMatchCnt()->validAidBitmap & ~1);
    } else {
        for (i = 1; i <= DWCi_GetMatchCnt()->gt2NumConnection; i++) {
            bitmask |= 1U << DWCi_GetMatchCnt()->aidList[i];
        }

        return bitmask;
    }
}
