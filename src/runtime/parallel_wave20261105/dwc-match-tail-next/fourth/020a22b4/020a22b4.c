#include "context.h"
int native_main_020a22b4 (void)
{
    SBError sbError;
    int result;
    native_fn_020a3d70()->qr2IsReserved = 0;
    native_fn_020a3d70()->qr2Reservation = 0;
    native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_INIT;
    if (native_fn_020a3d70()->priorProfileID) {
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_HOST);
            sbError = native_fn_0209fc38(0);
            if (native_fn_020a304c(sbError)) return sbError;
        } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)   {
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_WAIT_RESV);
            result = native_fn_020a1278(native_fn_020a3d70()->priorProfileID, FALSE);
            if (native_fn_020a1258(result)) return result;
        }
    } else {
        native_fn_020a21e0(DWC_MATCH_RESET_RESTART);
    }
    return 0;
}
