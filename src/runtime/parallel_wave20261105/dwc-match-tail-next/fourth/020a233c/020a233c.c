#include "context.h"
BOOL native_main_020a233c (int profileID)
{
    BOOL ret;
    GT2Connection * connection;
    native_fn_020a3d70()->cbEventPid = profileID;
    connection = native_fn_0209bdc4(profileID, native_fn_020a3d70()->gt2NumConnection + 1);
    if (connection) {
        native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_TIMEOUT;
        native_fn_020b4528(*connection);
        native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_INIT;
        ret = TRUE;
    } else {
        (void)native_fn_0209f47c(profileID, native_fn_020a3d70()->gt2NumConnection + 1);
        ret = FALSE;
    }
    return ret;
}
