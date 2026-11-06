#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e1728(WlMaMpEndInd *pInd, u16 pollBitmap, BOOL minPollBmpMode)
{
    WlMpKeyData *kd;
    s32 i;
    u16 temp;
    u16 min;
    WMStatus *status = WMSP_GetStatusStructure();
    min = status->minRssi;
    if (pollBitmap != 0) {
        return;
    } else if (pInd->mpKey.count < 1) {
        return;
    } else {
        for (i = 0; i < pInd->mpKey.count; i++) {
            kd = (WlMpKeyData *)((u32)pInd->mpKey.data + (pInd->mpKey.length * i));
            temp = WMSP_GetRssi8(kd->rssi);
            if (temp < min) {
                min = temp;
            }
        }
    }
    status->minRssi = min;
}
