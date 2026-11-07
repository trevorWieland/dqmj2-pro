#include "context000.h"

u32 native_host_arm7_wram_038043a4(void)
{
    native_host_arm7_arm_037fe5a8(EXI_GPIOIF_GPIO);
    SPI_Wait();
    TP_SPIChangeMode(SPI_TRANSMODE_CONTINUOUS);
    SPI_SendWait(0x84 );
    native_host_arm7_arm_03804498();
    TP_SPIChangeMode(SPI_TRANSMODE_1BYTE);
    native_host_arm7_arm_03804498();
    if (!native_host_arm7_data_03809ea8) {
        return !((*( REGType16v *) (0x04000000 + 0x136)) & 0x0040 );
    }
    if (!((*( REGType16v *) (0x04000000 + 0x136)) & 0x0040 )) {
        return TOUCH_ON;
    }
    TP_SPIChangeMode(SPI_TRANSMODE_CONTINUOUS);
    SPI_SendWait(0x84 );
    native_host_arm7_arm_03804498();
    TP_SPIChangeMode(SPI_TRANSMODE_1BYTE);
    native_host_arm7_arm_03804498();
    if (!((*( REGType16v *) (0x04000000 + 0x136)) & 0x0040 )) {
        return TOUCH_MAY_OFFNOISE;
    } else {
        return TOUCH_OFF;
    }
}
