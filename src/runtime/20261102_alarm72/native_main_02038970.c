typedef unsigned long u32;
int native_main_02038970(void);
extern u32 native_data_main_020f4c38[2];
int native_main_02038970 (void)
{
    int alarmNo;
    u32 mask = 1;
    for (alarmNo = 0; alarmNo < 8 ; alarmNo++, mask <<= 1) {
        if ((native_data_main_020f4c38[1] & mask) == 0) {
            native_data_main_020f4c38[1] |= mask;
            return alarmNo;
        }
    }
    return -1;
}
