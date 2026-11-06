#include "dependency000.h"

BOOL native_utility_child_arm7_main_027e3a3c(WMBssDesc *bssDesc)
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
