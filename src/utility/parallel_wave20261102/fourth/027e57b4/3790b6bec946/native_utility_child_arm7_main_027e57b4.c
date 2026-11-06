#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e57b4(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WMDcfRecvBuf *recvBuf;
    u16 recvSize;
    OSIntrMode e;
    recvBuf = (WMDcfRecvBuf *)buf[1];
    recvSize = (u16)buf[2];
    e = native_utility_child_arm7_arm_037fe41c();
    status->dcf_recvBuf[0] = recvBuf;
    status->dcf_recvBufSize = recvSize;
    status->dcf_recvBuf[1] = (WMDcfRecvBuf *)((u32)recvBuf + (u32)recvSize);
    status->dcf_recvBufSel = 0;
    status->dcf_sendData = ((void *)0) ;
    status->dcf_sendSize = 0;
    status->dcf_sendFlag = 0 ;
    status->state = WM_STATE_DCF_CHILD;
    {
        WMStartDCFCallback *cb = (WMStartDCFCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_START_DCF;
        cb->errcode = WM_ERRCODE_SUCCESS;
        cb->state = WM_STATECODE_DCF_START;
        native_utility_child_arm7_arm_038057c8((void *)cb);
    }
    status->dcf_flag = 1 ;
    (void)native_utility_child_arm7_arm_037fe430(e);
}
