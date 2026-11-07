#include "context000.h"

void native_host_arm7_main_027f6538(void)
{
    RTCRawStatus1 stat1;
    RTCRawStatus2 stat2;
    native_host_arm7_arm_027f6b10(&stat1);
    if (stat1.intr1 || stat1.intr2) {
        native_host_arm7_arm_027f6b74(&stat2);
        u32 intr_num = 0;
        if (stat1.intr1) {
            intr_num |= 1;
            stat2.intr_mode = 0x0 ;
        }
        if (stat1.intr2) {
            intr_num |= 2;
            stat2.intr2_mode = 0;
        }
        native_host_arm7_arm_027f6ba0(&stat2);
        native_host_arm7_arm_027f6074(0x30 , intr_num);
    }
}
