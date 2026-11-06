#include "context.h"
void native_main_0208a3e0(void* bssid, void* essid, u32 option)
{
    (void)native_fn_0208a28c(option);
    native_data_021cfcb4->scanExParam.scanBuf = (WMBssDesc*)native_data_021cfcb4->recvBuf;
    native_data_021cfcb4->scanExParam.scanBufSize = WM_SIZE_SCAN_EX_BUF;
    native_data_021cfcb4->scanExParam.channelList = (u16) ((0x0001 << native_fn_0208a508(0)) >> 1);
    native_data_021cfcb4->scanExParam.maxChannelTime = ((native_data_021cfcb4->maxScanTime != 0) ? native_data_021cfcb4->maxScanTime : native_fn_020123d0());
    native_data_021cfcb4->scanExParam.scanType = (u16) (((native_data_021cfcb4->option & WCM_OPTION_MASK_SCANTYPE) == WCM_OPTION_SCANTYPE_ACTIVE) ? WM_SCANTYPE_ACTIVE : WM_SCANTYPE_PASSIVE);
    if (bssid == NULL)
    {
        native_fn_02008e0c(native_data_020dc3c8, native_data_021cfcb4->scanExParam.bssid, WCM_BSSID_SIZE);
    }
    else
    {
        native_fn_02008e0c(bssid, native_data_021cfcb4->scanExParam.bssid, WCM_BSSID_SIZE);
    }
    if ((essid == NULL) || (essid == (void*)native_data_020dc3d0))
    {
        native_fn_02008e0c(native_data_020dc3d0, native_data_021cfcb4->scanExParam.ssid, WCM_ESSID_SIZE);
        native_data_021cfcb4->scanExParam.ssidLength = 0;
    }
    else
    {
        s32 len;
        native_fn_02008e0c(essid, native_data_021cfcb4->scanExParam.ssid, WCM_ESSID_SIZE);
        for (len = 0; len < WCM_ESSID_SIZE; len++)
        {
            if (((u8*)essid)[len] == '\0')
            {
                break;
            }
        }
        native_data_021cfcb4->scanExParam.ssidLength = (u16) len;
    }
    native_data_021cfcb4->scanCount = 0;
}
