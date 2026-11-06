#include "context000.h"

void native_host_arm7_main_027e83cc(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMSetMPParameterReq *req;
    WMMPParam *param;
    WMMPParam old_param;
    WMErrCode result;
    req = (WMSetMPParameterReq *)buf;
    param = &req->param;
    result = native_host_arm7_arm_027e8428(param, &old_param);
    {
        WMSetMPParameterCallback *cb = (WMSetMPParameterCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_SET_MP_PARAMETER;
        cb->errcode = result;
        cb->mask = param->mask;
        native_host_arm7_arm_037fe12c(&old_param, &cb->oldParam, sizeof(cb->oldParam));
        native_host_arm7_arm_038073a4(cb);
    }
}

#include "context001.h"
