static BOOL IsIncludeValidSSID(WMBssDesc *bssDesc)
{
    s32 i;
    if (bssDesc->ssidLength == 0) {
        return 0 ;
    }
    if (bssDesc->ssidLength > 32 ) {
        return 0 ;
    }
    for (i = 0; i < bssDesc->ssidLength; i++) {
        if (bssDesc->ssid[i] != 0x00) {
            return 1 ;
        }
    }
    return 0 ;
}

static u32 WmspGetScanExBufSize4WL(u16 arm9_BufSize)
{
    u32 tempSize;
    tempSize = (u32)(arm9_BufSize - (((arm9_BufSize - (sizeof(WlBssDesc) - 4)) / (sizeof(WlBssDesc) - 2)) * 2));
    return (u32)(tempSize + (((sizeof(WlMlmeScanReq) + 1) / 2) * 2) + (((sizeof(WlCmdHeader) + 1) / 2) * 2) + 6);
}

void native_host_arm7_arm_027e3d80(u16 wlCommand, u16 wlResult, BOOL exFlag);
