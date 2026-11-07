#include "context000.h"

void native_host_arm7_main_027f667c(u16 format)
{
    RTCRawStatus1 stat1;
    RTCRawAlarm alarm;
    format %= 2;
    if (format != 1) {
        return;
    }
    RTC_ReadStatus1(&stat1);
    if (stat1.format != format) {
        stat1.format = format;
        RTC_WriteStatus1(&stat1);
        native_host_arm7_arm_027f6ec0(0x86 , 0x10 , &alarm, 3);
        if (format == 0) {
            native_host_arm7_arm_027f6ca0(&alarm);
        } else {
            native_host_arm7_arm_027f6db0(&alarm);
        }
        native_host_arm7_arm_027f6ec0(0x06 , 0x10 , &alarm, 3);
        native_host_arm7_arm_027f6ec0(0x86 , 0x50 , &alarm, 3);
        if (format == 0) {
            native_host_arm7_arm_027f6ca0(&alarm);
        } else {
            native_host_arm7_arm_027f6db0(&alarm);
        }
        native_host_arm7_arm_027f6ec0(0x06 , 0x50 , &alarm, 3);
    }
}

#include "context001.h"
