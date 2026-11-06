#include "context.h"
void native_main_0208a698(void)
{
    WMErrCode   wmResult;
    if (native_data_021cfcb4->resetting == WCM_RESETTING_OFF)
    {
        native_data_021cfcb4->resetting = WCM_RESETTING_ON;
        wmResult = native_fn_020127ec(native_fn_0208af1c);
        if (wmResult != WM_ERRCODE_OPERATING)
        {
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_020127ec", wmResult);
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            native_fn_0208a550(WCM_RESULT_FATAL_ERROR, 0, 0, 1552);
        }
    }
}
