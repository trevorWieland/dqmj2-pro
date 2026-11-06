#include "context.h"
void native_main_020a2290 (void)
{
    if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) ||
        (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL)) {
        DWC_Printf(DWC_REPORTFLAG_WARNING, "DWCi_RestartFromTimeout() shouldn't be called.\n");
        return;
    }
    native_fn_020a2394();
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "Closed all connections and restart matching.\n");
    native_fn_020a21e0(DWC_MATCH_RESET_RESTART);
}
