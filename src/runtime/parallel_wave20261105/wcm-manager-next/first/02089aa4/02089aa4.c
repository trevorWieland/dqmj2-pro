#include "context.h"
s32 native_main_02089aa4(void* buf, s32 len)
{
    OSIntrMode  e = native_fn_02007ff4();
    SDK_ASSERT_ON_COMPILE(sizeof(WCMWork) <= WCM_WORK_SIZE);
    if (native_data_021cfcb4 != NULL)
    {
        WCMi_Warning(wcmWarningText_AlreadyInit);
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if (buf == NULL)
    {
        WCMi_Warning(wcmWarningText_IllegalParam, "buf");
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if ((u32) buf & 0x01f)
    {
        WCMi_Warning(wcmWarningText_IllegalParam, "buf");
        (void)native_fn_02008008(e);
        return WCM_RESULT_FAILURE;
    }
    if (len < sizeof(WCMWork))
    {
        WCMi_Warning(wcmWarningText_IllegalParam, "len");
        (void)native_fn_02008008(e);
        return WCM_RESULT_NOT_ENOUGH_MEM;
    }
    native_data_021cfcb4 = (WCMWork*)buf;
    native_data_021cfcb4->phase = WCM_PHASE_WAIT;
    native_data_021cfcb4->notifyId = WCM_NOTIFY_COMMON;
    native_data_021cfcb4->maxScanTime = 0;
    native_data_021cfcb4->apListLock = WCM_APLIST_UNLOCK;
    native_data_021cfcb4->resetting = WCM_RESETTING_OFF;
    native_data_021cfcb4->authId = 0;
    native_data_021cfcb4->wlStatusOnConnectFail = 0x0000;
    native_fn_0208a4f0();
    native_fn_0208b44c();
    if (!native_fn_02007a24())
    {
        native_fn_020079ac();
    }
    if (!native_fn_02007c58())
    {
        native_fn_02007bd8();
    }
    native_fn_02007c68(&(native_data_021cfcb4->keepAliveAlarm));
    (void)native_fn_02008008(e);
    return WCM_RESULT_SUCCESS;
}
