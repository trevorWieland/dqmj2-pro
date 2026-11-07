#include "context.h"
u8 native_main_020a2c38 (int profileID, BOOL idx0)
{
    int i;

    for (i = (idx0 ? 0 : 1); i <= DWCi_GetMatchCnt()->gt2NumConnection; i++) {
        if (DWCi_GetMatchCnt()->sbPidList[i] == profileID)
            return DWCi_GetMatchCnt()->aidList[i];
    }

    return 0xff;
}
