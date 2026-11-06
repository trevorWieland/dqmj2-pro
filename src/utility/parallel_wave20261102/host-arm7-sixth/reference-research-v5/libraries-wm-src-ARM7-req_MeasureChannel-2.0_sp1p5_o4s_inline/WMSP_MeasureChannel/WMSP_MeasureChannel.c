#include "context000.h"

#include "context001.h"

void WMSP_MeasureChannel(OSMessage msg)
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
        WMMeasureChannelCallback *callback = (WMMeasureChannelCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_MEASURE_CHANNEL;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    {
        WlDevGetStationStateCfm *p_confirm;
        p_confirm = WMSP_WL_DevGetStationState(buf);
        if (p_confirm->resultCode != 0x00 ) {
            WmspError((0x0300 | 0x08) , p_confirm->resultCode);
            return;
        }
        current_state = p_confirm->state;
    }
    status->mode = 2 ;
    if (current_state == 0x10 ) {
        if (!WMSP_SetAllParams(WM_APIID_START_SCAN, buf)) {
            return;
        }
        {
            WlDevClass1Cfm *p_confirm;
            p_confirm = WMSP_WL_DevClass1(buf);
            if (p_confirm->resultCode != 0x00 ) {
                WmspError((0x0300 | 0x03) , p_confirm->resultCode);
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
            p_confirm = WMSP_WL_MlmePowerManagement(buf, pwrMgtMode, wakeUp, recieveDtims);
            if (p_confirm->resultCode != 0x00 ) {
                WmspError((0x0000 | 0x01) , p_confirm->resultCode);
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
        MI_CpuFill8(channelList, 0x00, 16 );
        MI_WriteByte(&channelList[0], (u8)channel);
    }
    {
        pConfirm = WMSP_WL_MlmeMeasureChannel(buf, ccaMode, edThreshold, measureTime, channelList);
        if (pConfirm->resultCode != 0x00 ) {
            WmspError((0x0000 | 0x0A) , pConfirm->resultCode);
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
            WlDevIdleCfm *p_confirm = WMSP_WL_DevIdle(buf);
            if (p_confirm->resultCode != 0x00 ) {
                WmspError((0x0300 | 0x02) , p_confirm->resultCode);
                return;
            }
        }
        status->state = WM_STATE_IDLE;
        cb = (WMMeasureChannelCallback *)WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_MEASURE_CHANNEL;
        cb->errcode = WM_ERRCODE_SUCCESS;
        cb->channel = cb_channel;
        cb->ccaBusyRatio = cb_ccaBusyRatio;
        WMSP_ReturnResult2Wm9((void *)cb);
    }
    return;
}

#include "context002.h"
