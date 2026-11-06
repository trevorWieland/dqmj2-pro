#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0f40(WlCmdReq *req)
{
    WMStartDCFCallback *callback;
    WlMaDataInd *pInd = (WlMaDataInd *)req;
    WMStatus *status = WMSP_GetStatusStructure();
    WlRxFrame *pFrame;
    WMDcfRecvBuf *bufp;
    if (status->dcf_flag == 0 ) {
        return;
    }
    {
        WMSPWork *pw = WMSP_GetSystemWork();
        native_utility_child_arm7_arm_027e0374(WMSP_GetRssi8(pInd->frame.rssi));
        status->linkLevel = native_utility_child_arm7_arm_027e0300();
    }
    pFrame = (WlRxFrame *)&pInd->frame;
    if (1 == native_utility_child_arm7_arm_027e05b4((u8 *)(pFrame->srcAdrs))) {
        return;
    }
    if (pFrame->length > 1508 ) {
        return;
    }
    status->dcf_recvBufSel ^= 1;
    bufp = status->dcf_recvBuf[status->dcf_recvBufSel];
    native_utility_child_arm7_arm_037fe814(pFrame,
        bufp,
        (pFrame->length + 44 + 1U) & ~1U
    );
    native_utility_child_arm7_arm_037fe814(pFrame->destAdrs, bufp->destAdrs, 6 );
    native_utility_child_arm7_arm_037fe814(pFrame->srcAdrs, bufp->srcAdrs, 6 );
    callback = (WMStartDCFCallback *)native_utility_child_arm7_arm_0380576c();
    callback->apiid = WM_APIID_START_DCF;
    callback->errcode = WM_ERRCODE_SUCCESS;
    callback->state = WM_STATECODE_DCF_IND;
    callback->recvBuf = bufp;
    native_utility_child_arm7_arm_038057c8(callback);
}
