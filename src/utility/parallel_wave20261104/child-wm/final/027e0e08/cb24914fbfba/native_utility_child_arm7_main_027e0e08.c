#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e0e08(WlCmdReq *req)
{
    WlMaFatalErrInd *pInd = (WlMaFatalErrInd *)req;
    u32 *buf;
    BOOL result;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    ((void)0) ;
    if (status->mp_ignoreFatalErrorMode == 1 && pInd->errCode == 0x20) {
        ((void)0) ;
        {
            OSIntrMode enabled;
            enabled = native_utility_child_arm7_arm_037fe41c();
            WmspCancelMPAckAlarm();
            status->mp_waitAckFlag = 0 ;
            (void)native_utility_child_arm7_arm_037fe430(enabled);
            status->mp_setDataFlag = 0 ;
            (void)native_utility_child_arm7_arm_027e7018(1 , 0x0000);
        }
        {
            WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_SUCCESS;
            cb->state = WM_STATECODE_INFORMATION;
            cb->reason = WM_INFOCODE_FATAL_ERROR;
            native_utility_child_arm7_arm_038057c8(cb);
        }
    } else {
        buf = native_utility_child_arm7_arm_027e0134();
        if (buf == ((void *)0) ) {
            result = 0 ;
        } else {
            buf[0] = WM_APIID_AUTO_DISCONNECT;
            buf[2] = WM_DISCONNECT_REASON_FATAL_ERROR;
            if (WMSPi_IsParent(status->state)) {
                buf[1] = 0x7ffe;
            } else if (WMSPi_IsChild(status->state)) {
                buf[1] = 0x0001;
            }
            ((void)0) ;
            result = native_utility_child_arm7_arm_037fcccc(&(WMSP_GetSystemWork()->requestQ),
                (OSMessage)buf,
                0 );
        }
        if (!result) {
            WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_AUTO_DISCONNECT;
            native_utility_child_arm7_arm_038057c8(cb);
        }
    }
}
