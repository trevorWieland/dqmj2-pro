static inline u8 WMSP_GetRssi8(u8 rssi)
{
    if (rssi & 0x0002) {
        return (u8)(rssi >> 2);
    }
    return (u8)((rssi >> 2) + 25);
}

void native_utility_child_arm7_main_027e1728(WlMaMpEndInd *pInd, u16 pollBitmap, BOOL minPollBmpMode);
