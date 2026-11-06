static void WmspError(u16 wmApiID, u16 wlCommand, u16 wlResult)
{
    WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = wmApiID;
    callback->errcode = WM_ERRCODE_FAILED;
    callback->wlCmdID = wlCommand;
    callback->wlResult = wlResult;
    native_host_arm7_arm_038073a4(callback);
}
