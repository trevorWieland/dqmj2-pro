#include "context.h"
BOOL native_main_020a1608 (int resendPid)
{
    SBError sbError;
    int result;
    native_fn_020a3d70()->priorProfileID = 0;
    native_fn_020a3d70()->reqProfileID = 0;
    native_fn_020a3d70()->resvWaitCount = 0;
    native_fn_020a3d70()->cmdTimeoutStartTick = native_fn_02007a9c();
    if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
        native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_HOST);
        sbError = native_fn_0209fc38(0);
        if (native_fn_020a304c(sbError)) return FALSE;
    } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)   {
        result = native_fn_020a13d8(FALSE, FALSE, resendPid);
        if (native_fn_020a1258(result)) return FALSE;
    } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL)   {
        native_fn_0209f130(DWC_ERROR_NETWORK,
                          DWC_ECODE_SEQ_MATCH + DWC_ECODE_TYPE_OTHER);
        return FALSE;
    }
    return TRUE;
}
