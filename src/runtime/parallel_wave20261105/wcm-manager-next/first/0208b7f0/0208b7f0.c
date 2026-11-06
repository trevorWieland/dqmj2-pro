#include "context.h"
void native_main_0208b7f0 (u8 rssi)
{
    u8 raw;
    if (rssi & 0x02) {
        raw = (u8) (rssi >> 2);
    } else {
        raw = (u8) (25 + (rssi >> 2));
    }
    native_data_021cfce8[native_data_021cfce4 % WCM_RSSI_COUNT_MAX] = raw;
    if (native_data_021cfce4 >= WCM_RSSI_COUNT_MAX) {
        native_data_021cfce4 = (u8) (((1 + native_data_021cfce4) % WCM_RSSI_COUNT_MAX) + WCM_RSSI_COUNT_MAX);
    } else {
        native_data_021cfce4++;
    }
}
