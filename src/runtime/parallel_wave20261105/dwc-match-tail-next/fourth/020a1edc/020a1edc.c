#include "context.h"
BOOL native_main_020a1edc (const u32 pidList[], u32 pidListLen)
{
    int i;
    if (native_fn_020a3d70()->distantFriend &&
        (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAIT_RESV))
        return TRUE;
    for (i = 0; i < pidListLen; i++) {
#ifdef DWC_LIMIT_FRIENDS_MATCH_VALID
        if (!native_fn_020a2b44((int)pidList[i])) return FALSE;
#else
        if (!gpIsBuddy(native_fn_020a3d70()->pGpObj, (int)pidList[i])) return FALSE;
#endif
        if (native_fn_020a3d70()->distantFriend &&
            (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAITING)) {
            return TRUE;
        }
    }
    return TRUE;
}
