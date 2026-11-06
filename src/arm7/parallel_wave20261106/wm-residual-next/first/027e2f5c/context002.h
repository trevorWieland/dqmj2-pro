static void WmspError(u16 wlCommand, u16 wlResult)
{
    WMCallback *cb;
    cb = (WMCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_SET_P_PARAM;
    cb->errcode = WM_ERRCODE_FAILED;
    cb->wlCmdID = wlCommand;
    cb->wlResult = wlResult;
    native_host_arm7_arm_038073a4((void *)cb);
}
