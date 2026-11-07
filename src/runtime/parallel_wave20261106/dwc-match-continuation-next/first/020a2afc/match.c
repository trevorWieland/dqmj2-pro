#include "context.h"
u8 native_main_020a2afc (void)
{
    u8 i;
    int j;

    for (i = 0; i < DWC_MAX_CONNECTIONS; i++) {
        for (j = 0; j <= DWCi_GetMatchCnt()->qr2NNFinishCount; j++) {
            if (DWCi_GetMatchCnt()->aidList[j] == i) break;
        }
        if (j > DWCi_GetMatchCnt()->qr2NNFinishCount) break;
    }

    return i;
}
