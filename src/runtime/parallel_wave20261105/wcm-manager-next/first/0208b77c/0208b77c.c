#include "context.h"
u8 native_main_0208b77c (void)
{
    s32 sum = 0;
    s32 i;
    if (native_data_021cfce4 > WCM_RSSI_COUNT_MAX) {
        for (i = 0; i < WCM_RSSI_COUNT_MAX; i++) {
            sum += native_data_021cfce8[i];
        }
        sum /= WCM_RSSI_COUNT_MAX;
    } else if (native_data_021cfce4 > 0)   {
        for (i = 0; i < native_data_021cfce4; i++) {
            sum += native_data_021cfce8[i];
        }
        sum /= native_data_021cfce4;
    }
    return (u8) sum;
}
