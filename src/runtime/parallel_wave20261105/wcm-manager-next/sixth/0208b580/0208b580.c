#include "context.h"
s32 native_main_0208b580 (const u8 * dstAddr, const u8 * header, s32 headerLen, const u8 * body, s32 bodyLen)
{
    OSIntrMode e = native_fn_02007ff4();
    volatile WCMWork * w = native_fn_0208a31c();
    if (w == NULL) {
        WCMi_Warning(cpsifWarningText_NotInit);
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_BEFORE_INIT;
    }
#if WCM_DEBUG
    if ((dstAddr == NULL) || (header == NULL)) {
        WCMi_Warning(cpsifWarningText_IllegalParam, "dstAddr or header");
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_ILLEGAL_PARAM;
    }
    if (headerLen <= 0 || (body != NULL && bodyLen < 0) || (body == NULL && bodyLen != 0)) {
        WCMi_Warning(cpsifWarningText_IllegalParam, "headerLen or bodyLen");
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_ILLEGAL_PARAM;
    }
    if (headerLen + bodyLen > WCM_ROUNDUP32(WM_DCF_MAX_SIZE)) {
        WCMi_Warning(cpsifWarningText_IllegalParam, "headerLen + bodyLen");
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_ILLEGAL_PARAM;
    }
    if ((u32) header & 0x01 || ((body != NULL) && ((u32) body & 0x01))) {
        WCMi_Warning(cpsifWarningText_IllegalParam, "header or body");
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_ILLEGAL_PARAM;
    }
    if (OS_GetProcMode() == HW_PSR_IRQ_MODE) {
        WCMi_Warning(cpsifWarningText_InIrqMode);
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_IN_IRQ_MODE;
    }
#endif
    native_fn_0200708c(&(native_data_021cfcb8.sendMutex));
    w = native_fn_0208a31c();
    if (w == NULL) {
        native_fn_02007110(&(native_data_021cfcb8.sendMutex));
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_BEFORE_INIT;
    }
    if ((w->phase != WCM_PHASE_DCF) || (w->resetting == WCM_RESETTING_ON)) {
        native_fn_02007110(&(native_data_021cfcb8.sendMutex));
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_NO_CONNECTION;
    }
    native_fn_02008e0c(header, (void *)(w->sendBuf), (u32) headerLen);
    if (bodyLen > 0) {
        native_fn_02008e0c(body, (void *)(((u8 *)w->sendBuf) + headerLen), (u32) bodyLen);
    }
    {
        WMErrCode wmResult;
        wmResult = native_fn_02013328(native_fn_0208b6a8, (const u8 *)dstAddr, (const u16 *)(w->sendBuf), (u16) (headerLen + bodyLen));
        switch (wmResult) {
        case WM_ERRCODE_OPERATING:
            break;
        case WM_ERRCODE_ILLEGAL_STATE:
        case WM_ERRCODE_INVALID_PARAM:
        case WM_ERRCODE_FIFO_ERROR:
        default:
            WCMi_Printf(cpsifReportText_WmSyncError, "native_fn_02013328", wmResult);
            native_fn_02007110(&(native_data_021cfcb8.sendMutex));
            (void)native_fn_02008008(e);
            return WCM_CPSIF_RESULT_SEND_FAILURE;
        }
    }
    native_fn_020068d4(&(native_data_021cfcb8.sendQ));
    switch (native_data_021cfcb8.sendResult) {
    case WM_ERRCODE_SUCCESS:
        break;
    case WM_ERRCODE_FAILED:
    default:
        WCMi_Printf(cpsifReportText_WmAsyncError, "WCM_SendDCFData", native_data_021cfcb8.sendResult);
        native_fn_02007110(&(native_data_021cfcb8.sendMutex));
        (void)native_fn_02008008(e);
        return WCM_CPSIF_RESULT_SEND_FAILURE;
    }
    native_fn_02007110(&(native_data_021cfcb8.sendMutex));
    (void)native_fn_02008008(e);
    return headerLen + bodyLen;
}
