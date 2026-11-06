#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e58bc(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    u16 ccaMode;
    u16 edThreshold;
    u16 measureTime;
    u16 channel;
    u8 channelList[16 ];
    u16 current_state;
    WlMlmeMeasureChannelCfm *pConfirm;
    if (status->state != WM_STATE_IDLE) {
        WMMeasureChannelCallback *callback = (WMMeasureChannelCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_MEASURE_CHANNEL;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    {
        WlDevGetStationStateCfm *p_confirm;
        p_confirm = native_host_arm7_arm_027e2924(buf);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e5a64((0x0300 | 0x08) , p_confirm->resultCode);
            return;
        }
        current_state = p_confirm->state;
    }
    status->mode = 2 ;
    if (current_state == 0x10 ) {
        if (!native_host_arm7_arm_027e03d0(WM_APIID_START_SCAN, buf)) {
            return;
        }
        {
            WlDevClass1Cfm *p_confirm;
            p_confirm = native_host_arm7_arm_027e28b0(buf);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e5a64((0x0300 | 0x03) , p_confirm->resultCode);
                return;
            }
        }
        status->state = WM_STATE_CLASS1;
        {
            WlMlmePowerManagementCfm *p_confirm;
            u16 pwrMgtMode;
            u16 wakeUp;
            u16 recieveDtims;
            pwrMgtMode = 1 ;
            wakeUp = 0 ;
            recieveDtims = 1 ;
            p_confirm = native_host_arm7_arm_027e1dbc(buf, pwrMgtMode, wakeUp, recieveDtims);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e5a64((0x0000 | 0x01) , p_confirm->resultCode);
                return;
            }
            status->pwrMgtMode = pwrMgtMode;
        }
        current_state = 0x20 ;
    }
    {
        WMMeasureChannelReq *args = (WMMeasureChannelReq *)msg;
        ccaMode = args->ccaMode;
        edThreshold = args->edThreshold;
        channel = args->channel;
        measureTime = args->measureTime;
        native_host_arm7_arm_037fe070(channelList, 0x00, 16 );
        MI_WriteByte(&channelList[0], (u8)channel);
    }
    {
        pConfirm = native_host_arm7_arm_027e2180(buf, ccaMode, edThreshold, measureTime, channelList);
        if (pConfirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e5a64((0x0000 | 0x0A) , pConfirm->resultCode);
            return;
        }
    }
    {
        u16 cb_channel;
        u16 cb_ccaBusyRatio;
        WMMeasureChannelCallback *cb;
        cb_channel = (u16)(pConfirm->ccaBusyInfo[0] & 0x00ff);
        cb_ccaBusyRatio = (u16)(pConfirm->ccaBusyInfo[0] >> 8);
        {
            WlDevIdleCfm *p_confirm = native_host_arm7_arm_027e2898(buf);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e5a64((0x0300 | 0x02) , p_confirm->resultCode);
                return;
            }
        }
        status->state = WM_STATE_IDLE;
        cb = (WMMeasureChannelCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_MEASURE_CHANNEL;
        cb->errcode = WM_ERRCODE_SUCCESS;
        cb->channel = cb_channel;
        cb->ccaBusyRatio = cb_ccaBusyRatio;
        native_host_arm7_arm_038073a4((void *)cb);
    }
    return;
}
#include "dependency002.h"
