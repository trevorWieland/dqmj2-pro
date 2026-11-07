#include "context000.h"

void native_host_arm7_main_027f4ddc(void)
{
    vu32 statusReg;
    while (1 ) {
        native_host_arm7_arm_027f5554((u8 *)&statusReg);
        if (statusReg & 0x20 ) {
            native_host_arm7_arm_027f5c90();
        } else if (!(statusReg & 0x01 )) {
            break;
        }
    }
}
