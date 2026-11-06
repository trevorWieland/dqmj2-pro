#include "context.h"
s32 native_main_02089ef8(void* bssDesc, void* wepDesc, u32 option)
{
    OSIntrMode  e = native_fn_02007ff4();
    if (native_data_021cfcb4 == NULL)
    {
        WCMi_Warning(wcmWarningText_NotInit);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    switch (native_data_021cfcb4->phase)
    {
    case WCM_PHASE_IDLE:
        if (bssDesc == NULL)
        {
            WCMi_Warning(wcmWarningText_IllegalParam, "bssDesc");
            (void)native_fn_02008008(e);
            return WCM_RESULT_FAILURE;
        }
        if (((WMBssDesc*)bssDesc)->gameInfoLength > 0)
        {
            WCMi_Warning(wcmWarningText_IllegalParam, "bssDesc");
            (void)native_fn_02008008(e);
            return WCM_RESULT_FAILURE;
        }
        if (wepDesc != NULL)
        {
            if ((((WCMWepDesc*)wepDesc)->mode >= 4) || (((WCMWepDesc*)wepDesc)->keyId >= 4))
            {
                WCMi_Warning(wcmWarningText_IllegalParam, "wepDesc");
                (void)native_fn_02008008(e);
                return WCM_RESULT_FAILURE;
            }
            native_data_021cfcb4->wepDesc.mode = ((WCMWepDesc*)wepDesc)->mode;
            native_data_021cfcb4->wepDesc.keyId = ((WCMWepDesc*)wepDesc)->keyId;
            if (native_data_021cfcb4->wepDesc.mode == WCM_WEPMODE_NONE)
            {
                MI_CpuClear8(native_data_021cfcb4->wepDesc.key, WM_SIZE_WEPKEY);
            }
            else
            {
                native_fn_02008e0c(((WCMWepDesc*)wepDesc)->key, native_data_021cfcb4->wepDesc.key, WM_SIZE_WEPKEY);
            }
        }
        else
        {
            MI_CpuClear8(&(native_data_021cfcb4->wepDesc), sizeof(WCMWepDesc));
        }
        native_fn_02008e0c(bssDesc, &(native_data_021cfcb4->bssDesc), sizeof(WMBssDesc));
#if 0
        {
            int     i;
            u8*     pDump = (u8 *) (&(native_data_021cfcb4->bssDesc));
            for (i = 0; i < 192; i++)
            {
                if (i % 16)
                {
                    OS_TPrintf(" ");
                }
                OS_TPrintf("%02X", pDump[i]);
                if ((i % 16) == 15)
                {
                    OS_TPrintf("\n");
                }
            }
        }
#endif
        native_data_021cfcb4->bssDesc.rateSet.support = (u16) (WCM_ADDITIONAL_RATESET | native_data_021cfcb4->bssDesc.rateSet.basic);
        (void)native_fn_0208a28c(option);
        break;
    case WCM_PHASE_IDLE_TO_DCF:
        (void)native_fn_02008008(e);
        return WCM_RESULT_PROGRESS;
    case WCM_PHASE_DCF:
        (void)native_fn_02008008(e);
        return WCM_RESULT_SUCCESS;
    default:
        WCMi_Warning(wcmWarningText_IllegalPhase, native_data_021cfcb4->phase);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    {
        WMErrCode   wmResult;
        wmResult = native_fn_02014200(native_fn_0208a730, 0xffff, WCM_CAM_LIFETIME, 0xffff, 0xffff);
        switch (wmResult)
        {
        case WM_ERRCODE_OPERATING:
            native_fn_0208a5ac(WCM_PHASE_IDLE_TO_DCF);
            native_data_021cfcb4->notifyId = WCM_NOTIFY_CONNECT;
            break;
        case WM_ERRCODE_FIFO_ERROR:
            WCMi_Printf(wcmReportText_WmSyncError, "native_fn_02014200", wmResult);
            (void)native_fn_02008008(e);
            return WCM_RESULT_REJECT;
        case WM_ERRCODE_ILLEGAL_STATE:
            WCMi_Warning(wcmWarningText_InvalidWmState);
        default:
            native_fn_0208a5ac(WCM_PHASE_FATAL_ERROR);
            (void)native_fn_02008008(e);
            return WCM_RESULT_FATAL_ERROR;
        }
    }
    (void)native_fn_02008008(e);
    return WCM_RESULT_ACCEPT;
}
