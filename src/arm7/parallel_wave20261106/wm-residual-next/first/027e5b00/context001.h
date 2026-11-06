static void WmspError(u16 wlCommand, u16 wlResult)
{
    WMgetWirelessCounterCallback *cb;
    cb = (WMgetWirelessCounterCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_GET_W_COUNTER;
    cb->errcode = WM_ERRCODE_FAILED;
    cb->wlCmdID = wlCommand;
    cb->wlResult = wlResult;
    native_host_arm7_arm_038073a4((void *)cb);
}
