#include "context.h"
BOOL native_main_020a2b44 (int profileID)
{
    int listProfileID;
    int i;

    if (DWCi_GetMatchCnt()->friendList == NULL) return FALSE;

    for (i = 0; i < DWCi_GetMatchCnt()->friendIdxListLen; i++) {
        if (((listProfileID = DWCi_GetProfileIDFromList(DWCi_GetMatchCnt()->friendIdxList[i])) > 0) &&
            (listProfileID == profileID)) {

            return TRUE;
        }
    }

    return FALSE;
}
