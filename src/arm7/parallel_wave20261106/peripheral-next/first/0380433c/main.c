#include "context000.h"

void native_host_arm7_wram_0380433c(void *arg)
{
    if (!native_host_arm7_arm_03803b7c(SPI_DEVICE_TYPE_TP, 0x0010 , 1, (u32)arg)) {
        SPITpData temp;
        temp.e.validity = SPI_TP_VALIDITY_INVALID_XY;
        *((u16 *)(&(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->touch_panel[0]))) = temp.halfs[0];
        *((u16 *)(&(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->touch_panel[2]))) = temp.halfs[1];
        native_host_arm7_arm_03803a48(0x0010 , (u32)arg & 0xFF);
    }
}
